#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
Simulate channel with sampling frequency offset
"""

import math, random, pylab
import dab_tb, ber

NUM_BYTES = 1000000

MODES=[1,2,3,4]
MODES=[1]
SAMPLE_RATE_ERROR = pylab.linspace(0.99, 1.01, 50)

PLOT_FORMAT=['-','-x','--x','-.x',':x']

# initialise test flowgraph
tb = dab_tb.dab_ofdm_testbench(autocorrect_sample_rate=True, ber_sink=True)
tb.gen_random_bytes(NUM_BYTES)

# prepeare plot	
pylab.xlabel("Sampling frequency offset (ratio)")
pylab.ylabel("BER")

# open logfile
logfile = open("sampling_frequency_offset_ber_log.txt",'w')
logfile.write("number of bytes: " + str(NUM_BYTES) + "\nRange of sampling rate ratios: " + str(SAMPLE_RATE_ERROR) + "\n\n")

for mode in MODES:
	print "Mode: "+str(mode)+"\n-------\n"
	tb.setup_flowgraph(mode, ber_skipbytes=5*tb.dp.bytes_per_frame)
	ber_values = []
	bytes_received = []
	# estimate signal energy for this mode (disturbed by FFT ...)
	tb.set_signal_energy(1)
	tb.set_noise_energy(0)
	tb.run()
	tb.demod.stop()
	tb.set_power_correction(tb.probe_signal.level())
	print "estimated energy: " + str(tb.probe_signal.level()) + "\n"
	for ratio in SAMPLE_RATE_ERROR:
		print "Mode: "+str(mode)+" Ratio: "+str(ratio)
		# reset and run the test
		tb.rewind_sources()
		tb.clear_sinks()
		tb.clear_state()
		tb.set_sampling_frequency_offset(1/ratio)
		tb.set_signal_energy(math.pow(10,1.5))
		tb.set_noise_energy(1)
		tb.run()
		tb.demod.stop()
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
	for i in range(0,len(SAMPLE_RATE_ERROR)):
		logfile.write(str(SAMPLE_RATE_ERROR[i])+": "+str(ber_values[i])+" (" + str(bytes_received[i]) + ")\n")
	logfile.write("\n\n")
	# plot it:
	if sum([abs(x) for x in ber_values])==0:
		print "all BER values are 0 - not plotting"
	else:
		pylab.semilogy(SAMPLE_RATE_ERROR, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))
		# pylab.plot(SAMPLE_RATE_ERROR, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))

logfile.close()
# pylab.axis([SAMPLE_RATE_ERROR[0],SAMPLE_RATE_ERROR[-1],0,0.52])
pylab.legend()
pylab.show()
