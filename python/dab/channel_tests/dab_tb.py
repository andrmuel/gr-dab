#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
Complete DAB TX and RX with a software channel to simulate noise, frequency offset, etc.
"""

from gnuradio import gr, blks2
import gnuradio.dab as grdab
import math, random

DAB_SAMPLE_RATE=2048000

class dab_ofdm_testbench(gr.top_block):
	def __init__(self, autocorrect_sample_rate=False, input_filter=True, ber_sink=False):
		gr.top_block.__init__(self)
		self.dp = grdab.dab_parameters(1)
		self.rp = grdab.receiver_parameters(1, softbits=False, input_fft_filter=input_filter, autocorrect_sample_rate=autocorrect_sample_rate, correct_ffe=True, equalize_magnitude=False)
		self.ber_sink = ber_sink
		os.environ['GR_SCHEDULER'] = "STS" # need single threaded scheduler for use with concatenate_signals

	def setup_flowgraph(self, mode, ber_skipbytes=0):
		# parameters
		self.dp.set_mode(mode)
		self.rp.set_mode(mode)
		self.vlen = self.dp.num_carriers/4
		self.ber_skipbytes = ber_skipbytes

		# trigger signals
		frame_trigger = [1]+[0]*(self.dp.symbols_per_frame-2)
		self.frame_start = frame_trigger*(len(self.random_bytes)/(self.vlen*(self.dp.symbols_per_frame-1)))+frame_trigger[0:(len(self.random_bytes)/self.vlen)%(self.dp.symbols_per_frame-1)]

		# sources/sinks
		self.source    = gr.vector_source_b(self.random_bytes, False)
		self.trig      = gr.vector_source_b(self.frame_start, False)
		if self.ber_sink:
			self.sink = grdab.blocks.measure_ber_b()
		else:
			self.sink = gr.vector_sink_b()

		# self.noise_start      = gr.noise_source_c(gr.GR_GAUSSIAN, math.sqrt(2), random.randint(0,10000))
		# self.noise_start_head = gr.head(gr.sizeof_gr_complex, NOISE_SAMPLES_AT_START)
		# self.noise_end        = gr.noise_source_c(gr.GR_GAUSSIAN, math.sqrt(2), random.randint(0,10000))
		# self.noise_end_head   = gr.head(gr.sizeof_gr_complex, NOISE_SAMPLES_AT_END)
		
		# blocks
		self.s2v       = gr.stream_to_vector(gr.sizeof_char, self.vlen)
		self.v2s       = gr.vector_to_stream(gr.sizeof_char, self.vlen)
		if self.ber_sink:
			self.ber_skipbytes0 = gr.skiphead(gr.sizeof_char, self.ber_skipbytes)
			self.ber_skipbytes1 = gr.skiphead(gr.sizeof_char, self.ber_skipbytes+self.dp.bytes_per_frame)
		
		# more blocks (they have state, so better reinitialise them)
		self.mod       = grdab.ofdm_mod(self.dp, debug = False)
		self.rescale   = gr.multiply_const_cc(1)
		self.amp       = gr.multiply_const_cc(1)
		self.channel   = blks2.channel_model(noise_voltage=0, noise_seed=random.randint(0,10000))
		# self.cat       = grdab.concatenate_signals(gr.sizeof_gr_complex)
		self.demod     = grdab.ofdm_demod(self.dp, self.rp, debug = False, verbose = True)

		# connect it all
		if self.ber_sink:
			self.connect(self.source, self.s2v, (self.mod,0), self.rescale, self.amp, self.channel, (self.demod,0), self.v2s, self.ber_skipbytes0, self.sink)
			self.connect(self.source, self.ber_skipbytes1, (self.sink,1))
		else:
			self.connect(self.source, self.s2v, (self.mod,0), self.rescale, self.amp, self.channel, (self.demod,0), self.v2s, self.sink)
		self.connect(self.trig, (self.mod,1))

		# SNR calculation and prober
		self.probe_signal = gr.probe_avg_mag_sqrd_c(0,0.00001)
		self.probe_total  = gr.probe_avg_mag_sqrd_c(0,0.00001)
		self.connect(self.amp, self.probe_signal)
		self.connect(self.channel, self.probe_total)
        	
	def gen_random_bytes(self, num_bytes):
		self.random_bytes = [random.randint(0,255) for i in xrange(0,num_bytes)]
		
	def set_noise_energy(self, noise_energy):
		self.channel.set_noise_voltage(math.sqrt(noise_energy)/math.sqrt(2))

	def set_signal_energy(self, signal_energy):
		self.amp.set_k(math.sqrt(signal_energy))
	
	def set_carrier_frequency_offset(self, freq_offset):
		self.channel.set_frequency_offset(float(freq_offset)/self.dp.sample_rate)

	def set_sampling_frequency_offset(self, ratio):
		self.channel.set_timing_offset(ratio)	

	def set_multipath_taps(self, taps):
		self.channel.set_taps(taps)

	def set_power_correction(self, estimated_energy):
		self.estimated_signal_energy = estimated_energy
		sig_ratio = float(self.dp.num_carriers) / float(self.dp.fft_length) # not all subcarriers are occupied -> must be considered to calculate scale factor
		self.rescale.set_k((1/math.sqrt(self.estimated_signal_energy))*math.sqrt(sig_ratio))

	def rewind_sources(self):
		self.source.rewind()
		self.trig.rewind()
		# self.noise_start_head.rewind()
		# self.noise_end_head.rewind()
		
	def clear_sinks(self):
		self.sink.clear()
	
	def clear_state(self):
		if self.ber_sink:
			self.ber_skipbytes0.rewind()
			self.ber_skipbytes1.rewind()
		# self.cat.reset()
		self.demod.clear_state()

		# TODO some state is still left in the demod block - for now just make a new one
		self.disconnect(self.channel, self.demod)
		self.disconnect((self.demod,0), self.v2s)
		self.demod = grdab.ofdm_demod(self.dp, self.rp, debug = False, verbose = True)
		self.connect(self.channel, self.demod)
		self.connect((self.demod,0), self.v2s)
