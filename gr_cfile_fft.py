#!/usr/bin/env python
# _*_ coding: utf8 _*_

# gr_cfile_fft.py - show complex samples in a real time fft
#
# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions


from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.wxgui import stdgui2, fftsink2
from optparse import OptionParser
import wx

class gr_cfile_fft(stdgui2.std_top_block):
	def __init__(self, frame, panel, vbox, argv):
		stdgui2.std_top_block.__init__(self, frame, panel, vbox, argv)
        	
		usage = "%prog: [options] samples_file"
		parser = OptionParser(option_class=eng_option, usage=usage)
		parser.add_option("-r", "--sample_rate", type="int", default=2.048e6, help="throttle to sample rate RATE", metavar="RATE")
        	(options, args) = parser.parse_args ()
		
        	if len(args) != 1:
	            parser.print_help()
        	    raise SystemExit, 1
	
		filename = args[0]
		
		self.src = gr.file_source(gr.sizeof_gr_complex, filename, False)
		self.throttle = gr.throttle(gr.sizeof_gr_complex, options.sample_rate)
		self.fftsink = fftsink2.fft_sink_c (panel, fft_size=1024, sample_rate=options.sample_rate) 

		# gui
		vbox.Add(self.fftsink.win, 1, wx.EXPAND)

		# connect blocks
		self.connect(self.src, self.throttle, self.fftsink)

if __name__=='__main__':
	app = stdgui2.stdapp(gr_cfile_fft, "cfile samples FFT")
	app.MainLoop()
