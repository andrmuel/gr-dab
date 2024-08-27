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

from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
from optparse import OptionParser
from gnuradio.dab import ofdm
import parameters
import random

class test_ofdm(gr.top_block):
	"""
	@brief Test program for the ofdm_demod class.
	"""
	def __init__(self):
		gr.top_block.__init__(self)
		

		usage = "%prog: [options] samples_file"
		parser = OptionParser(option_class=eng_option, usage=usage)
  		parser.add_option("-m", "--dab-mode", type="int", default=1,
        	     	help="DAB mode [default=%default]")
		parser.add_option("-F", "--filter-input", action="store_true", default=False,
                          help="Enable FFT filter at input")
  		parser.add_option("-s", "--resample-fixed", type="float", default=1,
			help="resample by a fixed factor (fractional interpolation)")
		parser.add_option("-S", "--autocorrect-sample-rate", action="store_true", default=False,
                          help="Estimate sample rate offset and resample (dynamic fractional interpolation)")
  		parser.add_option('-r', '--sample-rate', type="int", default=2048000,
	     		help="Use non-standard sample rate (default=%default)")
  		parser.add_option('-e', '--equalize-magnitude', action="store_true", default=False,
	     		help="Enable individual carrier magnitude equalizer")
  		parser.add_option('-d', '--debug', action="store_true", default=False,
	     		help="Write output to files")
  		parser.add_option('-v', '--verbose', action="store_true", default=False,
	     		help="Print status messages")
		(options, args) = parser.parse_args ()
	
		dp = parameters.dab_parameters(options.dab_mode, verbose=options.verbose, sample_rate=options.sample_rate)

		rp = parameters.receiver_parameters(options.dab_mode, input_fft_filter=options.filter_input, autocorrect_sample_rate=options.autocorrect_sample_rate, sample_rate_correction_factor=options.resample_fixed, equalize_magnitude=options.equalize_magnitude, verbose=options.verbose)

		if len(args)<1:
			if options.verbose: print "-> using repeating random vector as source"
			self.sigsrc = blocks.vector_source_c([10e6*(random.random() + 1j*random.random()) for i in range(0,100000)],True)
			self.ns_simulate = blocks.vector_source_c([0.01]*dp.ns_length+[1]*dp.symbols_per_frame*dp.symbol_length,1)
			self.mult = blocks.multiply_cc() # simulate null symbols ...
			self.src = blocks.throttle( gr.sizeof_gr_complex,2048000)
			self.connect(self.sigsrc, (self.mult, 0))
			self.connect(self.ns_simulate, (self.mult, 1))
			self.connect(self.mult, self.src)
		else:
			filename = args[0]
			if options.verbose: print "-> using samples from file " + filename
			self.src = blocks.file_source(gr.sizeof_gr_complex, filename, False)

		self.dab_demod = ofdm.ofdm_demod(dp, rp, debug=options.debug, verbose=options.verbose)
		
		self.connect(self.src, self.dab_demod)

		# sink output to nowhere 
		self.nop0 = blocks.nop(gr.sizeof_char*dp.num_carriers/4)
		self.nop1 = blocks.nop(gr.sizeof_char)
		self.connect((self.dab_demod,0),self.nop0)
		self.connect((self.dab_demod,1),self.nop1)
			
if __name__=='__main__':
	try:
		to = test_ofdm()
		# to.run()
		to.run()
		to.dump()
		to.dab_demod.stop()
		
	except KeyboardInterrupt:
		pass

