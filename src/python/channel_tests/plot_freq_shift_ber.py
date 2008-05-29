#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
Simulate noise channel to evaluate BER vs SNR
"""

from gnuradio import dab
import math, random, pylab
import dab_tb, ber

NUM_BYTES = 1000000
NUM_BYTES = 100000

MODES=[1,2,3,4]
MODES=[1]
FREQ_OFFSET_RANGE = range(0,100000,1000)
FREQ_OFFSET_RANGE = range(0,5000,1000)

PLOT_FORMAT=['-','-x','--x','-.x',':x']

if __name__ == '__main__':
	try:
		# initialise test flowgraph
		tb = dab_tb.dab_ofdm_testbench()
		tb.gen_random_bytes(NUM_BYTES)

		# prepeare plot	
		#pylab.title("BER in channel with frequency shift") # add caption in LaTeX -> looks better
		pylab.xlabel("Frequency shift [Hz]")
		pylab.ylabel("BER")

		# open logfile
		logfile = open("snr_freq_shift_log.txt",'w')
		logfile.write("number of bytes: " + str(NUM_BYTES) + "\nFrequency shift range: " + str(FREQ_OFFSET_RANGE) + "\n\n")

		for mode in MODES:
			print "Mode: "+str(mode)+"\n-------\n"
			tb.setup_flowgraph(mode)
			dp = dab.dab_parameters(mode)
			ber_values = []
			bytes_received = []
			# estimate signal energy for this mode (disturbed by FFT ...)
			tb.set_signal_energy(1)
			tb.set_noise_energy(0)
			tb.run()
			tb.set_power_correction(tb.probe_signal.level())
			print "estimated energy: " + str(tb.probe_signal.level()) + "\n"
			for offset in FREQ_OFFSET_RANGE:
				print "Mode: "+str(mode)+" Offset: "+str(offset)
				# reset and run the test
				tb.rewind_sources()
				tb.clear_sinks()
				tb.clear_state()
				tb.set_carrier_frequency_offset(offset)
				tb.run()
				print "signal power: " + str(tb.probe_signal.level())
				print "total power: " + str(tb.probe_total.level())
				# get the result
				result = tb.sink.data()
				expected_result = tb.random_bytes[dp.bytes_per_frame:]
				bytes_received.append(len(result))
				print "bytes sent: " + str(NUM_BYTES)
				print "bytes received: " + str(len(result))
				# calculate bit error rate
				ber_values.append(ber.find_ber(expected_result,result))
				print "BER: " + str(ber_values[-1])
				print

			# plot it:
			# pylab.semilogy(FREQ_OFFSET_RANGE, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))
			pylab.plot(FREQ_OFFSET_RANGE, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))
			logfile.write("Mode: " + str(mode)+"\n" +
				      "=======\n\n" +
				      "Frequency shift: BER (number of bytes received)\n" +
				      "-----------------------------------\n")
			for i in range(0,len(FREQ_OFFSET_RANGE)):
				logfile.write(str(FREQ_OFFSET_RANGE[i])+": "+str(ber_values[i])+" (" + str(bytes_received[i]) + ")\n")
			logfile.write("\n\n")

		logfile.close()
		# pylab.axis([FREQ_OFFSET_RANGE[0],FREQ_OFFSET_RANGE[-1],0,0.52])
		pylab.legend()
		pylab.show()


	except KeyboardInterrupt:
		pass



