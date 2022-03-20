# _*_ coding: utf8 _*_

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

# Andreas Mueller, 2008
# andrmuel@ee.ethz.ch

from gnuradio import gr, blocks, analog
import gnuradio.dab as grdab
import sys
from math import pi

class ofdm_sync_dab2(gr.hier_block2):
	"""
	@brief OFDM Energy based time synchronisation and coarse frequency synchronisation for DAB signals

	This block implements synchronisation. Time synchronisation is done by using the NULL symbols.
	Fine frequency synchronisation is done by correlating the cyclic prefix with the last part of the symbol.

	In contrast to the first version, this block averages over multiple symbols to get better fine frequency error estimates.
	"""
	def __init__(self, dab_params, rx_params, debug=False):
		"""
		OFDM time and coarse frequency synchronisation for DAB

		@param mode DAB mode (1-4)
		@param debug if True: write data streams out to files
		"""

		dp = dab_params
		rp = rx_params
		
		gr.hier_block2.__init__(self,"ofdm_sync_dab",
		                        gr.io_signature(1, 1, gr.sizeof_gr_complex), # input signature
					gr.io_signature(1, 1, gr.sizeof_gr_complex)) # output signature

		# workaround for a problem that prevents connecting more than one block directly (see trac ticket #161)
		#self.input = gr.kludge_copy(gr.sizeof_gr_complex)
		self.input = blocks.multiply_const_cc(1) # FIXME
		self.connect(self, self.input)

		#
		# null-symbol detection
		#
		# (outsourced to detect_zero.py)
		
		self.ns_detect = grdab.detect_null(dp.ns_length, debug)
		self.connect(self.input, self.ns_detect)

		self.add_stream_tag = grdab.control_stream_to_tag_cc("dab_sync")
		#
		# fine frequency synchronisation
		#

		# the code for fine frequency synchronisation is adapted from
		# ofdm_sync_ml.py; it abuses the cyclic prefix to find the fine
		# frequency error, as suggested in "ML Estimation of Timing and
		# Frequency Offset in OFDM Systems", by Jan-Jaap van de Beek,
		# Magnus Sandell, Per Ola Börjesson, see
		# http://www.sm.luth.se/csee/sp/research/report/bsb96r.html

		self.ffe = grdab.ofdm_ffe_all_in_one(dp.symbol_length, dp.fft_length, rp.symbols_for_ffs_estimation, rp.ffs_alpha, int(dp.sample_rate))
		if rp.correct_ffe:
			self.ffs_delay_input_for_correction = blocks.delay(gr.sizeof_gr_complex, dp.symbol_length*rp.symbols_for_ffs_estimation) # by delaying the input, we can use the ff offset estimation from the first symbol to correct the first symbol itself
			self.ffs_delay_frame_start = blocks.delay(gr.sizeof_char, dp.symbol_length*rp.symbols_for_ffs_estimation) # sample the value at the end of the symbol ..
			self.ffs_nco = analog.frequency_modulator_fc(1) # ffs_sample_and_hold directly outputs phase error per sample
			self.ffs_mixer = blocks.multiply_cc()

		# calculate fine frequency error
		self.connect(self.ns_detect, (self.add_stream_tag, 1))
		self.connect(self.input, (self.add_stream_tag, 0))
		self.connect(self.add_stream_tag, self.ffe)

		if rp.correct_ffe: 
			# do the correction
			self.connect(self.ffe, self.ffs_nco, (self.ffs_mixer, 0))
			self.connect(self.add_stream_tag, self.ffs_delay_input_for_correction, (self.ffs_mixer, 1))
			# output - corrected signal and start of DAB frames
			self.connect(self.ffs_mixer, (self, 0))
		else: 
			# just patch the signal through
			self.connect(self.ffe, blocks.null_sink(gr.sizeof_float))
			self.connect(self.add_stream_tag, (self,0))
			# frame start still needed ..

		if debug:
			self.connect(self.ffe, blocks.multiply_const_ff(1./(dp.T*2*pi)), blocks.file_sink(gr.sizeof_float, "debug/ofdm_sync_dab_fine_freq_err_f.dat"))
			#self.connect(self.ffs_mixer, blocks.file_sink(gr.sizeof_gr_complex, "debug/ofdm_sync_dab_fine_freq_corrected_c.dat"))
	
	def clear_state(self):
		self.ns_detect.clear_state()
