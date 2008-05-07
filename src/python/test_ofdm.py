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

# test_ofdm.py - test the ofdm demod block
#
# Andreas Mueller, 2008
# andrmuel@ee.ethz.ch

from gnuradio import gr, blks2
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import ofdm
import parameters
import random
import os

class test_ofdm(gr.top_block):
	"""
	@brief Test program for the ofdm_demod class.
	"""
	def __init__(self):
		gr.top_block.__init__(self)
		
		mode = 1
		dp = parameters.dab_parameters(mode)

		usage = "%prog: [options] samples_file"
		parser = OptionParser(option_class=eng_option, usage=usage)
		(options, args) = parser.parse_args ()
		if len(args)<1:
			# print "using gaussian noise as source"
			# self.sigsrc = gr.noise_source_c(gr.GR_GAUSSIAN,10e6)
			print "using repeating random vector as source"
			self.sigsrc = gr.vector_source_c([10e6*(random.random() + 1j*random.random()) for i in range(0,100000)],True)
			self.ns_simulate = gr.vector_source_c([0.01]*dp.ns_length+[1]*dp.symbols_per_frame*dp.symbol_length,1)
			self.mult = gr.multiply_cc() # simulate null symbols ...
			self.src = gr.throttle( gr.sizeof_gr_complex,2048000)
			self.connect(self.sigsrc, (self.mult, 0))
			self.connect(self.ns_simulate, (self.mult, 1))
			self.connect(self.mult, self.src)
		else:
			filename = args[0]
			print "using samples from file " + filename
			self.src = gr.file_source(gr.sizeof_gr_complex, filename, False)

		self.resample = blks2.rational_resampler_ccc(128,125) #2048:2000

		self.dab_demod = ofdm.ofdm_demod(mode=1, debug=True)
		
		self.connect(self.src, self.resample, self.dab_demod)
		# self.connect(self.src, self.dab_demod)
		

if __name__=='__main__':
	try:
		test_ofdm().run()
	except KeyboardInterrupt:
		pass

