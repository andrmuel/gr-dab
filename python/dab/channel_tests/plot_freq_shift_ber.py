#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
Simulate channel with frequency offset
"""

import math, random, pylab
import dab_tb, ber

NUM_BYTES = 1000000

MODES=[1,2,3,4]
FREQ_OFFSET_RANGE = range(-300000,300000,10000)
FREQ_OFFSET_RANGE = range(0,1000,100)

PLOT_FORMAT=['-','-x','--x','-.x',':x']

# initialise test flowgraph
tb = dab_tb.dab_ofdm_testbench(ber_sink=True)
tb.gen_random_bytes(NUM_BYTES)

# prepeare plot	
#pylab.title("BER in channel with frequency shift") # add caption in LaTeX -> looks better
pylab.xlabel("Frequency shift [Hz]")
pylab.ylabel("BER")

# open logfile
logfile = open("freq_shift_ber_log.txt",'w')
logfile.write("number of bytes: " + str(NUM_BYTES) + "\nFrequency shift range: " + str(FREQ_OFFSET_RANGE) + "\n\n")

for mode in MODES:
	print "Mode: "+str(mode)+"\n-------\n"
	tb.setup_flowgraph(mode)
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
		bytes_received.append(tb.sink.bytecount())
		print "bytes sent: " + str(NUM_BYTES)
		print "bytes received: " + str(tb.sink.bytecount())
		ber_values.append(tb.sink.ber())
		print "BER: " + str(ber_values[-1])
		print

	# write log
	logfile.write("Mode: " + str(mode)+"\n" +
		      "=======\n\n" +
		      "Frequency shift: BER (number of bytes received)\n" +
		      "-----------------------------------\n")
	for i in range(0,len(FREQ_OFFSET_RANGE)):
		logfile.write(str(FREQ_OFFSET_RANGE[i])+": "+str(ber_values[i])+" (" + str(bytes_received[i]) + ")\n")
	logfile.write("\n\n")
	# plot it:
	if sum([abs(x) for x in ber_values])==0:
		print "all BER values are 0 - not plotting"
	else:
		pylab.semilogy(FREQ_OFFSET_RANGE, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))
		# pylab.plot(FREQ_OFFSET_RANGE, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))

logfile.close()
# pylab.axis([FREQ_OFFSET_RANGE[0],FREQ_OFFSET_RANGE[-1],0,0.52])
pylab.legend()
pylab.show()
