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

# ofdm_sync_dab.py - OFDM synchronisation for DAB
#
# Andreas Mueller, 2008
# andrmuel@ee.ethz.ch

from gnuradio import gr
import dab_python
import sys
from math import pi
import parameters, detect_null

class ofdm_sync_dab(gr.hier_block2):
	"""
	@brief OFDM Energy based time synchronisation and coarse frequency synchronisation for DAB signals

	This block implements synchronisation. Time synchronisation is done by using the NULL symbols.
	Fine frequency synchronisation is done by correlating the cyclic prefix with the last part of the symbol.
	"""
	def __init__(self, mode, debug=False):
		"""
		OFDM time and coarse frequency synchronisation for DAB

		@param mode DAB mode (1-4)
		@param debug if True: write data streams out to files
		"""

		if mode<1 or mode>4:
			raise ValueError, "Invalid DAB mode: "+str(mode)+" (modes 1-4 exist)"

		# get the correct DAB parameters
		dp = parameters.dab_parameters(mode)
		rp = parameters.receiver_parameters(mode)
		
		gr.hier_block2.__init__(self,"ofdm_sync_dab",
		                        gr.io_signature(1, 1, gr.sizeof_gr_complex), # input signature
					gr.io_signature2(2, 2, gr.sizeof_gr_complex, gr.sizeof_char)) # output signature

		# workaround for a problem that prevents connecting more than one block directly (see trac ticket #161)
		self.input = gr.kludge_copy(gr.sizeof_gr_complex)
		self.connect(self, self.input)

		#
		# null-symbol detection
		#
		# (outsourced to detect_zero.py)
		
		self.ns_detect = detect_null.detect_null(dp.ns_length, debug)
		self.connect(self.input, self.ns_detect)

		#
		# fine frequency synchronisation
		#

		# the code for fine frequency synchronisation is adapted from
		# ofdm_sync_ml.py; it abuses the cyclic prefix to find the fine
		# frequency error, as suggested in "ML Estimation of Timing and
		# Frequency Offset in OFDM Systems", by Jan-Jaap van de Beek,
		# Magnus Sandell, Per Ola Börjesson, see
		# http://www.sm.luth.se/csee/sp/research/report/bsb96r.html

		self.ffs_delay = gr.delay(gr.sizeof_gr_complex, dp.fft_length)
		self.ffs_conj = gr.conjugate_cc()
		self.ffs_mult = gr.multiply_cc()
		# self.ffs_moving_sum = gr.fir_filter_ccf(1, [1]*dp.cp_length)
		self.ffs_moving_sum = dab_python.moving_sum_cc(dp.cp_length)
		self.ffs_angle = gr.complex_to_arg()
		self.ffs_angle_scale = gr.multiply_const_ff(1./dp.fft_length)
		self.ffs_delay_sample_and_hold = gr.delay(gr.sizeof_char, dp.symbol_length) # sample the value at the end of the symbol ..
		self.ffs_sample_and_hold = gr.sample_and_hold_ff()
		self.ffs_delay_input_for_correction = gr.delay(gr.sizeof_gr_complex, dp.symbol_length) # by delaying the input, we can use the ff offset estimation from the first symbol to correct the first symbol itself
		self.ffs_nco = gr.frequency_modulator_fc(1) # ffs_sample_and_hold directly outputs phase error per sample
		self.ffs_mixer = gr.multiply_cc()

		# calculate fine frequency error
		self.connect(self.input, self.ffs_conj, self.ffs_mult)
		self.connect(self.input, self.ffs_delay, (self.ffs_mult, 1))
		self.connect(self.ffs_mult, self.ffs_moving_sum, self.ffs_angle)
		# only use the value from the first half of the first symbol
		self.connect(self.ffs_angle, self.ffs_angle_scale, (self.ffs_sample_and_hold, 0))
		self.connect(self.ns_detect, self.ffs_delay_sample_and_hold, (self.ffs_sample_and_hold, 1))
		# do the correction
		self.connect(self.ffs_sample_and_hold, self.ffs_nco, (self.ffs_mixer, 0))
		self.connect(self.input, self.ffs_delay_input_for_correction, (self.ffs_mixer, 1))

		# output - corrected signal and start of DAB frames
		self.connect(self.ffs_mixer, (self, 0))
		self.connect(self.ffs_delay_sample_and_hold, (self, 1))

		if debug:
			self.connect(self.ffs_angle, gr.file_sink(gr.sizeof_float, "debug/ofdm_sync_dab_ffs_angle.dat"))
			self.connect(self.ffs_sample_and_hold, gr.multiply_const_ff(1./(dp.T*2*pi)), gr.file_sink(gr.sizeof_float, "debug/ofdm_sync_dab_fine_freq_err_f.dat"))
			self.connect(self.ffs_mixer, gr.file_sink(gr.sizeof_gr_complex, "debug/ofdm_sync_dab_fine_freq_corrected_c.dat"))
	
	def clear_state(self):
		self.ffs_moving_sum.reset()
		self.ns_detect.clear_state()
