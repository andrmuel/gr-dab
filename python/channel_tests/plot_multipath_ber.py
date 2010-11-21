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

NUM_BYTES = 500000

MODES=[1,2,3,4]
MODES=[1]
ECHO_MAGNITUDE_RANGE = [0.5]
ECHO_MAGNITUDE_RANGE = [1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2]
ECHO_DELAY_RANGE = range(50,401,10)
ECHO_DELAY_RANGE = range(50,1001,50)

PLOT_FORMAT=['-','-x','--x','-.x',':x']

# initialise test flowgraph
tb = dab_tb.dab_ofdm_testbench(ber_sink=True)
tb.gen_random_bytes(NUM_BYTES)

# prepeare plot	
pylab.xlabel("Echo delay [samples]")
pylab.ylabel("BER")

# open logfile
logfile = open("multipath_ber_log.txt",'w')
logfile.write("number of bytes: " + str(NUM_BYTES) + "\nEcho magnitude range: " + str(ECHO_MAGNITUDE_RANGE) + "\nEcho delay range: " + str(ECHO_DELAY_RANGE) + "\n\n")

for mode in MODES:
	print "Mode: "+str(mode)+"\n-------\n"
	tb.setup_flowgraph(mode)
	# estimate signal energy for this mode (disturbed by FFT ...)
	tb.set_signal_energy(1)
	tb.set_noise_energy(0)
	tb.run()
	tb.set_power_correction(tb.probe_signal.level())
	print "estimated energy: " + str(tb.probe_signal.level()) + "\n"
	for magnitude in ECHO_MAGNITUDE_RANGE:
		ber_values = []
		bytes_received = []
		for delay in ECHO_DELAY_RANGE:
			print "Mode: "+str(mode)+" Echo magnitude: "+str(magnitude)+" Echo delay: "+str(delay)
			# reset and run the test
			tb.rewind_sources()
			tb.clear_sinks()
			tb.clear_state()
			tb.set_multipath_taps([1]+[0]*(delay-1)+[magnitude])
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
			      "Echo Magnitude: "+str(magnitude)+"\n\n"+
			      "Echo delay: BER (number of bytes received)\n" +
			      "-----------------------------------\n")
		for i in range(0,len(ECHO_DELAY_RANGE)):
			logfile.write(str(ECHO_DELAY_RANGE[i])+": "+str(ber_values[i])+" (" + str(bytes_received[i]) + ")\n")
		logfile.write("\n\n")
		# plot it:
		if sum([abs(x) for x in ber_values])==0:
			print "all BER values are 0 - not plotting"
		else:
			# pylab.semilogy(ECHO_DELAY_RANGE, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode)+" Mag "+str(magnitude))
			pylab.semilogy(ECHO_DELAY_RANGE, ber_values, PLOT_FORMAT[mode], label=str(magnitude))
			# pylab.plot(ECHO_DELAY_RANGE, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode)+" Magnitude: "+str(magnitude))

logfile.close()
# pylab.axis([ECHO_MAGNITUDE_RANGE[0],ECHO_MAGNITUDE_RANGE[-1],0,0.52])
pylab.legend(loc="upper left")
pylab.show()
