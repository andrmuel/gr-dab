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

# test_ofdm_sync_dab.py - test the DAB OFDM synchronisation
#
# Andreas Mueller, 2008
# andrmuel@ee.ethz.ch

from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
from optparse import OptionParser
from ofdm_sync_dab import ofdm_sync_dab
import parameters
import random
import os

class dab_ofdm_sync_test(gr.top_block):
	"""
	@brief Test application for the synchronisation block.
	"""
	def __init__(self):
		gr.top_block.__init__(self)
		
		usage = "%prog: [options] samples_file"
		parser = OptionParser(option_class=eng_option, usage=usage)
		(options, args) = parser.parse_args ()
		if len(args)<1:
			# print "using gaussian noise as source"
			# self.sigsrc = gr.noise_source_c(gr.GR_GAUSSIAN,10e6)
			print "using repeating random vector as source"
			self.sigsrc = blocks.vector_source_c([10e6*(random.random() + 1j*random.random()) for i in range(0,100000)],True)
			self.src = blocks.throttle( gr.sizeof_gr_complex,2048000)
			self.connect(self.sigsrc, self.src)
		else:
			filename = args[0]
			print "using samples from file " + filename
			self.src = blocks.file_source(gr.sizeof_gr_complex, filename, False)

		dp = parameters.dab_parameters(1)
		rp = parameters.receiver_parameters(1)
		self.sync_dab = ofdm_sync_dab(dp, rp, False)
		self.nop0 = blocks.nop(gr.sizeof_gr_complex)
		self.nop1 = blocks.nop(gr.sizeof_char)
		self.connect(self.src, self.sync_dab, self.nop0)
		self.connect((self.sync_dab,1), self.nop1)

if __name__=='__main__':
	try:
		dab_ofdm_sync_test().run()
	except KeyboardInterrupt:
		pass
