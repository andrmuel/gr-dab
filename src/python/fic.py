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
	
	def __init__(self, dab_params, verbose=True):
		"""
		Hierarchical block for FIC decoding
		
		@param dab_params DAB parameter object (dab.parameters.dab_parameters)
		"""
		gr.hier_block2.__init__(self,"fic",
					gr.io_signature2(2, 2, gr.sizeof_char*dab_params.num_carriers/4, gr.sizeof_char), # input
					gr.io_signature(0, 0, 0)) # output signature

		self.dp = dab_params
		self.verbose = verbose
		
		
		# FIB selection and block partitioning
		self.select_fics = dab_swig.select_vectors(gr.sizeof_float, self.dp.num_carriers*2, self.dp.num_fic_syms, 0)
		self.repartition_fic = dab_swig.repartition_vectors(self.dp.num_carriers*2, self.dp.fic_punctured_codeword_length, self.dp.num_fic_syms, self.dp.num_cifs)

		# unpuncturing
		self.unpuncture = dab_swig.unpuncture_vbb(self.dp.assembled_fic_puncturing_sequence)

		# convolutional coding
		self.fsm = trellis.fsm(self.dp.conv_code_in_bits, self.dp.conv_code_out_bits, self.dp.conv_code_generator_polynomials)
		self.conv_decode = trellis.viterbi_combined_fb(self.fsm, ?, 0, 0, 1, [1,-1] , trellis.TRELLIS_EUCLIDEAN)

		# energy dispersal
		self.prbs_src   = gr.vector_source_b(self.dp.prbs(self.dp.energy_dispersal_fic_vector_length), repeat=True)
		self.energy_v2s = gr.stream_to_vector(self.dp.energy_dispersal_fic_vector_length)
		self.add_mod_2  = gr.xor_bb()
		self.energy_s2v = gr.stream_to_vector(self.dp.energy_dispersal_fic_vector_length)
		self.cut_into_fibs = dab_swig.block_partitioning_vbb(self.dp.energy_dispersal_fic_vector_length, self.dp.fib_bits, 1, self.dp.energy_dispersal_fic_fibs_per_vector)
		
		
		# connect all
		self.nullsink = gr.null_sink(gr.sizeof_char)
		self.filesink = gr.file_sink(gr.sizeof_char, "debug/fic.dat")
		
		self.connect((self,0), (self.select_fic_syms,0), (self.repartition_fic,0), self.unpuncture, self.conv_decode, self.energy_v2s, self.add_mod_2, self.energy_s2v, (self.cut_into_fibs,0), self.filesink)
		self.connect(self.prbs_src, (self.add_mod_2,1))
		self.connect((self,1), (self.select_fic_syms,1), (self.repartition_fic,1), (self.cut_into_fibs,1), self.nullsink)


