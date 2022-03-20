#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, blocks, trellis
import gnuradio.dab as grdab
from math import sqrt

class msc_decode(gr.hier_block2):
    """
    @brief block to extract and decode a sub-channel out of the MSC (Main Service Channel) of a demodulated transmission frame

    - get MSC from byte stream
    - repartition MSC to CIFs (Common Interleaved Frames)
    - select a subchannel and extraxt it (dump rest of CIF)
    - do time deinterleaving
    - do convolutional decoding
    - undo energy dispersal
    - output data stream of one subchannel (packed bytes)
    """

    def __init__(self, dab_params, address, size, protection, verbose=False, debug=False):
        gr.hier_block2.__init__(self,
                                "msc_decode",
                                # Input signature
                                gr.io_signature(1, 1, gr.sizeof_float * dab_params.num_carriers * 2),
                                # Output signature
                                gr.io_signature(1, 1, gr.sizeof_char))
        self.dp = dab_params
        self.address = address
        self.size = size
        self.protect = protection
        self.verbose = verbose
        self.debug = debug

        # calculate n factor (multiple of 8kbits etc.)
        self.n = self.size / self.dp.subch_size_multiple_n[self.protect]

        # calculate puncturing factors (EEP, table 33, 34)
        self.msc_I = self.n * 192
        if (self.n > 1 or self.protect != 1):
            self.puncturing_L1 = [6 * self.n - 3, 2 * self.n - 3, 6 * self.n - 3, 4 * self.n - 3]
            self.puncturing_L2 = [3, 4 * self.n + 3, 3, 2 * self.n + 3]
            self.puncturing_PI1 = [24, 14, 8, 3]
            self.puncturing_PI2 = [23, 13, 7, 2]
            # calculate length of punctured codeword (11.3.2)
            self.msc_punctured_codeword_length = self.puncturing_L1[self.protect] * 4 * self.dp.puncturing_vectors_ones[
                self.puncturing_PI1[self.protect]] + self.puncturing_L2[self.protect] * 4 * \
                                                     self.dp.puncturing_vectors_ones[
                                                         self.puncturing_PI2[self.protect]] + 12
            self.assembled_msc_puncturing_sequence = int(self.puncturing_L1[self.protect]) * 4 * self.dp.puncturing_vectors[
                self.puncturing_PI1[self.protect]] + int(self.puncturing_L2[self.protect]) * 4 * self.dp.puncturing_vectors[
                self.puncturing_PI2[self.protect]] + self.dp.puncturing_tail_vector
            self.msc_conv_codeword_length = 4*self.msc_I + 24 # 4*I + 24 ()
        # exception in table
        else:
            self.msc_punctured_codeword_length = 5 * 4 * self.dp.puncturing_vectors_ones[13] + 1 * 4 * \
                                                                                               self.dp.puncturing_vectors_ones[
                                                                                                   12] + 12
        #sanity check
        assert(6*self.n == self.puncturing_L1[self.protect] + self.puncturing_L2[self.protect])


        # MSC selection and block partitioning
        # select OFDM carriers with MSC
        self.select_msc_syms = grdab.select_vectors(gr.sizeof_float, self.dp.num_carriers * 2, self.dp.num_msc_syms,
                                                  self.dp.num_fic_syms)
        # repartition MSC data in CIFs (left out due to heavy burden for scheduler and not really necessary)
        #self.repartition_msc_to_CIFs = grdab.repartition_vectors_make(gr.sizeof_float, self.dp.num_carriers * 2,
        #                                                            self.dp.cif_bits, self.dp.num_msc_syms,
        #                                                            self.dp.num_cifs)
        #repartition MSC to CUs
        self.repartition_msc_to_cus = grdab.repartition_vectors_make(gr.sizeof_float, self.dp.num_carriers*2, self.dp.msc_cu_size, self.dp.num_msc_syms, self.dp.num_cus * self.dp.num_cifs)

        # select CUs of one subchannel of each CIF and form logical frame vector
        self.select_subch = grdab.select_subch_vfvf_make(self.dp.msc_cu_size, self.dp.msc_cu_size * self.size, self.address, self.dp.num_cus)

        # time deinterleaving
        self.time_v2s = blocks.vector_to_stream_make(gr.sizeof_float, self.dp.msc_cu_size * self.size)
        self.time_deinterleaver = grdab.time_deinterleave_ff_make(self.dp.msc_cu_size * self.size, self.dp.scrambling_vector)
        # unpuncture
        self.conv_v2s = blocks.vector_to_stream(gr.sizeof_float, self.msc_punctured_codeword_length)
        self.unpuncture = grdab.unpuncture_ff_make(self.assembled_msc_puncturing_sequence, 0)

        # convolutional decoding
        self.fsm = trellis.fsm(1, 4, [0o133, 0o171, 0o145, 0o133])  # OK (dumped to text and verified partially)
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
        self.conv_decode = trellis.viterbi_combined(self.fsm, self.msc_I + self.dp.conv_code_add_bits_input, 0, 0, 4, table, trellis.TRELLIS_EUCLIDEAN)
        self.conv_s2v = blocks.stream_to_vector(gr.sizeof_char, self.msc_I + self.dp.conv_code_add_bits_input)
        self.conv_prune = grdab.prune(gr.sizeof_char, self.msc_conv_codeword_length / 4, 0,
                                            self.dp.conv_code_add_bits_input)

        #energy descramble
        self.prbs_src = blocks.vector_source_b(self.dp.prbs(int(self.msc_I)), True)
        self.energy_v2s = blocks.vector_to_stream(gr.sizeof_char, self.msc_I)
        self.add_mod_2 = blocks.xor_bb()
        #self.energy_s2v = blocks.stream_to_vector(gr.sizeof_char, self.msc_I)

        #pack bits
        self.pack_bits = blocks.unpacked_to_packed_bb_make(1, gr.GR_MSB_FIRST)

        # connect blocks
        self.connect((self, 0),
                     (self.select_msc_syms),
                     #(self.repartition_msc_to_CIFs, 0),
                     (self.repartition_msc_to_cus),
                     (self.select_subch, 0),
                     #(self.repartition_cus_to_logical_frame, 0),
                     self.time_v2s,
                     self.time_deinterleaver,
                     #self.conv_v2s,
                     self.unpuncture,
                     self.conv_decode,
                     #self.conv_s2v,
                     self.conv_prune,
                     #self.energy_v2s,
                     self.add_mod_2,
                     self.pack_bits,
                     #self.energy_s2v, #better output stream or vector??
                     (self))
        self.connect(self.prbs_src, (self.add_mod_2, 1))


#debug
        if debug is True:
            #msc_select_syms
            self.sink_msc_select_syms = blocks.file_sink_make(gr.sizeof_float * self.dp.num_carriers * 2, "debug/msc_select_syms.dat")
            self.connect(self.select_msc_syms, self.sink_msc_select_syms)

            #msc repartition cus
            self.sink_repartition_msc_to_cus = blocks.file_sink_make(gr.sizeof_float * self.dp.msc_cu_size, "debug/msc_repartitioned_to_cus.dat")
            self.connect((self.repartition_msc_to_cus), self.sink_repartition_msc_to_cus)

            #data of one sub channel not decoded
            self.sink_select_subch = blocks.file_sink_make(gr.sizeof_float * self.dp.msc_cu_size * self.size, "debug/select_subch.dat")
            self.connect(self.select_subch, self.sink_select_subch)

            #sub channel time_deinterleaved
            self.sink_subch_time_deinterleaved = blocks.file_sink_make(gr.sizeof_float, "debug/subch_time_deinterleaved.dat")
            self.connect(self.time_deinterleaver, self.sink_subch_time_deinterleaved)

            #sub channel unpunctured
            self.sink_subch_unpunctured = blocks.file_sink_make(gr.sizeof_float, "debug/subch_unpunctured.dat")
            self.connect(self.unpuncture, self.sink_subch_unpunctured)

            # sub channel convolutional decoded
            self.sink_subch_decoded = blocks.file_sink_make(gr.sizeof_char, "debug/subch_decoded.dat")
            self.connect(self.conv_decode, self.sink_subch_decoded)

            # sub channel convolutional decoded
            self.sink_subch_pruned = blocks.file_sink_make(gr.sizeof_char, "debug/subch_pruned.dat")
            self.connect(self.conv_prune, self.sink_subch_pruned)

            # sub channel energy dispersal undone unpacked
            self.sink_subch_energy_disp_undone = blocks.file_sink_make(gr.sizeof_char, "debug/subch_energy_disp_undone_unpacked.dat")
            self.connect(self.add_mod_2, self.sink_subch_energy_disp_undone)

            # sub channel energy dispersal undone packed
            self.sink_subch_energy_disp_undone_packed = blocks.file_sink_make(gr.sizeof_char, "debug/subch_energy_disp_undone_packed.dat")
            self.connect(self.pack_bits, self.sink_subch_energy_disp_undone_packed)
