#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
Simulate noise channel to evaluate BER vs SNR
"""

import math, random, pylab
import dab_tb, ber

NUM_BYTES = 1000000

MODES=[1,2,3,4]
SNR_DB = range(-5,21)

PLOT_FORMAT=['-','-x','--x','-.x',':x']

# initialise test flowgraph
tb = dab_tb.dab_ofdm_testbench()
tb.gen_random_bytes(NUM_BYTES)

# prepeare plot	
#pylab.title("BER in noisy channel") # add caption in LaTeX -> looks better
pylab.xlabel("SNR [dB]")
pylab.ylabel("BER")

# open logfile
logfile = open("snr_ber_log.txt",'w')
logfile.write("number of bytes: " + str(NUM_BYTES) + "\nSNR range: " + str(SNR_DB) + "\n\n")

for mode in MODES:
	print "\nMode: "+str(mode)+"\n-------\n"
	tb.setup_flowgraph(mode)
	ber_values = []
	bytes_received = []
	# estimate signal energy for this mode (disturbed by FFT ...)
	tb.set_signal_energy(1)
	tb.set_noise_energy(0)
	tb.run()
	
	tb.set_power_correction(tb.probe_signal.level())
	print "estimated energy: " + str(tb.probe_signal.level()) + "\n"
	for snr_db in SNR_DB:
		print "\nMode: "+str(mode)+" SNR: "+str(snr_db)
		# reset and run the test
		tb.rewind_sources()
		tb.clear_sinks()
		tb.clear_state()
		tb.set_signal_energy(math.pow(10,snr_db/10.))
		tb.set_noise_energy(1)
		tb.run()
		print "signal power: " + str(tb.probe_signal.level())
		print "total power: " + str(tb.probe_total.level())
		# get the result
		result = tb.sink.data()
		expected_result = tb.random_bytes[tb.dp.bytes_per_frame:]
		bytes_received.append(len(result))
		print "bytes sent: " + str(NUM_BYTES)
		print "bytes received: " + str(len(result))
		# calculate bit error rate
		ber_values.append(ber.find_ber(expected_result,result))
		print "BER: " + str(ber_values[-1])
		print "Phase - sqrt(var): " + str(math.sqrt(tb.demod.probe_phase_var.level()))

	# write log
	logfile.write("Mode: " + str(mode)+"\n" +
		      "=======\n\n" +
		      "SNR: BER (number of bytes received)\n" +
		      "-----------------------------------\n")
	for i in range(0,len(SNR_DB)):
		logfile.write(str(SNR_DB[i])+": "+str(ber_values[i])+" (" + str(bytes_received[i]) + ")\n")
	logfile.write("\n\n")
	# plot it:
	if sum([abs(x) for x in ber_values])==0:
		print "all BER values are 0 - not plotting"
	else:
		pylab.semilogy(SNR_DB, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))
		# pylab.plot(SNR_DB, ber_values, PLOT_FORMAT[mode], label="Mode "+str(mode))

logfile.close()
# pylab.axis([SNR_DB[0],SNR_DB[-1],0,0.52])
pylab.legend()
pylab.show()
