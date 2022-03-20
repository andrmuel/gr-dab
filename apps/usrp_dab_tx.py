#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
send DAB with USRP
"""

from gnuradio import gr, uhd, blocks
from gnuradio.eng_option import eng_option
import gnuradio.dab as grdab
from optparse import OptionParser
import sys

class usrp_dab_tx(gr.top_block):
	def __init__(self):
		gr.top_block.__init__(self)
        
		
		parser = OptionParser(option_class=eng_option, usage="%prog: [options] input-filename")
		parser.add_option("-T", "--tx-subdev-spec", type="subdev", default=(0, 0),
		     help="select USRP Tx side A or B [default=A]")
		parser.add_option("-f", "--freq", type="eng_float", default=227.36e6,
		     help="set frequency to FREQ [default=%default]")
		parser.add_option("-g", "--tx-gain", type="eng_float", default=None,
		     help="set transmit gain in dB (default is midpoint)")
		parser.add_option('-v', '--verbose', action="store_true", default=False,
		     help="verbose output")
		parser.add_option('-a', '--antenna', type="string", default="TX/RX",
		     help="select antenna")

        	(options, args) = parser.parse_args ()
		if len(args)!=1:
			parser.print_help()
			sys.exit(1)
		else:
			self.filename = args[0]

		# if gr.enable_realtime_scheduling() != gr.RT_OK:
		#       print "-> failed to enable realtime scheduling"

		interp = 64
		self.sample_rate = 128e6/interp
		self.dab_params = grdab.parameters.dab_parameters(mode=1, sample_rate=2000000, verbose=options.verbose)

		self.src = blocks.file_source(gr.sizeof_char, self.filename)
		self.trigsrc = blocks.vector_source_b([1]+[0]*(self.dab_params.symbols_per_frame-1),True)
		
		self.s2v = blocks.stream_to_vector(gr.sizeof_char, 384)
		
		self.mod = grdab.ofdm_mod(self.dab_params, verbose=options.verbose) 

		#self.sink = usrp.sink_c(interp_rate = interp)
		self.sink = uhd.usrp_sink("",uhd.io_type.COMPLEX_FLOAT32,1)
		self.sink.set_samp_rate(self.sample_rate)
        	#self.sink.set_mux(usrp.determine_tx_mux_value(self.sink, options.tx_subdev_spec))
        	#self.subdev = usrp.selected_subdev(self.sink, options.tx_subdev_spec)
		self.sink.set_antenna(options.antenna)
		
		print "--> using sample rate: " + str(self.sample_rate)


		self.connect(self.src, self.s2v, self.mod, self.sink)
		self.connect(self.trigsrc, (self.mod,1))

		# tune frequency
		self.sink.set_center_freq(options.freq)

		# set gain      
		if options.tx_gain is None:
			# if no gain was specified, use the mid-point in dB
			g = self.sink.get_gain_range()
			options.tx_gain = float(g.start()+g.stop())/2
		self.sink.set_gain(options.tx_gain)


if __name__=='__main__':
	try:
		usrp_dab_tx().run()
	except KeyboardInterrupt:
		pass



