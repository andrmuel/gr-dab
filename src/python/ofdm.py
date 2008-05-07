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


class ofdm_mod(gr.hier_block2):
	"""
	@brief Block to create a DAB signal from bits.

	Takes a data stream and performs OFDM modulation according to the DAB standard.
	The output sample rate is 2.048 MSPS.
	"""
	
	def __init__(self, mode=1):
		"""
		Hierarchical block for OFDM modulation

		@param mode: DAB mode (I-IV)
		"""

		self.mode = mode
		dp = parameters.dab_parameters(mode)

		gr.hier_block2.__init__(self,"ofdm_mod",
		                        gr.io_signature(1, 1, gr.sizeof_char*dp.carriers), # input signature
					gr.io_signature(1, 1, gr.sizeof_gr_complex)) # output signature


		# create dab frames

		# add pilot symbol

		# symbol mapper

		# phase sum

		# ifft

		# cyclic prefixer
		self.prefixer = gr.ofdm_cyclic_prefixer()

		# add null symbol

		pass

class ofdm_demod(gr.hier_block2):
	"""
	@brief Block to demodulate a DAB signal into bits.

	Takes a stream of complex baseband samples and performs OFDM demodulation according to the DAB standard.
	Expects an input sample rate of 2.048 MSPS.
	"""
	
	def __init__(self, mode=1, debug=False):
		"""
		Hierarchical block for OFDM demodulation

		@param mode DAB mode (I-IV)
		@param debug: write debug output to files
		"""

		self.mode = mode
		dp = parameters.dab_parameters(mode)
		rp = parameters.receiver_parameters(mode)

		gr.hier_block2.__init__(self,"ofdm_demod",
		                        gr.io_signature(1, 1, gr.sizeof_gr_complex), # input signature
					gr.io_signature(1, 1, gr.sizeof_char*dp.carriers)) # output signature

		

		# workaround for a problem that prevents connecting more than one block directly (see trac ticket #161)
		self.input = gr.kludge_copy(gr.sizeof_gr_complex)
		self.connect(self, self.input)
		
		# input filtering
		bw = (dp.carriers/2.0)/dp.fft_length
		tb = bw*0.15
		lowpass_taps = gr.firdes_low_pass(1.0,                     # gain
                                                  1.0,                     # sampling rate (1.0 works out fine, as the bandwidth is relative as well)
                                                  bw+tb,                   # cutoff frequency
                                                  tb,                      # width of transition band
                                                  gr.firdes.WIN_HAMMING)   # Hamming window
		self.fft_filter = gr.fft_filter_ccc(1, lowpass_taps)
		
		# timing and fine frequency synchronisation
		self.sync = ofdm_sync_dab.ofdm_sync_dab(mode, debug)

		# ofdm symbol sampler
		self.sampler = dab.ofdm_sampler(dp.fft_length, dp.cp_length, dp.symbols_per_frame, rp.cp_gap)
		
		# fft for symbol vectors
		self.fft = gr.fft_vcc(dp.fft_length, True, [1]*dp.fft_length, True)

		# coarse frequency synchronisation
		self.cfs = dab.ofdm_coarse_frequency_correct(dp.fft_length, dp.carriers)

		# diff phasor
		self.phase_diff = dab.diff_phasor_vcc(dp.carriers)

		# remove pilot symbol
		self.remove_pilot = dab.ofdm_remove_first_symbol_vcc(dp.carriers)

		# complex to phase
		self.arg = gr.complex_to_arg(dp.carriers)

		# correct frequency dependent phase offset
		self.correct_phase_offset = dab.correct_individual_phase_offset_vff(dp.carriers,0.01)
		
		self.connect(self.input, self.fft_filter, self.sync)
		# self.connect(self.input, self.sync)
		self.connect((self.sync, 0), (self.sampler, 0))
		self.connect((self.sampler, 0), self.fft, (self.cfs, 0))
		self.connect((self.sync, 1), (self.sampler, 1))
		self.connect((self.sampler, 1), (self.cfs, 1))
		self.connect((self.cfs,0), self.phase_diff)
		self.connect(self.phase_diff, (self.remove_pilot,0))
		self.connect((self.cfs,1), (self.remove_pilot,1))
		self.connect((self.remove_pilot,0), self.arg, self.correct_phase_offset)

		if debug:
			self.connect(self.fft, gr.file_sink(gr.sizeof_gr_complex*dp.fft_length, "debug/ofdm_after_fft.dat"))
			self.connect((self.cfs,0), gr.file_sink(gr.sizeof_gr_complex*dp.carriers, "debug/ofdm_after_cfs.dat"))
			self.connect(self.phase_diff, gr.file_sink(gr.sizeof_gr_complex*dp.carriers, "debug/ofdm_diff_phasor.dat"))
			self.connect(self.correct_phase_offset, gr.file_sink(gr.sizeof_float*dp.carriers, "debug/ofdm_phase_offset_corrected.dat"))
			self.connect((self.remove_pilot,1), gr.file_sink(gr.sizeof_char, "debug/ofdm_after_cfs_trigger.dat"))
		else: #FIXME remove once completed
			self.nop0 = gr.nop(gr.sizeof_gr_complex*dp.carriers)
			self.nop1 = gr.nop(gr.sizeof_char)
			self.connect(self.phase_diff, self.nop0)
			self.connect((self.cfs,1), self.nop1)



