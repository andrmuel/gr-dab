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
# Moritz Luca Schmid, 2017
# luca.m.schmid@gmail.com

from gnuradio import gr, blocks
from gnuradio.dab import dab_python

class detect_null(gr.hier_block2):
	"""
	@brief Detect Null symbols by looking at the energy of the symbol

	This block outputs a 1 where a new DAB frame begins, and zeros otherwise.
	"""
	
	def __init__(self, length, debug=False):
		"""
		Hierarchical block to detect Null symbols

		@param length length of the Null symbol (in samples)
		@param debug whether to write signals out to files
		"""
		gr.hier_block2.__init__(self,"detect_null",
		                        gr.io_signature(1, 1, gr.sizeof_gr_complex),    # input signature
					gr.io_signature(1, 1, gr.sizeof_char))          # output signature


		# get the magnitude squared
		self.ns_c2magsquared = blocks.complex_to_mag_squared()
		
		# this wastes cpu cycles:
		# ns_detect_taps = [1]*length
		# self.ns_moving_sum = gr.fir_filter_fff(1,ns_detect_taps)
		# this isn't better:
		#self.ns_filter = gr.iir_filter_ffd([1]+[0]*(length-1)+[-1],[0,1])
		# this does the same again, but is actually faster (outsourced to an independent block ..):
		self.ns_moving_sum = dab_python.moving_sum_ff(length)
		self.ns_invert = blocks.multiply_const_ff(-1)

		# peak detector on the inverted, summed up signal -> we get the nulls (i.e. the position of the start of a frame)
		self.ns_peak_detect = dab_python.peak_detector_fb(0.6,0.7,10,0.0001) # mostly found by try and error -> remember that the values are negative!

		# connect it all
		self.connect(self, self.ns_c2magsquared, self.ns_moving_sum, self.ns_invert, self.ns_peak_detect, self)

		if debug:
			self.connect(self.ns_invert, blocks.file_sink(gr.sizeof_float, "debug/ofdm_sync_dab_ns_filter_inv_f.dat"))
			self.connect(self.ns_peak_detect,blocks.file_sink(gr.sizeof_char, "debug/ofdm_sync_dab_peak_detect_b.dat"))
	
	def clear_state(self):	
		self.ns_moving_sum.reset()
		self.ns_peak_detect.clear_state()
