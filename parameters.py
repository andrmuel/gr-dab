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

	def __init__(self, mode):
		"""
		selects the correct parameters for the selected mode and calculates the prn sequence
		"""
		assert(mode>=1 and mode <=4)
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

		# TODO prn


class receiver_parameters:
	"""
	parameters for the receiver, independent of the standard
	"""
	def __init__(self,mode):
		pass
