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

# ofdm.py - modulator and demodulator for the DAB physical layer 
#
# the code in this file is partially adapted from ofdm.py and ofdm_receiver.py
# from the gnuradio trunk; this implementation is however stream based, not
# packet based
#
# Andreas Mueller, 2008
# andrmuel@ee.ethz.ch

from gnuradio import gr, dab
import parameters
import ofdm_sync_dab
import ofdm_sync_dab2
import detect_null
import threading
import time

class ofdm_mod(gr.hier_block2):
	"""
	@brief Block to create a DAB signal from bits.

	Takes a data stream and performs OFDM modulation according to the DAB standard.
	The output sample rate is 2.048 MSPS.
	"""
	
	def __init__(self, mode=1):
		"""
		Hierarchical block for OFDM modulation

		@param mode DAB mode (I-IV)
		"""

		self.mode = mode
		dp = parameters.dab_parameters(mode)

		gr.hier_block2.__init__(self,"ofdm_mod",
		                        gr.io_signature(1, 1, gr.sizeof_char*dp.num_carriers/4), # input signature
					gr.io_signature(1, 1, gr.sizeof_gr_complex)) # output signature


		# symbol mapping
		self.mapper = dab.qpsk_mapper_vbc(dp.num_carriers)
		
		# add pilot symbol

		# phase sum
		
		# frequency interleaving
		self.interleave = dab.frequency_interleaver_vcc(frequency_interleaving_sequence_array)

		# add central carrier & move to middle

		# ifft
		self.ifft = gr.fft_vcc(dp.fft_length, False, [1]*dp.fft_length, True)

		# cyclic prefixer
		self.prefixer = gr.ofdm_cyclic_prefixer(dp.fft_length, dp.symbol_length)

		# add null symbol

		#
		# connect it all
		#


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
		@param debug enables debug output to files
		"""

		self.mode = mode
		self.verbose = verbose
		dp = parameters.dab_parameters(mode)
		self.dp = dp
		rp = parameters.receiver_parameters(mode)

		gr.hier_block2.__init__(self,"ofdm_demod",
		                        gr.io_signature(1, 1, gr.sizeof_gr_complex), # input signature
					gr.io_signature(1, 1, gr.sizeof_char*dp.num_carriers/4)) # output signature

		

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
			self.rate_estimator = dab.estimate_sample_rate_bf(dp.sample_rate, dp.frame_length)
			self.prober = gr.probe_signal_f()
			self.connect(self.input, self.rate_detect_ns, self.rate_estimator, self.prober)
			# self.resample = gr.fractional_interpolator_cc(0, 1)
			self.resample = dab.fractional_interpolator_triggered_update_cc(0,1)
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
		# self.sync = ofdm_sync_dab.ofdm_sync_dab(mode, debug)
		self.sync = ofdm_sync_dab2.ofdm_sync_dab2(mode, debug)

		# ofdm symbol sampler
		self.sampler = dab.ofdm_sampler(dp.fft_length, dp.cp_length, dp.symbols_per_frame, rp.cp_gap)
		
		# fft for symbol vectors
		self.fft = gr.fft_vcc(dp.fft_length, True, [1]*dp.fft_length, True)

		# coarse frequency synchronisation
		self.cfs = dab.ofdm_coarse_frequency_correct(dp.fft_length, dp.num_carriers)

		# diff phasor
		self.phase_diff = dab.diff_phasor_vcc(dp.num_carriers)

		# remove pilot symbol
		self.remove_pilot = dab.ofdm_remove_first_symbol_vcc(dp.num_carriers)

		# frequency deinterleaving
		self.deinterleave = dab.frequency_interleaver_vcc(dp.frequency_deinterleaving_sequence_array)

		# complex to phase
		self.arg = gr.complex_to_arg(dp.num_carriers)

		# correct frequency dependent phase offset
		# self.correct_phase_offset = dab.correct_individual_phase_offset_vff(dp.num_carriers,0.01)
		self.correct_phase_offset = gr.add_const_vff([0]*dp.num_carriers)
		
		# symbol demapping
		self.demapper = dab.qpsk_demapper_vcb(dp.num_carriers)

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
		self.connect((self.sync, 0), (self.sampler, 0))
		self.connect((self.sampler, 0), self.fft, (self.cfs, 0))
		self.connect((self.sync, 1), (self.sampler, 1))
		self.connect((self.sampler, 1), (self.cfs, 1))
		self.connect((self.cfs,0), self.phase_diff)
		self.connect(self.phase_diff, (self.remove_pilot,0))
		self.connect((self.cfs,1), (self.remove_pilot,1))
		self.connect((self.remove_pilot,0), self.deinterleave, self.demapper, self)
				
		self.connect(self.arg, self.correct_phase_offset)

		if debug:
			self.connect(self.fft, gr.file_sink(gr.sizeof_gr_complex*dp.fft_length, "debug/ofdm_after_fft.dat"))
			self.connect((self.cfs,0), gr.file_sink(gr.sizeof_gr_complex*dp.num_carriers, "debug/ofdm_after_cfs.dat"))
			self.connect(self.phase_diff, gr.file_sink(gr.sizeof_gr_complex*dp.num_carriers, "debug/ofdm_diff_phasor.dat"))
			self.connect(self.correct_phase_offset, gr.file_sink(gr.sizeof_float*dp.num_carriers, "debug/ofdm_phase_offset_corrected.dat"))
			self.connect((self.remove_pilot,1), gr.file_sink(gr.sizeof_char, "debug/ofdm_after_cfs_trigger.dat"))
		else: #FIXME remove once completed
			self.nop0 = gr.nop(gr.sizeof_gr_complex*dp.num_carriers)
			self.nop1 = gr.nop(gr.sizeof_char)
			self.nop2 = gr.nop(gr.sizeof_float*dp.num_carriers)
			self.nop3 = gr.nop(gr.sizeof_char)
			self.connect(self.phase_diff, self.nop0)
			self.connect((self.cfs,1), self.nop1)
			self.connect(self.correct_phase_offset, self.nop2)
			self.connect((self.remove_pilot,1), self.nop3)



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
