#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
Simulate channel with sampling frequency offset
"""

from gnuradio import dab
import math, random, pylab
import dab_tb, ber

NUM_BYTES = 1000000

MODES=[1,2,3,4]
MODES=[1]
RATE_OFFSET = pylab.logspace(pylab.log10(0.999), pylab.log10(1.001), 10)
RATE_OFFSET = pylab.linspace(0.999, 1.001, 100)
RATE_OFFSET = [1.001,1.002]

PLOT_FORMAT=['-','-x','--x','-.x',':x']

if __name__ == '__main__':
	try:
		# initialise test flowgraph
		tb = dab_tb.dab_ofdm_testbench(autocorrect_sample_rate=True, ber_sink=True)
		tb.gen_random_bytes(NUM_BYTES)

		# prepeare plot	
		pylab.xlabel("Sampling frequency offset (ratio)")
		pylab.ylabel("BER")

		# open logfile
		logfile = open("snr_sampling_frequency_offset_log.txt",'w')
		logfile.write("number of bytes: " + str(NUM_BYTES) + "\nRange of sampling rate ratios: " + str(RATE_OFFSET) + "\n\n")

		for mode in MODES:
			print "Mode: "+str(mode)+"\n-------\n"
			dp = dab.dab_parameters(mode)
			tb.setup_flowgraph(mode, ber_skipbytes=5*dp.bytes_per_frame)
			ber_values = []
			bytes_received = []
			# estimate signal energy for this mode (disturbed by FFT ...)
			tb.set_signal_energy(1)
			tb.set_noise_energy(0)
			tb.run()
			tb.set_power_correction(tb.probe_signal.level())
			print "estimated energy: " + str(tb.probe_signal.level()) + "\n"
			tb.autocorrect_sample_rate = True
			for offset in RATE_OFFSET:
				print "Mode: "+str(mode)+" Offset: "+str(offset)
				# reset and run the test
				tb.rewind_sources()
				tb.clear_sinks()
				tb.clear_state()
				tb.set_sampling_frequency_offset(offset)
				tb.run()
				print "signal power: " + str(tb.probe_signal.level())
				print "total power: " + str(tb.probe_total.level())
				# get the result
				bytes_received.append(tb.sink.bytecount())
				print "bytes sent: " + str(NUM_BYTES)
				print "bytes received: " + str(tb.sink.bytecount())
				ber_values.append(tb.sink.ber())
				print "BER: " + str(ber_values[-1])
				print
			# write log
			logfile.write("Mode: " + str(mode)+"\n" +
				      "=======\n\n" +
				      "Actual to real sampling frequency ratio: BER (number of bytes received)\n" +
				      "-----------------------------------\n")
			for i in range(0,len(RATE_OFFSET)):
				logfile.write(str(RATE_OFFSET[i])+": "+str(ber_values[i])+" (" + str(bytes_received[i]) + ")\n")
			logfile.write("\n\n")
			# plot it:
			if sum([abs(x) for x in ber_values])==0:
				print "all BER values are 0 - not plotting"
			else:
				pylab.semilogy(RATE_OFFSET, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))
				# pylab.plot(RATE_OFFSET, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))

		logfile.close()
		# pylab.axis([RATE_OFFSET[0],RATE_OFFSET[-1],0,0.52])
		pylab.legend()
		pylab.show()


	except KeyboardInterrupt:
		pass



