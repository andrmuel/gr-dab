#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
receive DAB with USRP
"""

from gnuradio import gr, usrp, blks2, dab
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import sys

class usrp_rx_dab(gr.top_block):
	def __init__(self):
		gr.top_block.__init__(self)
        
		
		parser = OptionParser(option_class=eng_option)
		parser.add_option("-R", "--rx-subdev-spec", type="subdev", default=(0, 0),
		     help="select USRP Rx side A or B [default=A]")
		parser.add_option("-f", "--freq", type="eng_float", default=227.36e6,
		     help="set frequency to FREQ [default=%default]")
		parser.add_option("-g", "--rx-gain", type="eng_float", default=None,
		     help="set receive gain in dB (default is midpoint)")
		parser.add_option("-o", "--output-filename", type="string", default="debug/usrp_bytes.raw",
		     help="specify output-filename [default=%default]")
        	(options, args) = parser.parse_args ()
		if len(args)>0:
			parser.print_help()
			sys.exit(1)

		# if gr.enable_realtime_scheduling() != gr.RT_OK:
		#       print "-> failed to enable realtime scheduling"

		decim = 32

		self.dab_params = dab.parameters.dab_parameters(mode=1, sample_rate=2000000, verbose=True)
		self.rx_params = dab.parameters.receiver_parameters(mode=1, sample_rate=2000000, input_fft_filter=False)

		self.src = usrp.source_c(decim_rate=decim)
        	self.src.set_mux(usrp.determine_rx_mux_value(self.src, options.rx_subdev_spec))
        	self.subdev = usrp.selected_subdev(self.src, options.rx_subdev_spec)
        	print "-> using RX dboard " + self.subdev.side_and_name()

		self.sample_rate = self.src.adc_rate()/decim
		print self.sample_rate

		self.demod = dab.ofdm_demod(self.dab_params, self.rx_params, verbose=True) 

		self.sink = gr.file_sink(gr.sizeof_char*384, options.output_filename)

		self.trigsink = gr.null_sink(gr.sizeof_char)

		self.connect(self.src, self.demod, self.sink)
		self.connect((self.demod,1), self.trigsink)

		# tune frequency
		self.src.tune(0, self.subdev, options.freq)

		# set gain      
		if options.rx_gain is None:
			# if no gain was specified, use the mid-point in dB
			g = self.subdev.gain_range()
			options.rx_gain = float(g[0]+g[1])/2
		self.subdev.set_gain(options.rx_gain)

if __name__=='__main__':
	try:
		usrp_rx_dab().run()
	except KeyboardInterrupt:
		pass



