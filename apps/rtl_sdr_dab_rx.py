#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
receive DAB with USRP
"""

from gnuradio import gr, blocks
import osmosdr
from gnuradio.eng_option import eng_option
import gnuradio.dab as grdab
from optparse import OptionParser
import sys, time, threading, math

class rtl_sdr_dab_rx(gr.top_block):
	def __init__(self):
		gr.top_block.__init__(self)
        
		
		parser = OptionParser(option_class=eng_option, usage="%prog: [options] output-filename")
  		parser.add_option("-m", "--dab-mode", type="int", default=1,
        	     	help="DAB mode [default=%default]")
		parser.add_option("-F", "--filter-input", action="store_true", default=False,
                          help="Enable FFT filter at input")
		parser.add_option('-c', '--correct-ffe', action="store_true", default=False,
		     help="do fine frequency correction")
		parser.add_option('-u', '--correct-ffe-usrp', action="store_true", default=False,
		     help="do fine frequency correction by retuning the USRP instead of in software")
		parser.add_option('-e', '--equalize-magnitude', action="store_true", default=False,
		     help="do magnitude equalization")
  		parser.add_option("-s", "--resample-fixed", type="eng_float", default=1,
			help="resample by a fixed factor (fractional interpolation)")
		parser.add_option("-S", "--autocorrect-sample-rate", action="store_true", default=False,
                          help="Estimate sample rate offset and resample (dynamic fractional interpolation)")
		parser.add_option("-f", "--freq", type="eng_float", default=227.36e6,
		     help="set frequency to FREQ [default=%default]")
		parser.add_option("-p", "--ppm", type="int", default=0,
		     help="set frequency correction in ppm [default=%default]")
		parser.add_option("-r", "--sample-rate", type="int", default=2000000,
		     help="set sample rate to SAMPLE_RATE [default=%default]")
		parser.add_option("-g", "--rx-gain", type="eng_float", default=None,
		     help="set receive gain in dB (default is midpoint)")
		parser.add_option('-v', '--verbose', action="store_true", default=False,
		     help="verbose output")
        	(options, args) = parser.parse_args ()

		# if len(args)!=1:
			# parser.print_help()
			# sys.exit(1)
		# else:
			# self.filename = args[0]

		# if gr.enable_realtime_scheduling() != gr.RT_OK:
		#       print "-> failed to enable realtime scheduling"

		self.verbose = options.verbose

		self.sample_rate = sample_rate = options.sample_rate

		self.src = osmosdr.source()
		self.src.set_sample_rate(sample_rate)
		#self.src.set_center_freq(209.936e6, 0)
		self.src.set_freq_corr(options.ppm)
		self.src.set_gain_mode(True, 0)
		self.src.set_gain(0, 0)

		self.dab_params = grdab.parameters.dab_parameters(
                        mode=options.dab_mode,
                        sample_rate=self.sample_rate,
                        verbose=options.verbose
                        )
		self.rx_params = grdab.parameters.receiver_parameters(
                        mode=options.dab_mode,
                        softbits=True,
                        input_fft_filter=options.filter_input,
                        autocorrect_sample_rate=options.autocorrect_sample_rate,
                        sample_rate_correction_factor=options.resample_fixed,
                        verbose=options.verbose,
                        correct_ffe=options.correct_ffe,
                        equalize_magnitude=options.equalize_magnitude
                        )

		self.demod = grdab.ofdm_demod(self.dab_params, self.rx_params, verbose=options.verbose) 

                if len(args) >= 1:
                        self.filename = args[0]
                        self.sink = blocks.file_sink(gr.sizeof_char*12288, self.filename)
                        #self.sink = gr.file_sink(gr.sizeof_char*3072, self.filename)
                        self.connect(self.demod, self.sink)


		
		self.fic_dec = grdab.fic_decode(self.dab_params)
		self.connect(self.src, self.demod, self.fic_dec)

		# tune frequency
		self.frequency = options.freq
		self.set_freq(options.freq)

		# set gain      
		if options.rx_gain is None:
			# if no gain was specified, use AGC
                        self.src.set_gain_mode(True, 0)
                else:
                        self.src.set_gain(options.rx_gain, 0)

		self.update_ui = options.verbose
		if self.update_ui:
			self.run_ui_update_thread = True
			self.ui_updater = threading.Timer(0.1,self.update_ui_function)
			self.ui_updater.setDaemon(True)
			self.ui_updater.start()

		self.correct_ffe_usrp = options.correct_ffe_usrp
		if self.correct_ffe_usrp:
			print "--> correcting FFE on USRP"
			self.run_correct_ffe_thread = True
			self.ffe_updater = threading.Timer(0.1, self.correct_ffe)
			self.ffe_updater.setDaemon(True)
			self.ffe_updater.start()

	def update_ui_function(self):
		while self.run_ui_update_thread:
			var = self.demod.probe_phase_var.level()
			q = int(50*(math.sqrt(var)/(math.pi/4)))
			print "--> Phase variance: " + str(var) +"\n"
			print "--> Signal quality: " + '='*(50-q) + '>' + '-'*q + "\n"
			time.sleep(0.3)
	
	def correct_ffe(self):
		while self.run_correct_ffe_thread:
			diff = self.demod.sync.ffs_sample_and_average_arg.ffe_estimate()
			if abs(diff) > self.rx_params.usrp_ffc_min_deviation:
				self.frequency -= diff*self.rx_params.usrp_ffc_adapt_factor
				print "--> updating fine frequency correction: " + str(self.frequency)
				self.set_freq(self.frequency)
			time.sleep(1./self.rx_params.usrp_ffc_retune_frequency)

	def set_freq(self, freq):
		if self.src.set_center_freq(freq, 0):
			if self.verbose:
				print "--> retuned to " + str(freq) + " Hz"
			return True
		else:
			print "-> error - cannot tune to " + str(freq) + " Hz"
			return False
        
if __name__=='__main__':
	try:
		rx = rtl_sdr_dab_rx()
		rx.run()
	except KeyboardInterrupt:
		pass



