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

# Andreas Mueller, 2008
# andrmuel@ee.ethz.ch

"""
estimate the sample rate of DAB samples by looking at the Null symbols
"""

from gnuradio import gr, blocks
from gnuradio.eng_option import eng_option
import gnuradio.dab as grdab
from optparse import OptionParser

class estimate_samplerate(gr.top_block):
	"""
	@brief Estimate actual sample rate

	Looks for Null symbols and estimates the real sample rate by counting
	the samples between two Null symbols.
	"""
	def __init__(self):
		gr.top_block.__init__(self)

		usage = "%prog: [options] samples_file"
		parser = OptionParser(option_class=eng_option, usage=usage)
  		parser.add_option("-m", "--dab-mode", type="int", default=1,
        	     	help="DAB mode [default=%default]")
  		parser.add_option('-u', '--usrp-source', action="store_true", default=False,
	     		help="Samples from USRP (-> resample from 2 MSPS to 2.048 MSPS)")
		(options, args) = parser.parse_args ()

		dp = grdab.dab_parameters(options.dab_mode)
		filename = args[0]

		self.src = blocks.file_source(gr.sizeof_gr_complex, filename, False)
		self.resample = blocks.rational_resampler_ccc(2048,2000)
		self.rate_detect_ns = grdab.detect_null.detect_null(dp.ns_length, False)
		self.rate_estimator = grdab.blocks.estimate_sample_rate_bf(dp.sample_rate, dp.frame_length)
		self.decimate = blocks.keep_one_in_n(gr.sizeof_float, dp.frame_length)
		self.ignore_first = blocks.skiphead(gr.sizeof_float, 1)
		self.sink = blocks.vector_sink_f()

		if options.usrp_source:
			self.connect(self.src, self.resample, self.rate_detect_ns, self.rate_estimator, self.decimate, self.ignore_first, self.sink)
		else:
			self.connect(self.src, self.rate_detect_ns, self.rate_estimator, self.decimate, self.ignore_first, self.sink)


if __name__=='__main__':
	try:
		es = estimate_samplerate()
		es.run()
		print "sample rate estimation (average): " + str(sum(es.sink.data())/len(es.sink.data())) + " SPS"
	except KeyboardInterrupt:
		pass


