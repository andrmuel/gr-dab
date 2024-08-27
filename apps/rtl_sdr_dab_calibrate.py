#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
demodulate DAB signal and use it for calibration purposes
"""

from gnuradio import gr, blocks
import osmosdr
from gnuradio.eng_option import eng_option
import gnuradio.dab as grdab
from optparse import OptionParser
import sys, threading, time

class rtl_sdr_dab_cal(gr.top_block):
	def __init__(self):
		gr.top_block.__init__(self)

		parser = OptionParser(option_class=eng_option, usage="%prog: [options] <filename>")
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
		parser.add_option("-r", "--sample-rate", type="int", default=2000000,
			help="set sample rate to SAMPLE_RATE [default=%default]")
		parser.add_option("-d", "--decim", type="intx", default=32,
			help="set decimation rate to DECIM [default=%default]")
		parser.add_option("-g", "--rx-gain", type="eng_float", default=None,
			help="set receive gain in dB (default is midpoint)")
		parser.add_option('-v', '--verbose', action="store_true", default=False,
			help="verbose output")
		(options, args) = parser.parse_args()

		
		self.verbose = options.verbose
		self.sample_rate = options.sample_rate

		if len(args) == 0:
			if self.verbose:
				print "--> receiving from USRP"
			self.src = osmosdr.source()
			self.src.set_sample_rate(self.sample_rate)
			self.src.set_freq_corr(0)
			# tune frequency
			self.frequency = options.freq
			self.orig_frequency = options.freq
			self.set_freq(options.freq)

			self.src.set_freq_corr(0)

			# set gain 
			if options.rx_gain is None:
				# if no gain was specified, use AGC
				self.src.set_gain_mode(True, 0)
			else:
				self.src.set_gain(options.rx_gain, 0)

		else:
			if self.verbose:
				print "--> receiving from file: " + args[0]
			self.filename = args[0]
			self.src = blocks.file_source(gr.sizeof_gr_complex, self.filename, False)
		
		
		self.dab_params = grdab.parameters.dab_parameters(mode=options.dab_mode, sample_rate=self.sample_rate, verbose=options.verbose)
		self.rx_params = grdab.parameters.receiver_parameters(mode=options.dab_mode, softbits=True, input_fft_filter=options.filter_input, 			autocorrect_sample_rate=options.autocorrect_sample_rate, sample_rate_correction_factor=options.resample_fixed, verbose=options.verbose, correct_ffe=options.correct_ffe, equalize_magnitude=options.equalize_magnitude)

		self.demod = grdab.ofdm_demod(self.dab_params, self.rx_params, verbose=self.verbose) 

		self.v2s = blocks.vector_to_stream(gr.sizeof_gr_complex, self.dab_params.num_carriers)

		self.sink = blocks.null_sink(gr.sizeof_float*self.dab_params.num_carriers*2)

		self.connect(self.src, self.demod, self.sink)

		# retune USRP to correct FFE?
		self.correct_ffe_usrp = options.correct_ffe_usrp
		if self.correct_ffe_usrp:
			print "--> correcting FFE on USRP"
			self.run_correct_ffe_thread = True
			self.ffe_updater = threading.Timer(0.1, self.correct_ffe)
			self.ffe_updater.setDaemon(True)
			self.ffe_updater.start()

	def correct_ffe(self):
		while self.run_correct_ffe_thread:
			carrier_offs = self.demod.cfs.get_delta_f() * 1000
			diff = self.demod.sync.ffe.ffe_estimate()
			error_hz = diff-carrier_offs
			error_ppm = (((self.orig_frequency-self.frequency)-error_hz) / self.frequency) * 1000000
			print "abs err: " + str(error_ppm) + " ppm\tsoft err: " + str(error_hz) + " Hz\tcarr: " + str(carrier_offs/1000)
			if abs(error_hz) > 500:
				self.frequency -= error_hz
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
		rx = rtl_sdr_dab_cal()
		rx.run()
	except KeyboardInterrupt:
		pass

