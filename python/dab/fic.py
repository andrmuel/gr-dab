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

from gnuradio import gr, trellis, blocks, digital
from . import dab_python as grdab
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

    def __init__(self, dab_params, verbose=False, debug=False):
        """
        Hierarchical block for FIC decoding

        @param dab_params DAB parameter object (grdab.parameters.dab_parameters)
        """
        gr.hier_block2.__init__(self, "fic",
                                gr.io_signature(1, 1, gr.sizeof_float * dab_params.num_carriers * 2),
                                gr.io_signature(1, 1, gr.sizeof_char * 32))

        self.dp = dab_params
        self.verbose = verbose
        self.debug = debug

        # FIB selection and block partitioning
        self.select_fic_syms = grdab.select_vectors(gr.sizeof_float, self.dp.num_carriers * 2, self.dp.num_fic_syms, 0)
        self.repartition_fic = grdab.repartition_vectors(gr.sizeof_float, self.dp.num_carriers * 2,
                                                       self.dp.fic_punctured_codeword_length, self.dp.num_fic_syms,
                                                       self.dp.num_cifs)

        # unpuncturing
        self.unpuncture = grdab.unpuncture_vff(self.dp.assembled_fic_puncturing_sequence, 0)

        # convolutional coding
        # self.fsm = trellis.fsm(self.dp.conv_code_in_bits, self.dp.conv_code_out_bits, self.dp.conv_code_generator_polynomials)
        self.fsm = trellis.fsm(1, 4, [0o133, 0o171, 0o145, 0o133])  # OK (dumped to text and verified partially)
        self.conv_v2s = blocks.vector_to_stream(gr.sizeof_float, self.dp.fic_conv_codeword_length)
        # self.conv_decode = trellis.viterbi_combined_fb(self.fsm, 20, 0, 0, 1, [1./sqrt(2),-1/sqrt(2)] , trellis.TRELLIS_EUCLIDEAN)
        table = [
            0, 0, 0, 0,
            0, 0, 0, 1,
            0, 0, 1, 0,
            0, 0, 1, 1,
            0, 1, 0, 0,
            0, 1, 0, 1,
            0, 1, 1, 0,
            0, 1, 1, 1,
            1, 0, 0, 0,
            1, 0, 0, 1,
            1, 0, 1, 0,
            1, 0, 1, 1,
            1, 1, 0, 0,
            1, 1, 0, 1,
            1, 1, 1, 0,
            1, 1, 1, 1
        ]
        assert (len(table) / 4 == self.fsm.O())
        table = [(1 - 2 * x) / sqrt(2) for x in table]
        self.conv_decode = trellis.viterbi_combined_fb(self.fsm, 774, 0, 0, 4, table, digital.TRELLIS_EUCLIDEAN)
        #self.conv_s2v = blocks.stream_to_vector(gr.sizeof_char, 774)
        self.conv_prune = grdab.prune(gr.sizeof_char, self.dp.fic_conv_codeword_length // 4, 0,
                                            self.dp.conv_code_add_bits_input)

        # energy dispersal
        self.prbs_src = blocks.vector_source_b(self.dp.prbs(self.dp.energy_dispersal_fic_vector_length), True)
        #self.energy_v2s = blocks.vector_to_stream(gr.sizeof_char, self.dp.energy_dispersal_fic_vector_length)
        self.add_mod_2 = blocks.xor_bb()
        self.energy_s2v = blocks.stream_to_vector(gr.sizeof_char, self.dp.energy_dispersal_fic_vector_length)
        self.cut_into_fibs = grdab.repartition_vectors(gr.sizeof_char, self.dp.energy_dispersal_fic_vector_length,
                                                     self.dp.fib_bits, 1, self.dp.energy_dispersal_fic_fibs_per_vector)

        # connect all
        self.nullsink = blocks.null_sink(gr.sizeof_char)
        self.pack = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.fibout = blocks.stream_to_vector(1, 32)
        # self.filesink = gr.file_sink(gr.sizeof_char, "debug/fic.dat")
        self.fibsink = grdab.fib_sink_vb()

        # self.connect((self,0), (self.select_fic_syms,0), (self.repartition_fic,0), self.unpuncture, self.conv_v2s, self.conv_decode, self.conv_s2v, self.conv_prune, self.energy_v2s, self.add_mod_2, self.energy_s2v, (self.cut_into_fibs,0), gr.vector_to_stream(1,256), gr.unpacked_to_packed_bb(1,gr.GR_MSB_FIRST), self.filesink)
        self.connect((self, 0),
                     (self.select_fic_syms, 0),
                     (self.repartition_fic, 0),
                     self.unpuncture,
                     self.conv_v2s,
                     self.conv_decode,
                     #self.conv_s2v,
                     self.conv_prune,
                     #self.energy_v2s,
                     self.add_mod_2,
                     self.energy_s2v,
                     (self.cut_into_fibs, 0),
                     blocks.vector_to_stream(1, 256),
                     self.pack,
                     self.fibout,
                     self.fibsink)
        self.connect(self.fibout, self)
        self.connect(self.prbs_src, (self.add_mod_2, 1))

        if self.debug:
            self.connect((self, 0), blocks.file_sink(gr.sizeof_float * self.dp.num_carriers * 2, "debug/transmission_frame.dat"))
            self.connect((self, 1), blocks.file_sink(gr.sizeof_char, "debug/transmission_frame_trigger.dat"))
            self.connect(self.select_fic_syms, blocks.file_sink(gr.sizeof_float * self.dp.num_carriers * 2, "debug/fic_select_syms.dat"))
            self.connect(self.repartition_fic, blocks.file_sink(gr.sizeof_float * self.dp.fic_punctured_codeword_length, "debug/fic_repartitioned.dat"))
            self.connect(self.unpuncture, blocks.file_sink(gr.sizeof_float * self.dp.fic_conv_codeword_length, "debug/fic_unpunctured.dat"))
            self.connect(self.conv_decode, blocks.file_sink(gr.sizeof_char, "debug/fic_decoded.dat"))
            self.connect(self.conv_prune, blocks.file_sink(gr.sizeof_char, "debug/fic_decoded_pruned.dat"))
            #self.connect(self.conv_decode, blocks.file_sink(gr.sizeof_char * self.dp.energy_dispersal_fic_vector_length, "debug/fic_energy_dispersal_undone.dat"))
            self.connect(self.pack, blocks.file_sink(gr.sizeof_char, "debug/fic_energy_undone.dat"))

    def get_ensemble_info(self):
        return self.fibsink.get_ensemble_info()

    def get_service_info(self):
        return self.fibsink.get_service_info()

    def get_service_labels(self):
        return self.fibsink.get_service_labels()

    def get_subch_info(self):
        return self.fibsink.get_subch_info()

    def get_programme_type(self):
        return self.fibsink.get_programme_type()

    def get_crc_passed(self):
        return self.fibsink.get_crc_passed()

    def set_print_channel_info(self, val):
        self.fibsink.set_print_channel_info(val)
