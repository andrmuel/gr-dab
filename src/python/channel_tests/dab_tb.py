#!/usr/bin/env python
# _*_ coding: utf8 _*_

# Andreas Müller, 2008
# andrmuel@ee.ethz.ch
#
# this code may be freely used under GNU GPL conditions

"""
Complete DAB TX and RX with a software channel to simulate noise, frequency offset, etc.
"""

from gnuradio import gr, blks2, dab
import math, random

NOISE_SAMPLES_AT_START = 100000
NOISE_SAMPLES_AT_END = 100000

class dab_ofdm_testbench(gr.top_block):
	def __init__(self):
		gr.top_block.__init__(self)

	def setup_flowgraph(self, mode):
		# parameters
		self.mode = mode
		self.dp   = dab.dab_parameters(mode)
		self.vlen = self.dp.num_carriers/4

		# trigger signals
		frame_trigger = [1]+[0]*(self.dp.symbols_per_frame-2)
		self.frame_start = frame_trigger*(len(self.random_bytes)/(self.vlen*(self.dp.symbols_per_frame-1)))+frame_trigger[0:(len(self.random_bytes)/self.vlen)%(self.dp.symbols_per_frame-1)]

		# sources/sinks
		self.source    = gr.vector_source_b(self.random_bytes, False)
		self.trig      = gr.vector_source_b(self.frame_start, False)
		self.sink      = gr.vector_sink_b()
		self.trig_sink = gr.null_sink(gr.sizeof_char)

		self.noise_start      = gr.noise_source_c(gr.GR_GAUSSIAN, math.sqrt(2), random.randint(0,10000))
		self.noise_start_head = gr.head(gr.sizeof_gr_complex, NOISE_SAMPLES_AT_START)
		self.noise_end        = gr.noise_source_c(gr.GR_GAUSSIAN, math.sqrt(2), random.randint(0,10000))
		self.noise_end_head   = gr.head(gr.sizeof_gr_complex, NOISE_SAMPLES_AT_END)
		
		# blocks
		self.s2v     = gr.stream_to_vector(gr.sizeof_char, self.vlen)
		self.v2s     = gr.vector_to_stream(gr.sizeof_char, self.vlen)
		
		# more blocks (they have state, so better reinitialise them)
		self.mod     = dab.ofdm_mod(self.mode, debug = False)
		self.rescale = gr.multiply_const_cc(1)
		self.amp     = gr.multiply_const_cc(1)
		self.channel = blks2.channel_model(noise_voltage=0, noise_seed=random.randint(0,10000))
		# self.cat     = dab.concatenate_signals(gr.sizeof_gr_complex)
		self.demod   = dab.ofdm_demod(self.mode, rx_filter = True, autocorrect_sample_rate = False, sample_rate_correction_factor = 1, debug = False, verbose = False)

		# connect it all
		self.connect(self.source, self.s2v, (self.mod,0), self.rescale, self.amp, self.channel, (self.demod,0), self.v2s, self.sink)
		self.connect(self.trig, (self.mod,1))
		self.connect((self.demod, 1), self.trig_sink)

		# SNR calculation and prober
		self.probe_signal = gr.probe_avg_mag_sqrd_c(1,0.00001)
		self.probe_total  = gr.probe_avg_mag_sqrd_c(1,0.00001)
		self.connect(self.amp, self.probe_signal)
		self.connect(self.channel, self.probe_total)
        	
	def gen_random_bytes(self, num_bytes):
		self.random_bytes = [random.randint(0,255) for i in xrange(0,num_bytes)]
		
	def set_noise_energy(self, noise_energy):
		self.channel.set_noise_voltage(math.sqrt(noise_energy)/math.sqrt(2))

	def set_signal_energy(self, signal_energy):
		self.amp.set_k(math.sqrt(signal_energy))
	
	def set_carrier_frequency_offset(self, freq_offset):
		self.channel.set_frequency_offset(freq_offset)

	def set_sampling_frequency_offset(self, ratio):
		self.channel.set_timing_offset(ratio)	

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
		# self.cat.reset()
		self.demod.clear_state()

		# TODO some state is stull left - for now just make a new one
		self.disconnect(self.channel, self.demod)
		self.disconnect((self.demod,0), self.v2s)
		self.disconnect((self.demod,1), self.trig_sink)
		self.demod   = dab.ofdm_demod(self.mode, rx_filter = True, autocorrect_sample_rate = False, sample_rate_correction_factor = 1, debug = False, verbose = False)
		self.connect(self.channel, self.demod)
		self.connect((self.demod,0), self.v2s)
		self.connect((self.demod,1), self.trig_sink)
