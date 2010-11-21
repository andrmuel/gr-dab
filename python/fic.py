#!/usr/bin/env python
#
# Copyright 2008 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

# Andreas Mueller, 2008
# andrmuel@ee.ethz.ch

from gnuradio import gr, trellis
import dab_swig
from math import sqrt

"""
DAB FIC layer
"""

class fic_decode(gr.hier_block2):
	"""
	@brief block to decode FIBs (fast information blocks) from the FIC (fast information channel) of a demodulated DAB signal

	- get FIBs from byte stream
	- do convolutional decoding
	- undo energy dispersal
	- get FIC information
	"""
	
	def __init__(self, dab_params, verbose=True, debug=False):
		"""
		Hierarchical block for FIC decoding
		
		@param dab_params DAB parameter object (dab.parameters.dab_parameters)
		"""
		gr.hier_block2.__init__(self,"fic",
					gr.io_signature2(2, 2, gr.sizeof_float*dab_params.num_carriers*2, gr.sizeof_char), # input
					gr.io_signature(0, 0, 0)) # output signature

		self.dp = dab_params
		self.verbose = verbose
		self.debug = debug
		
		
		# FIB selection and block partitioning
		self.select_fic_syms = dab_swig.select_vectors(gr.sizeof_float, self.dp.num_carriers*2, self.dp.num_fic_syms, 0)
		self.repartition_fic = dab_swig.repartition_vectors(gr.sizeof_float, self.dp.num_carriers*2, self.dp.fic_punctured_codeword_length, self.dp.num_fic_syms, self.dp.num_cifs)

		# unpuncturing
		self.unpuncture = dab_swig.unpuncture_vff(self.dp.assembled_fic_puncturing_sequence)

		# convolutional coding
		# self.fsm = trellis.fsm(self.dp.conv_code_in_bits, self.dp.conv_code_out_bits, self.dp.conv_code_generator_polynomials)
		self.fsm = trellis.fsm(1, 4, [0133, 0171, 0145, 0133]) # OK (dumped to text and verified partially)
		self.conv_v2s = gr.vector_to_stream(gr.sizeof_float, self.dp.fic_conv_codeword_length)
		# self.conv_decode = trellis.viterbi_combined_fb(self.fsm, 20, 0, 0, 1, [1./sqrt(2),-1/sqrt(2)] , trellis.TRELLIS_EUCLIDEAN)
		table = [ 
			  0,0,0,0,
			  0,0,0,1,
			  0,0,1,0,
			  0,0,1,1,
			  0,1,0,0,
			  0,1,0,1,
			  0,1,1,0,
			  0,1,1,1,
			  1,0,0,0,
			  1,0,0,1,
			  1,0,1,0,
			  1,0,1,1,
			  1,1,0,0,
			  1,1,0,1,
			  1,1,1,0,
			  1,1,1,1
			]
		assert(len(table)/4==self.fsm.O())
		table = [(1-2*x)/sqrt(2) for x in table]
		self.conv_decode = trellis.viterbi_combined_fb(self.fsm, 774, 0, 0, 4, table, trellis.TRELLIS_EUCLIDEAN)
		self.conv_s2v = gr.stream_to_vector(gr.sizeof_char, 774)
		self.conv_prune = dab_swig.prune_vectors(gr.sizeof_char, self.dp.fic_conv_codeword_length/4, 0, self.dp.conv_code_add_bits_input)

		# energy dispersal
		self.prbs_src   = gr.vector_source_b(self.dp.prbs(self.dp.energy_dispersal_fic_vector_length), True)
		self.energy_v2s = gr.vector_to_stream(gr.sizeof_char, self.dp.energy_dispersal_fic_vector_length)
		self.add_mod_2  = gr.xor_bb()
		self.energy_s2v = gr.stream_to_vector(gr.sizeof_char, self.dp.energy_dispersal_fic_vector_length)
		self.cut_into_fibs = dab_swig.repartition_vectors(gr.sizeof_char, self.dp.energy_dispersal_fic_vector_length, self.dp.fib_bits, 1, self.dp.energy_dispersal_fic_fibs_per_vector)
		
		# connect all
		self.nullsink = gr.null_sink(gr.sizeof_char)
		# self.filesink = gr.file_sink(gr.sizeof_char, "debug/fic.dat")
		self.fibsink = dab_swig.fib_sink_vb()
		
		# self.connect((self,0), (self.select_fic_syms,0), (self.repartition_fic,0), self.unpuncture, self.conv_v2s, self.conv_decode, self.conv_s2v, self.conv_prune, self.energy_v2s, self.add_mod_2, self.energy_s2v, (self.cut_into_fibs,0), gr.vector_to_stream(1,256), gr.unpacked_to_packed_bb(1,gr.GR_MSB_FIRST), self.filesink)
		self.connect((self,0), (self.select_fic_syms,0), (self.repartition_fic,0), self.unpuncture, self.conv_v2s, self.conv_decode, self.conv_s2v, self.conv_prune, self.energy_v2s, self.add_mod_2, self.energy_s2v, (self.cut_into_fibs,0), gr.vector_to_stream(1,256), gr.unpacked_to_packed_bb(1,gr.GR_MSB_FIRST), gr.stream_to_vector(1,32), self.fibsink)
		self.connect(self.prbs_src, (self.add_mod_2,1))
		self.connect((self,1), (self.select_fic_syms,1), (self.repartition_fic,1), (self.cut_into_fibs,1), self.nullsink)

		if self.debug:
			self.connect(self.select_fic_syms, gr.file_sink(gr.sizeof_float*self.dp.num_carriers*2, "debug/fic_select_syms.dat"))
			self.connect(self.repartition_fic, gr.file_sink(gr.sizeof_float*self.dp.fic_punctured_codeword_length, "debug/fic_repartitioned.dat"))
			self.connect(self.unpuncture, gr.file_sink(gr.sizeof_float*self.dp.fic_conv_codeword_length, "debug/fic_unpunctured.dat"))
			self.connect(self.conv_decode, gr.file_sink(gr.sizeof_char, "debug/fic_decoded.dat"))
			self.connect(self.energy_s2v, gr.file_sink(gr.sizeof_char*self.dp.energy_dispersal_fic_vector_length, "debug/fic_energy_dispersal_undone.dat"))
