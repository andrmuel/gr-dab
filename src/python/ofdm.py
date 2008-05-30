#!/usr/bin/env python
#
# Copyright 2008 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

# the code in this file is partially adapted from ofdm.py from the gnuradio
# trunk (actually, only frequency synchronisation is done the same way, as that
# implementation otherwise is not suited for DAB)
#
# Andreas Mueller, 2008
# andrmuel@ee.ethz.ch

from gnuradio import gr, dab_swig
import parameters
import ofdm_sync_dab
import detect_null
import threading
import time
from math import pi

"""
modulator and demodulator for the DAB physical layer 
"""

class ofdm_mod(gr.hier_block2):
	"""
	@brief Block to create a DAB signal from bits.

	Takes a data stream and performs OFDM modulation according to the DAB standard.
	The output sample rate is 2.048 MSPS.
	"""
	
	def __init__(self, mode=1, debug=False):
		"""
		Hierarchical block for OFDM modulation

		@param mode DAB mode (I-IV)
		"""

		self.mode = mode
		dp = parameters.dab_parameters(mode)

		gr.hier_block2.__init__(self,"ofdm_mod",
		                        gr.io_signature2(2, 2, gr.sizeof_char*dp.num_carriers/4, gr.sizeof_char), # input signature
					gr.io_signature (1, 1, gr.sizeof_gr_complex)) # output signature


		# symbol mapping
		self.mapper = dab_swig.qpsk_mapper_vbc(dp.num_carriers)

		# add pilot symbol
		self.insert_pilot = dab_swig.ofdm_insert_pilot_vcc(dp.prn)

		# phase sum
		self.sum_phase = dab_swig.sum_phasor_trig_vcc(dp.num_carriers)

		# frequency interleaving
		self.interleave = dab_swig.frequency_interleaver_vcc(dp.frequency_interleaving_sequence_array)

		# add central carrier & move to middle
		self.move_and_insert_carrier = dab_swig.ofdm_move_and_insert_zero(dp.fft_length, dp.num_carriers)

		# ifft
		self.ifft = gr.fft_vcc(dp.fft_length, False, [], True)

		# cyclic prefixer
		self.prefixer = gr.ofdm_cyclic_prefixer(dp.fft_length, dp.symbol_length)

		# convert back to vectors
		self.s2v = gr.stream_to_vector(gr.sizeof_gr_complex, dp.symbol_length)

		# add null symbol
		self.insert_null = dab_swig.insert_null_symbol(dp.ns_length, dp.symbol_length)

		#
		# connect it all
		#

		# data
		self.connect((self,0), self.mapper, (self.insert_pilot,0), (self.sum_phase,0), self.interleave, self.move_and_insert_carrier, self.ifft, self.prefixer, self.s2v, (self.insert_null,0))
		self.connect(self.insert_null, self)

		# control signal (frame start)
		self.connect((self,1), (self.insert_pilot,1), (self.sum_phase,1), (self.insert_null,1))

		if debug:
			self.connect(self.mapper, gr.file_sink(gr.sizeof_gr_complex*dp.num_carriers, "debug/generated_signal_mapper.dat"))
			self.connect(self.insert_pilot, gr.file_sink(gr.sizeof_gr_complex*dp.num_carriers, "debug/generated_signal_insert_pilot.dat"))
			self.connect(self.sum_phase, gr.file_sink(gr.sizeof_gr_complex*dp.num_carriers, "debug/generated_signal_sum_phase.dat"))
			self.connect(self.interleave, gr.file_sink(gr.sizeof_gr_complex*dp.num_carriers, "debug/generated_signal_interleave.dat"))
			self.connect(self.move_and_insert_carrier, gr.file_sink(gr.sizeof_gr_complex*dp.fft_length, "debug/generated_signal_move_and_insert_carrier.dat"))
			self.connect(self.ifft, gr.file_sink(gr.sizeof_gr_complex*dp.fft_length, "debug/generated_signal_ifft.dat"))
			self.connect(self.prefixer, gr.file_sink(gr.sizeof_gr_complex, "debug/generated_signal_prefixer.dat"))
			self.connect(self.insert_null, gr.file_sink(gr.sizeof_gr_complex, "debug/generated_signal.dat"))



class ofdm_demod(gr.hier_block2):
	"""
	@brief Block to demodulate a DAB signal into bits.

	Takes a stream of complex baseband samples and performs OFDM demodulation according to the DAB standard.
	Expects an input sample rate of 2.048 MSPS.
	"""
	
	def __init__(self, mode=1, rx_filter=True, autocorrect_sample_rate=False, sample_rate_correction_factor=1, debug=False, verbose=False):
		"""
		Hierarchical block for OFDM demodulation

		@param mode DAB mode (1-4)
		@param rx_filter disable/enable FFT bandbass at input
		@param autocorrect_sample_rate whether to correct the sample rate dynamically
		@param sample_rate_correction_factor static correction factor for sample rate
		@param debug enables debug output to files
		@param verbose whether to produce verbose messages
		"""

		self.mode = mode
		self.verbose = verbose
		dp = parameters.dab_parameters(mode)
		self.dp = dp
		rp = parameters.receiver_parameters(mode)

		gr.hier_block2.__init__(self,"ofdm_demod",
		                        gr.io_signature (1, 1, gr.sizeof_gr_complex), # input signature
					gr.io_signature2(2, 2, gr.sizeof_char*dp.num_carriers/4, gr.sizeof_char)) # output signature

		

		# workaround for a problem that prevents connecting more than one block directly (see trac ticket #161)
		self.input = gr.kludge_copy(gr.sizeof_gr_complex)
		self.connect(self, self.input)
		
		# input filtering
		if rx_filter: 
			if verbose: print "--> RX filter enabled"
			lowpass_taps = gr.firdes_low_pass(1.0,                     # gain
							  dp.sample_rate,          # sampling rate
							  rp.filt_bw,              # cutoff frequency
							  rp.filt_tb,              # width of transition band
							  gr.firdes.WIN_HAMMING)   # Hamming window
			self.fft_filter = gr.fft_filter_ccc(1, lowpass_taps)
		

		# correct sample rate offset, if enabled
		if autocorrect_sample_rate:
			if verbose: print "--> dynamic sample rate correction enabled"
			self.rate_detect_ns = detect_null.detect_null(dp.ns_length, False)
			self.rate_estimator = dab_swig.estimate_sample_rate_bf(dp.sample_rate, dp.frame_length)
			self.prober = gr.probe_signal_f()
			self.connect(self.input, self.rate_detect_ns, self.rate_estimator, self.prober)
			# self.resample = gr.fractional_interpolator_cc(0, 1)
			self.resample = dab_swig.fractional_interpolator_triggered_update_cc(0,1)
			self.connect(self.rate_detect_ns, (self.resample,1))
			self.updater = threading.Timer(0.1,self.update_correction)
			# self.updater = threading.Thread(target=self.update_correction)
			self.run_interpolater_update_thread = True
			self.updater.setDaemon(True)
			self.updater.start()
		else:
			self.run_interpolater_update_thread = False
			if sample_rate_correction_factor != 1:
				if verbose: print "--> static sample rate correction enabled"
				self.resample = gr.fractional_interpolator_cc(0, sample_rate_correction_factor)

		# timing and fine frequency synchronisation
		self.sync = ofdm_sync_dab.ofdm_sync_dab(mode, debug)

		# ofdm symbol sampler
		self.sampler = dab_swig.ofdm_sampler(dp.fft_length, dp.cp_length, dp.symbols_per_frame, rp.cp_gap)
		
		# fft for symbol vectors
		self.fft = gr.fft_vcc(dp.fft_length, True, [], True)

		# coarse frequency synchronisation
		self.cfs = dab_swig.ofdm_coarse_frequency_correct(dp.fft_length, dp.num_carriers, dp.cp_length)

		# diff phasor
		self.phase_diff = dab_swig.diff_phasor_vcc(dp.num_carriers)

		# remove pilot symbol
		self.remove_pilot = dab_swig.ofdm_remove_first_symbol_vcc(dp.num_carriers)

		# frequency deinterleaving
		self.deinterleave = dab_swig.frequency_interleaver_vcc(dp.frequency_deinterleaving_sequence_array)

		# complex to phase
		self.arg = gr.complex_to_arg(dp.num_carriers)

		# correct frequency dependent phase offset
		# self.correct_phase_offset = dab_swig.correct_individual_phase_offset_vff(dp.num_carriers,0.01)
		self.correct_phase_offset = gr.add_const_vff([0]*dp.num_carriers)
		
		# symbol demapping
		self.demapper = dab_swig.qpsk_demapper_vcb(dp.num_carriers)

		#
		# connect everything
		#

		if autocorrect_sample_rate or sample_rate_correction_factor != 1:
			self.connect(self.input, self.resample)
			self.input2 = self.resample
		else:
			self.input2 = self.input
		if rx_filter:
			self.connect(self.input2, self.fft_filter, self.sync)
		else:
			self.connect(self.input2, self.sync)

		# data stream
		self.connect((self.sync, 0), (self.sampler, 0), self.fft, (self.cfs, 0), self.phase_diff, 
				(self.remove_pilot,0), self.deinterleave, self.demapper, (self,0))

		# control stream
		self.connect((self.sync, 1), (self.sampler, 1), (self.cfs, 1), (self.remove_pilot,1), (self,1))
			
		# TODO correct phase offset
		# self.connect(self.remove_pilot, self.arg, self.correct_phase_offset)

		# calculate an estimate of the SNR
		alpha = 0.05
		self.average_snr_estimate = gr.iir_filter_ffd([alpha], [0,1-alpha])
		self.probe_snr_estimate = gr.probe_signal_f()
		self.connect((self.remove_pilot,0), self.arg, dab_swig.sum_elements_vff(dp.num_carriers), dab_swig.modulo_ff(pi/2), gr.multiply_const_ff(1/float(dp.num_carriers)), gr.add_const_ff(-pi/4), self.average_snr_estimate, self.probe_snr_estimate)
		
		# debugging
		if debug:
			self.connect(self.fft, gr.file_sink(gr.sizeof_gr_complex*dp.fft_length, "debug/ofdm_after_fft.dat"))
			self.connect((self.cfs,0), gr.file_sink(gr.sizeof_gr_complex*dp.num_carriers, "debug/ofdm_after_cfs.dat"))
			self.connect(self.phase_diff, gr.file_sink(gr.sizeof_gr_complex*dp.num_carriers, "debug/ofdm_diff_phasor.dat"))
			# self.connect(self.correct_phase_offset, gr.file_sink(gr.sizeof_float*dp.num_carriers, "debug/ofdm_phase_offset_corrected.dat"))
			self.connect((self.remove_pilot,1), gr.file_sink(gr.sizeof_char, "debug/ofdm_after_cfs_trigger.dat"))
	
	def clear_state(self):
		self.sync.clear_state()

	def update_correction(self):
		while self.run_interpolater_update_thread:
			rate = self.prober.level()
			# print "resampling: "+str(rate)
			self.resample.set_interp_ratio(rate/self.dp.sample_rate)
			time.sleep(0.1)
	
	def stop(self):
		if self.run_interpolater_update_thread:
			self.run_interpolater_update_thread = False
			self.updater.join()
