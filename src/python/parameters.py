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
	DAB parameters for mode I to IV
	see Table 38, page 145 of the DAB specification
	for the PRN sequence vaules, see tables 39-43 on pages 148 and 149
	"""

	# parameter values for all modes
	__symbols_per_frame__ = [76, 76, 153, 76]             # number of OFDM symbols per DAB frame (excl. NS)
	__carriers__          = [1536, 384, 192, 768]         # number of carriers -> carrier width = 1536kHz/carriers
	__frame_length__      = [196608, 49152, 49152, 98304] # samples per frame; in ms: 96,24,24,48 (incl. NS)
	__ns_length__         = [2656, 664, 345, 1328]        # length of null symbol in samples
	__symbol_length__     = [2552, 638, 319, 1276]        # length of an OFDM symbol in samples
	__fft_length__        = [2048, 512, 256, 1024]        # fft length
	__cp_length__         = [504, 126, 63, 252]           # length of cyclic prefix
	sample_rate = 2048000
	T = 1./sample_rate

	# prn calculation data
	
	#format: [mode][index][k_min, k_max, k', i, n]
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
		[-128, -97,  -128, 0, 1],
		[-96,  -65,  -96,  1, 3],
		[-64,  -33,  -64,  2, 1],
		[-32,  -1,   -32,  3, 2],
		[1,    32,   1,    0, 3],
		[33,   64,   33,   3, 1],
		[65,   96,   65,   2, 1],
		[97,   128,  97,   1, 1],
		[129,  160,  129,  0, 2],
		[161,  192,  161,  3, 2],
		[193,  224,  193,  2, 1],
		[225,  256,  225,  1, 0],
		[257,  288,  257,  0, 2],
		[289,  320,  289,  3, 2],
		[321,  352,  321,  2, 3],
		[353,  384,  353,  1, 3],
		[385,  416,  385,  0, 0],
		[417,  448,  417,  3, 2],
		[449,  480,  449,  2, 1],
		[481,  512,  481,  1, 3],
		[513,  544,  513,  0, 3],
		[545,  576,  545,  3, 3],
		[577,  608,  577,  2, 3],
		[609,  640,  609,  1, 0],
		[641,  672,  641,  0, 3],
		[673,  704,  673,  3, 0],
		[705,  736,  705,  2, 1],
		[737,  768,  737,  1, 1]
	],[
		[-192, -161, -192, 0, 2],
		[-160, -129, -160, 1, 3],
		[-128, -97,  -128, 2, 2],
		[-96,  -65,  -96,  3, 2],
		[-64,  -33,  -64,  0, 1],
		[-32,  -1,   -32,  1, 2],
		[1,    32,   1,    2, 0],
		[33,   64,   33,   1, 2],
		[65,   96,   65,   0, 2],
		[97,   128,  97,   3, 1],
		[129,  160,  129,  2, 0],
		[161,  192,  161,  1, 3]
	],[
		[-96,  -65,  -96,  0, 2],
		[-64,  -33,  -64,  1, 3],
		[-32,  -1,   -32,  2, 0],
		[1,    32,   1,    3, 2],
		[33,   64,   33,   2, 2],
		[65,   96,   65,   1, 2]
	],[
		[-384, -353, -384, 0, 0],
		[-352, -321, -352, 1, 1],
		[-320, -289, -320, 2, 1],
		[-288, -257, -288, 3, 2],
		[-256, -225, -256, 0, 2],
		[-224, -193, -224, 1, 2],
		[-192, -161, -192, 2, 0],
		[-160, -129, -160, 3, 3],
		[-128, -97,  -128, 0, 3],
		[-96,  -65,  -96,  1, 1],
		[-64,  -33,  -64,  2, 3],
		[-32,  -1,   -32,  3, 2],
		[1,    32,   1,    0, 0],
		[33,   64,   33,   3, 1],
		[65,   96,   65,   2, 0],
		[97,   128,  97,   1, 2],
		[129,  160,  129,  0, 0],
		[161,  192,  161,  3, 1],
		[193,  224,  193,  2, 2],
		[225,  256,  225,  1, 2],
		[257,  288,  257,  0, 2],
		[289,  320,  289,  3, 1],
		[321,  352,  321,  2, 3],
		[353,  384,  353,  1, 0]
	]]

	# h_i,j
	# note: values for h_i,j are the same as for h_i,j+16 ...
	__prn_h__ = [ 
		[0, 2, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 2, 2, 1, 1, 0, 2, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 2, 2, 1, 1],
		[0, 3, 2, 3, 0, 1, 3, 0, 2, 1, 2, 3, 2, 3, 3, 0, 0, 3, 2, 3, 0, 1, 3, 0, 2, 1, 2, 3, 2, 3, 3, 0],
		[0, 0, 0, 2, 0, 2, 1, 3, 2, 2, 0, 2, 2, 0, 1, 3, 0, 0, 0, 2, 0, 2, 1, 3, 2, 2, 0, 2, 2, 0, 1, 3],
		[0, 1, 2, 1, 0, 3, 3, 2, 2, 3, 2, 1, 2, 1, 3, 2, 0, 1, 2, 1, 0, 3, 3, 2, 2, 3, 2, 1, 2, 1, 3, 2]
	]

	def __init__(self, mode):
		"""
		selects the correct parameters for the selected mode and calculates the prn sequence
		"""
		assert(mode>=1 and mode <=4)
		self.mode = mode
		# sanity checks:
		for i in range(0,4):
			assert(self.__symbols_per_frame__[i]*self.__symbol_length__[i]+self.__ns_length__[i] == self.__frame_length__[i])
			assert(self.__symbol_length__[i] == self.__fft_length__[i]+self.__cp_length__[i])

		self.symbols_per_frame = self.__symbols_per_frame__[mode-1]
		self.carriers          = self.__carriers__[mode-1]
		self.frame_length      = self.__frame_length__[mode-1]
		self.ns_length         = self.__ns_length__[mode-1]
		self.symbol_length     = self.__symbol_length__[mode-1]
		self.fft_length        = self.__fft_length__[mode-1]
		self.cp_length         = self.__cp_length__[mode-1]

		# prn sequence
		self.prn = []
		for k in range(-self.carriers//2, self.carriers//2+1):
			if k == 0:
				self.prn.append(0)
			else:
				[kk,i,n] = self.get_prn_kk_i_n(k)
				h = self.__prn_h__[i][k-kk]
				phi_k = (h+n)%4 # actually phi_k/(pi/2)
				if phi_k == 0: # e^(j*pi/2*phi_k) is not exact if calculated by python
					self.prn.append(1)
				elif phi_k == 1:
					self.prn.append(1j)
				elif phi_k == 2:
					self.prn.append(-1)
				elif phi_k == 3:
					self.prn.append(-1j)

	def get_prn_kk_i_n(self,k):
		assert(k!=0)
		assert(abs(k)<=self.carriers//2)
		if k<0:
			index = (k + self.carriers//2) // 32
			kk = 32*(int(k)//32)
		else:
			index = (k + self.carriers//2 - 1) // 32
			kk = 32*(int(k-1)//32)+1
		values = self.__prn_kin__[self.mode-1][index]
		assert(k>=values[0] and k<=values[1])
		assert(kk==values[2])
		i = values[3]
		n = values[4]
		return [kk, i, n]

class receiver_parameters:
	"""
	parameters for the receiver, independent of the standard
	"""
	__cp_gap__ = [30, 10, 5, 20] # adjust this ...
	def __init__(self,mode):
		assert(mode>=1 and mode <=4)
		self.mode = mode
		self.cp_gap = self.__cp_gap__[mode-1]
