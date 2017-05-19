#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import dab

class qa_fib_sink_vb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

#manual check of print outs with reference data of debug file (SWR radio station)
    def test_001_t (self):
        src = blocks.file_source_make(gr.sizeof_char, "debug/fic_with_crc16_packed.dat")
        fibout = blocks.stream_to_vector(1, 32)
        fibsink = dab.fib_sink_vb()
        self.tb.connect(src, fibout, fibsink)
        self.tb.run()
        pass


if __name__ == '__main__':
    gr_unittest.run(qa_fib_sink_vb, "qa_fib_sink_vb.xml")
