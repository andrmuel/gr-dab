#!/usr/bin/env python2
# -*- coding: utf8 -*-

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
receive DAB with USRP
"""

from gnuradio import gr, uhd, blocks
from gnuradio import audio
import gnuradio.dab as grdab
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import sys, time, threading, math

class usrp_dab_rx(gr.top_block):
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
		parser.add_option("-R", "--rx-subdev-spec", type="subdev", default=(0, 0),
		     help="select USRP Rx side A or B [default=A]")
		parser.add_option("-f", "--freq", type="eng_float", default=227.36e6,
		     help="set frequency to FREQ [default=%default]")
		parser.add_option("-d", "--decim", type="intx", default=32,
		     help="set decimation rate to DECIM [default=%default]")
		parser.add_option("-g", "--rx-gain", type="eng_float", default=None,
		     help="set receive gain in dB (default is midpoint)")
		parser.add_option('-v', '--verbose', action="store_true", default=False,
		     help="verbose output")
		parser.add_option('-a', '--antenna', type="string", default="TX/RX",
		     help="select antenna")
        	(options, args) = parser.parse_args ()

		# if len(args)!=1:
			# parser.print_help()
			# sys.exit(1)
		# else:
			# self.filename = args[0]

		# if gr.enable_realtime_scheduling() != gr.RT_OK:
		#       print "-> failed to enable realtime scheduling"

		self.verbose = options.verbose

		self.src = uhd.usrp_source("",uhd.io_type.COMPLEX_FLOAT32,1)
        	#self.src.set_mux(usrp.determine_rx_mux_value(self.src, options.rx_subdev_spec))
        	#self.subdev = uhd.selected_subdev(self.src, options.rx_subdev_spec)
        	#print "--> using RX dboard " + self.subdev.side_and_name()
		
		self.sample_rate = 2e6#self.src.adc_rate()/options.decim
		self.src.set_samp_rate(self.sample_rate)
		self.src.set_antenna(options.antenna)
		self.dab_params = grdab.parameters.dab_parameters(mode=options.dab_mode, sample_rate=self.sample_rate, verbose=options.verbose)
		self.rx_params = grdab.parameters.receiver_parameters(mode=options.dab_mode, softbits=True, input_fft_filter=options.filter_input, autocorrect_sample_rate=options.autocorrect_sample_rate, sample_rate_correction_factor=options.resample_fixed, verbose=options.verbose, correct_ffe=options.correct_ffe, equalize_magnitude=options.equalize_magnitude)

		self.demod = grdab.ofdm_demod(self.dab_params, self.rx_params, verbose=options.verbose) 

		# self.sink = gr.file_sink(gr.sizeof_char*384, self.filename)
		# self.trigsink = gr.null_sink(gr.sizeof_char)
		# self.connect(self.src, self.demod, self.sink)
		# self.connect((self.demod,1), self.trigsink)
		
		self.fic_dec = grdab.fic_decode(self.dab_params)
		self.connect(self.src, self.demod, self.fic_dec)

		# add MSC chain
		self.dabplus = grdab.dabplus_audio_decoder_ff(self.dab_params, 112, 54, 84, 2, True)
		self.audio = audio.sink(32000)
		self.connect(self.demod, self.dabplus)
		# left stereo channel
		self.connect((self.dabplus, 0), (self.audio, 0))
		# right stereo channel
		self.connect((self.dabplus, 1), (self.audio, 1))		


		# tune frequency
		self.frequency = options.freq
		self.set_freq(options.freq)

		# set gain      
		if options.rx_gain is None:
			# if no gain was specified, use the mid-point in dB
			g = self.src.get_gain_range()
			options.rx_gain = float(g.start()+g.stop())/2
		self.src.set_gain(options.rx_gain)
		#self.subdev.set_gain(options.rx_gain)

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
		if self.src.set_center_freq(freq): #src.tune(0, self.subdev, freq):
			if self.verbose:
				print "--> retuned to " + str(freq) + " Hz"
			return True
		else:
			print "-> error - cannot tune to " + str(freq) + " Hz"
			return False
        
if __name__=='__main__':
	try:
		rx = usrp_dab_rx()
		rx.run()
	except KeyboardInterrupt:
		pass



