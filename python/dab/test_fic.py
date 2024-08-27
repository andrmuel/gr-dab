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

from gnuradio import gr
from gnuradio.eng_option import eng_option
import gnuradio.dab as grdab
from optparse import OptionParser
import sys

class test_fic(gr.top_block):
	"""
	@brief Test program for the fic_decode class.
	"""
	def __init__(self):
		gr.top_block.__init__(self)

		usage = "%prog: [options] samples_file"
		parser = OptionParser(option_class=eng_option, usage=usage)
  		parser.add_option("-m", "--dab-mode", type="int", default=1,
        	     	help="DAB mode [default=%default]")
		parser.add_option("-F", "--filter-input", action="store_true", default=False,
                          help="Enable FFT filter at input")
  		parser.add_option("-s", "--resample-fixed", type="eng_float", default=1,
			help="resample by a fixed factor (fractional interpolation)")
		parser.add_option("-S", "--autocorrect-sample-rate", action="store_true", default=False,
                          help="Estimate sample rate offset and resample (dynamic fractional interpolation)")
  		parser.add_option('-u', '--usrp-source', action="store_true", default=False,
	     		help="Samples from USRP (-> adjust params for 2 MSPS)")
  		parser.add_option('-d', '--debug', action="store_true", default=False,
	     		help="Write output to files")
  		parser.add_option('-v', '--verbose', action="store_true", default=False,
	     		help="Print status messages")
		(options, args) = parser.parse_args ()
	
		if options.usrp_source:
			dp = grdab.dab_parameters(options.dab_mode, verbose=options.verbose, sample_rate=2000000)
		else:
			dp = grdab.dab_parameters(options.dab_mode, verbose=options.verbose)

		rp = grdab.receiver_parameters(options.dab_mode, softbits=True, input_fft_filter=options.filter_input, autocorrect_sample_rate=options.autocorrect_sample_rate, sample_rate_correction_factor=options.resample_fixed, correct_ffe=True, equalize_magnitude=True, verbose=options.verbose)

		if len(args)<1:
			print "error: need file with samples"
			sys.exit(1)
		else:
			filename = args[0]
			if options.verbose: print "--> using samples from file " + filename
			self.src = gr.file_source(gr.sizeof_gr_complex, filename, False)

		
		self.dab_demod = grdab.ofdm_demod(dp, rp, verbose=options.verbose, debug=options.debug)
		self.fic_dec   = grdab.fic_decode(dp, verbose=options.verbose, debug=options.debug)
		
		self.connect(self.src, self.dab_demod, self.fic_dec)
		self.connect((self.dab_demod,1), (self.fic_dec,1))

if __name__=='__main__':
	try:
		tf = test_fic()
		tf.run()
		tf.dab_demod.stop()
		print "processing rate: " + str(tf.dab_demod.measure_rate.processing_rate())
		print "bitrate: " + str(tf.dab_demod.measure_rate.bitrate())
	except KeyboardInterrupt:
		pass

