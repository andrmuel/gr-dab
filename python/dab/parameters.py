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

class dab_parameters:
    """
    @brief Represents the DAB parameters.

    DAB parameters for mode I to IV

    as specified in
    ETSI EN 300 401 V1.4.1 (2006-06)
    "Digital Audio Broadcasting (DAB) to mobile, portable and fixed receivers"
    """

    # parameter values for all modes

    # OFDM parameters (section 14)
    # Table 38, page 145 of the DAB specification
    __symbols_per_frame__ = [76, 76, 153, 76]  # number of OFDM symbols per DAB frame (incl. pilot, excl. NS)
    __num_carriers__ = [1536, 384, 192, 768]  # number of carriers -> carrier width = 1536kHz/carriers
    __frame_length__ = [196608, 49152, 49152, 98304]  # samples per frame; in ms: 96,24,24,48 (incl. NS)
    __ns_length__ = [2656, 664, 345, 1328]  # length of null symbol in samples
    __symbol_length__ = [2552, 638, 319, 1276]  # length of an OFDM symbol in samples
    __fft_length__ = [2048, 512, 256, 1024]  # fft length
    __cp_length__ = [504, 126, 63, 252]  # length of cyclic prefix
    default_sample_rate = 2048000
    T = 1. / default_sample_rate

    # prn calculation data
    # tables 39-43 on pages 148 and 149

    # format: [mode][index][k_min, k_max, k', i, n]
    __prn_kin__ = [[
        [-768, -737, -768, 0, 1],
        [-736, -705, -736, 1, 2],
        [-704, -673, -704, 2, 0],
        [-672, -641, -672, 3, 1],
        [-640, -609, -640, 0, 3],
        [-608, -577, -608, 1, 2],
        [-576, -545, -576, 2, 2],
        [-544, -513, -544, 3, 3],
        [-512, -481, -512, 0, 2],
        [-480, -449, -480, 1, 1],
        [-448, -417, -448, 2, 2],
        [-416, -385, -416, 3, 3],
        [-384, -353, -384, 0, 1],
        [-352, -321, -352, 1, 2],
        [-320, -289, -320, 2, 3],
        [-288, -257, -288, 3, 3],
        [-256, -225, -256, 0, 2],
        [-224, -193, -224, 1, 2],
        [-192, -161, -192, 2, 2],
        [-160, -129, -160, 3, 1],
        [-128, -97, -128, 0, 1],
        [-96, -65, -96, 1, 3],
        [-64, -33, -64, 2, 1],
        [-32, -1, -32, 3, 2],
        [1, 32, 1, 0, 3],
        [33, 64, 33, 3, 1],
        [65, 96, 65, 2, 1],
        [97, 128, 97, 1, 1],
        [129, 160, 129, 0, 2],
        [161, 192, 161, 3, 2],
        [193, 224, 193, 2, 1],
        [225, 256, 225, 1, 0],
        [257, 288, 257, 0, 2],
        [289, 320, 289, 3, 2],
        [321, 352, 321, 2, 3],
        [353, 384, 353, 1, 3],
        [385, 416, 385, 0, 0],
        [417, 448, 417, 3, 2],
        [449, 480, 449, 2, 1],
        [481, 512, 481, 1, 3],
        [513, 544, 513, 0, 3],
        [545, 576, 545, 3, 3],
        [577, 608, 577, 2, 3],
        [609, 640, 609, 1, 0],
        [641, 672, 641, 0, 3],
        [673, 704, 673, 3, 0],
        [705, 736, 705, 2, 1],
        [737, 768, 737, 1, 1]
    ], [
        [-192, -161, -192, 0, 2],
        [-160, -129, -160, 1, 3],
        [-128, -97, -128, 2, 2],
        [-96, -65, -96, 3, 2],
        [-64, -33, -64, 0, 1],
        [-32, -1, -32, 1, 2],
        [1, 32, 1, 2, 0],
        [33, 64, 33, 1, 2],
        [65, 96, 65, 0, 2],
        [97, 128, 97, 3, 1],
        [129, 160, 129, 2, 0],
        [161, 192, 161, 1, 3]
    ], [
        [-96, -65, -96, 0, 2],
        [-64, -33, -64, 1, 3],
        [-32, -1, -32, 2, 0],
        [1, 32, 1, 3, 2],
        [33, 64, 33, 2, 2],
        [65, 96, 65, 1, 2]
    ], [
        [-384, -353, -384, 0, 0],
        [-352, -321, -352, 1, 1],
        [-320, -289, -320, 2, 1],
        [-288, -257, -288, 3, 2],
        [-256, -225, -256, 0, 2],
        [-224, -193, -224, 1, 2],
        [-192, -161, -192, 2, 0],
        [-160, -129, -160, 3, 3],
        [-128, -97, -128, 0, 3],
        [-96, -65, -96, 1, 1],
        [-64, -33, -64, 2, 3],
        [-32, -1, -32, 3, 2],
        [1, 32, 1, 0, 0],
        [33, 64, 33, 3, 1],
        [65, 96, 65, 2, 0],
        [97, 128, 97, 1, 2],
        [129, 160, 129, 0, 0],
        [161, 192, 161, 3, 1],
        [193, 224, 193, 2, 2],
        [225, 256, 225, 1, 2],
        [257, 288, 257, 0, 2],
        [289, 320, 289, 3, 1],
        [321, 352, 321, 2, 3],
        [353, 384, 353, 1, 0]
    ]]

    # h_i,j
    # note: values for h_i,j are the same as for h_i,j+16 ...
    __prn_h__ = [
        [0, 2, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 2, 2, 1, 1, 0, 2, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 2, 2, 1, 1],
        [0, 3, 2, 3, 0, 1, 3, 0, 2, 1, 2, 3, 2, 3, 3, 0, 0, 3, 2, 3, 0, 1, 3, 0, 2, 1, 2, 3, 2, 3, 3, 0],
        [0, 0, 0, 2, 0, 2, 1, 3, 2, 2, 0, 2, 2, 0, 1, 3, 0, 0, 0, 2, 0, 2, 1, 3, 2, 2, 0, 2, 2, 0, 1, 3],
        [0, 1, 2, 1, 0, 3, 3, 2, 2, 3, 2, 1, 2, 1, 3, 2, 0, 1, 2, 1, 0, 3, 3, 2, 2, 3, 2, 1, 2, 1, 3, 2]
    ]

    __expected_frequency_interleaving__ = [
        # these few values are listed in the specs - they are used to verify the sequence
        [-513, -14, 329, 692, -733, 13, 680, 273, -36, 43],
        [-129, -14, -55, -76, 163, 141, -88, 7, -111, -85],
        [-65, -14, 52, -29, -58, 77, 40, 71, -38, 81],
        [-257, -14, 73, 180, 198, -243, 168, 218, 17, 299]
    ]

    # transport mechanism parameters
    __num_fic_syms__ = [3, 3, 8, 3]  # number of OFDM symbols per frame belonging to the FIC
    __num_msc_syms__ = [72, 72, 144, 72] # number of OFDM symbols per frame belonging to the MSC

    # puncturing
    puncturing_vectors = [  # table 29, page 131
        [],  # "Who are you? How did you get in my house?"
        [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        # PI=1: code rate: 8/9
        [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        # PI=2: code rate: 8/10
        [1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        # PI=3: code rate: 8/11
        [1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        # PI=4: code rate: 8/12
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        # PI=5: code rate: 8/13
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        # PI=6: code rate: 8/14
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        # PI=7: code rate: 8/15
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        # PI=8: code rate: 8/16
        [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        # PI=9: code rate: 8/17
        [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        # PI=10 code rate: 8/18
        [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        # PI=11 code rate: 8/19
        [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0],
        # PI=12 code rate: 8/20
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0],
        # PI=13 code rate: 8/21
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0],
        # PI=14 code rate: 8/22
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0],
        # PI=15 code rate: 8/23
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        # PI=16 code rate: 8/24
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        # PI=17 code rate: 8/25
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        # PI=18 code rate: 8/26
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        # PI=19 code rate: 8/27
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        # PI=20 code rate: 8/28
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        # PI=21 code rate: 8/29
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        # PI=22 code rate: 8/30
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        # PI=23 code rate: 8/31
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        # PI=24 code rate: 8/32
    ]
    puncturing_tail_vector = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]  # V_T
    puncturing_vectors_ones = [0, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    # conv coding rate at a protection level, table 7
    conv_code_rate = [1/4, 3/8, 1/2, 3/4]
    subch_size_multiple_n = [12, 8, 6, 4]

    # convolutional coding - 11.1, page 129/130
    conv_code_generator_polynomials = [
        0o133,
        0o171,
        0o145,
        0o133
    ]
    conv_code_initial_state = 0
    conv_code_final_state = 0
    conv_code_constraint_length = 7
    conv_code_in_bits = 1
    conv_code_add_bits_input = 6
    conv_code_out_bits = 4
    __fic_conv_codeword_length__ = [3096, 3096, 4120, 3096]  # 4*I + 24
    __fic_punctured_codeword_length__ = [2304, 2304, 3072, 2304]

    # energy dispersal

    __energy_dispersal_fic_fibs_per_vector__ = [3, 3, 4, 3]
    __energy_dispersal_fic_vector_length__ = [768, 768, 1024, 768]  # I
    __prbs_bits__ = [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1,
                     0]  # first 16 PRBS bits are given in the standard - can be used for another assert
    # time interleaving
    scrambling_vector = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]

    # transport mechanism parameters
    fib_bits = 256
    cif_bits = 55296
    __num_fibs__ = [12, 3, 4, 6]  # FIC
    __num_cifs__ = [4, 1, 1, 2]  # MSC -> num cifs = num fib groups
    num_cus = 864 # number of CUs in one cif
    msc_cu_size = 64 # size of capacity unit in msc (smallest unit)

    def __init__(self, mode, sample_rate=2048000, verbose=True):
        """
        selects the correct parameters for the selected mode and calculates the prn sequence, etc.

        @param mode DAB mode (I-IV)
        @param sample_rate sampling frequency
        """
        if verbose:
            print("--> creating DAB parameter object") # should not be seen more than once

        assert (mode >= 1 and mode <= 4)
        self.mode = mode
        self.sample_rate = sample_rate
        self.verbose = verbose

        # sanity checks:
        for i in range(0, 4):
            # OFDM parameters
            assert (
            self.__symbols_per_frame__[i] * self.__symbol_length__[i] + self.__ns_length__[i] == self.__frame_length__[
                i])
            assert (self.__symbol_length__[i] == self.__fft_length__[i] + self.__cp_length__[i])
            # block partitioning
            assert (self.__num_carriers__[i] * 2 * self.__num_fic_syms__[i] / self.__num_cifs__[i] ==
                    self.__fic_punctured_codeword_length__[i])
            # energy dispersal parameters
            assert (self.__energy_dispersal_fic_fibs_per_vector__[i] * self.fib_bits ==
                    self.__energy_dispersal_fic_vector_length__[i])
            assert (3 * self.__energy_dispersal_fic_vector_length__[i] == self.__fic_punctured_codeword_length__[
                i])  # not sure - according to specification, code rate is only approximately 1/3, but seems to be exact

        # sanity checks for PRBS sequence (energy dispersal)
        assert (self.prbs(16) == self.__prbs_bits__)  # bits from DAB standard
        assert (self.prbs(511) == self.prbs(1022)[511:])  # sequence must repeat itself
        if verbose:
            print("--> DAB parameters self check ok")

        self.__update_parameters__()

    def set_mode(self, mode):
        if self.verbose:
            print("--> setting DAB mode to " + str(mode))
        self.mode = mode
        self.__update_parameters__()

    def set_sample_rate(self, sample_rate):
        if self.verbose:
            print("--> setting sample rate to " + str(sample_rate))
        self.sample_rate = sample_rate
        self.__update_parameters__()

    def __update_parameters__(self):
        if self.verbose:
            print("--> updating DAB parameters")
        mode = self.mode
        # OFDM parameters (14)
        self.symbols_per_frame = self.__symbols_per_frame__[mode - 1]
        self.num_carriers = self.__num_carriers__[mode - 1]
        self.frame_length = self.__frame_length__[mode - 1]
        self.ns_length = self.__ns_length__[mode - 1]
        self.symbol_length = self.__symbol_length__[mode - 1]
        self.fft_length = self.__fft_length__[mode - 1]
        self.cp_length = self.__cp_length__[mode - 1]

        # bytes per frame and bytes per symbol
        self.bytes_per_frame = (self.symbols_per_frame - 1) * self.num_carriers / 4
        self.bytes_per_symbol = self.num_carriers / 4

        # prn sequence
        self.prn = []
        for k in range(-self.num_carriers // 2, self.num_carriers // 2 + 1):
            if k == 0:
                # self.prn.append(0)
                pass
            else:
                [kk, i, n] = self.__get_prn_kk_i_n__(k)
                h = self.__prn_h__[i][k - kk]
                phi_k = (h + n) % 4  # actually phi_k/(pi/2)
                if phi_k == 0:  # e^(j*pi/2*phi_k) is not exact if calculated by python
                    self.prn.append(1)
                elif phi_k == 1:
                    self.prn.append(1j)
                elif phi_k == 2:
                    self.prn.append(-1)
                elif phi_k == 3:
                    self.prn.append(-1j)

        # frequency (de)interleaving
        a = self.fft_length / 4 - 1
        b = self.fft_length
        A = [0]
        for i in range(1, self.fft_length):
            A.append((13 * A[-1] + a) % b)
        D = [d for d in A if d >= self.fft_length / 8 and d <= 7 * self.fft_length / 8 and d != self.fft_length / 2]
        assert (len(D) == self.num_carriers)
        self.frequency_interleaving_sequence = [d - self.fft_length / 2 for d in D]
        assert (self.frequency_interleaving_sequence[0:len(self.__expected_frequency_interleaving__[mode - 1])] ==
                self.__expected_frequency_interleaving__[mode - 1])
        # sequence for arrays, with indices starting from 0 and central carrier already removed
        self.frequency_interleaving_sequence_array = [k + self.num_carriers / 2 - (k > 0) for k in
                                                      self.frequency_interleaving_sequence]
        assert (len(self.frequency_interleaving_sequence_array) == self.num_carriers)
        assert (min(self.frequency_interleaving_sequence_array) == 0)
        assert (max(self.frequency_interleaving_sequence_array) == self.num_carriers - 1)
        assert (len(set(self.frequency_interleaving_sequence_array)) == len(
            self.frequency_interleaving_sequence_array))  # uniqueness of elements

        # frequency deinterleaving sequence
        self.frequency_deinterleaving_sequence_array = [self.frequency_interleaving_sequence_array.index(i) for i in
                                                        range(0, self.num_carriers)]

        # adapt for non-standard sample rate - do this at end, frequency interleaving calculation still needs default fft length
        if self.sample_rate != self.default_sample_rate:
            if self.verbose:
                print("--> using non-standard sample rate: " + str(self.sample_rate))
            self.T = 1. / self.sample_rate
            self.ns_length = int(round(self.ns_length * float(self.sample_rate) / float(self.default_sample_rate)))
            self.cp_length = int(round(self.cp_length * float(self.sample_rate) / float(self.default_sample_rate)))
            self.fft_length = int(round(self.fft_length * float(self.sample_rate) / float(self.default_sample_rate)))
            self.symbol_length = self.cp_length + self.fft_length
            self.frame_length = self.symbols_per_frame * self.symbol_length + self.ns_length

        # block partitioning parameters (14.4)
        self.num_fic_syms = self.__num_fic_syms__[mode - 1]
        self.num_msc_syms = self.__num_msc_syms__[mode - 1]

        # convolutional coding (11)
        self.fic_conv_codeword_length = self.__fic_conv_codeword_length__[mode - 1]  # length after puncturing

        # unpuncturing sequence (assembled, such that it can be applied on a complete fib group)
        # see 11.2 page 132
        self.fic_punctured_codeword_length = self.__fic_punctured_codeword_length__[mode - 1]
        if mode in [1, 2, 4]:
            self.assembled_fic_puncturing_sequence = 21 * 4 * self.puncturing_vectors[16] + 3 * 4 * \
                                                                                            self.puncturing_vectors[
                                                                                                15] + self.puncturing_tail_vector
        else:
            self.assembled_fic_puncturing_sequence = 29 * 4 * self.puncturing_vectors[16] + 3 * 4 * \
                                                                                            self.puncturing_vectors[
                                                                                                15] + self.puncturing_tail_vector
        assert (len(self.assembled_fic_puncturing_sequence) == self.fic_conv_codeword_length)
        #assert (
        #len(filter(lambda x: x == 1, self.assembled_fic_puncturing_sequence)) == self.fic_punctured_codeword_length)

        # energy dispersal (10)
        self.energy_dispersal_fic_fibs_per_vector = self.__energy_dispersal_fic_fibs_per_vector__[mode - 1]
        self.energy_dispersal_fic_vector_length = self.__energy_dispersal_fic_vector_length__[mode - 1]

        # transport mechanism parameters (5)
        self.num_fibs = self.__num_fibs__[mode - 1]
        self.num_cifs = self.__num_cifs__[mode - 1]

    def __get_prn_kk_i_n__(self, k):
        assert (k != 0)
        assert (abs(k) <= self.num_carriers // 2)
        if k < 0:
            index = (k + self.num_carriers // 2) // 32
            kk = 32 * (int(k) // 32)
        else:
            index = (k + self.num_carriers // 2 - 1) // 32
            kk = 32 * (int(k - 1) // 32) + 1
        values = self.__prn_kin__[self.mode - 1][index]
        assert (k >= values[0] and k <= values[1])
        assert (kk == values[2])
        i = values[3]
        n = values[4]
        return [kk, i, n]

    def prbs(self, length):
        """
        PRBS generated with the polynomial p(x) = x^9 + x^5 + 1
        and initial state 111111111

        @param length number of bits in the sequence
        """
        bits = [1] * 9
        sequence = []
        for i in range(0, length):
            newbit = bits[8] ^ bits[4]
            bits = [newbit] + bits[0:-1]
            sequence.append(newbit)
        return sequence

class receiver_parameters:
    """
    @brief Parameters for the receiver, independent of the DAB standard
    """
    # filter at input
    filt_bw = (768 + 100) * 1e3
    filt_tb = 50e3

    # OFDM stuff
    __cp_gap__ = [252, 63, 31, 124]  # gap for ofdm_sampler to leave before the start of the next symbol
    __symbols_for_ffs_estimation__ = [8, 8, 16, 8]  # number of symbols to evaluate for fine frequency error estimation
    __symbols_for_magnitude_equalization__ = [6, 6, 12,
                                              6]  # how many symbols should be used to estimate magnitude equalizer?
    ffs_alpha = 0.5

    # phase variance estimation
    phase_var_estimate_alpha = 0.01
    phase_var_estimate_downsample = 100  # 50 -> uses about 1% of the CPU time

    # for USRP
    usrp_ffc_retune_frequency = 5  # how often should the USRP be retuned at most?
    usrp_ffc_min_deviation = 5  # how far off does the FFE have to be to retune the USRP?
    usrp_ffc_adapt_factor = 0.5  # how much to adapt the correction?

    def __init__(self, mode, sample_rate=2048000, softbits=False, input_fft_filter=True, autocorrect_sample_rate=False,
                 sample_rate_correction_factor=1, correct_ffe=True, equalize_magnitude=True, verbose=True, always_include_resample=False):
        """
        Create new instance.

        @param mode DAB mode (I-IV)
        @param sample_rate sampling frequency
        @param input_fft_filter whether to use an FFT filter at the input
        @param autocorrect_sample_rate whether to correct the sample rate dynamically
        @param sample_rate_correction_factor static correction factor for sample rate
        @parem correct_ffe if False, only estimate fine frequency error - don't correct it
        @param verbose be talkative
        """
        if verbose:
            print("--> creating RX parameter object")
        assert (mode >= 1 and mode <= 4)

        self.set_mode(mode)
        self.sample_rate = sample_rate
        self.softbits = softbits
        self.input_fft_filter = input_fft_filter
        self.autocorrect_sample_rate = autocorrect_sample_rate
        self.sample_rate_correction_factor = sample_rate_correction_factor
        self.correct_ffe = correct_ffe
        self.equalize_magnitude = equalize_magnitude
        self.verbose = verbose
        self.always_include_resample = always_include_resample

    def set_mode(self, mode):
        self.mode = mode
        self.cp_gap = self.__cp_gap__[mode - 1]
        self.symbols_for_ffs_estimation = self.__symbols_for_ffs_estimation__[mode - 1]
        self.symbols_for_magnitude_equalization = self.__symbols_for_magnitude_equalization__[mode - 1]
