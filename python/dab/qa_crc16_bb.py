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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import dab_python as grdab


class qa_crc16_bb(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    # test with random data
    def test_001_t(self):
        src_data01 = (
            0x1D, 0x13, 0x06, 0x00, 0x00, 0x01, 0x0B, 0x00, 0x00, 0x05, 0x03, 0x00, 0x00, 0x09, 0x07, 0x00, 0x00, 0x04,
            0x09, 0x00, 0x00, 0x0C, 0x02, 0x00, 0x00, 0x02, 0x08, 0x00, 0x00, 0x0A, 0x00, 0x00)
        expected_result = (
            0x1D, 0x13, 0x06, 0x00, 0x00, 0x01, 0x0B, 0x00, 0x00, 0x05, 0x03, 0x00, 0x00, 0x09, 0x07, 0x00, 0x00, 0x04,
            0x09, 0x00, 0x00, 0x0C, 0x02, 0x00, 0x00, 0x02, 0x08, 0x00, 0x00, 0x0A, 0xE4, 0x9C)
        src = blocks.vector_source_b(src_data01)
        s2v = blocks.stream_to_vector(gr.sizeof_char, 32)
        crc16 = grdab.crc16_bb(32, 0x1021, 0xffff)
        v2s = blocks.vector_to_stream(gr.sizeof_char, 32)
        dst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, crc16, v2s, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(expected_result, result_data)

    # test with reference data
    def test_003_t(self):
        src_data02 = (
            0x05, 0x00, 0x10, 0xEA, 0x03, 0x8E, 0x06, 0x02, 0xD3, 0xA6, 0x01, 0x3F, 0x06, 0xFF, 0x00, 0x00, 0x00, 0x00,
            0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)

        expected_result = (
            0x05, 0x00, 0x10, 0xEA, 0x03, 0x8E, 0x06, 0x02, 0xD3, 0xA6, 0x01, 0x3F, 0x06, 0xFF, 0x00, 0x00, 0x00, 0x00,
            0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x56, 0xEF)
        src = blocks.vector_source_b(src_data02)
        s2v = blocks.stream_to_vector(gr.sizeof_char, 32)
        crc16 = grdab.crc16_bb(32, 0x1021, 0xffff)
        v2s = blocks.vector_to_stream(gr.sizeof_char, 32)
        dst = blocks.vector_sink_b()
        self.tb.connect(src, s2v, crc16, v2s, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(expected_result, result_data)


if __name__ == '__main__':
    gr_unittest.run(qa_crc16_bb, "qa_crc16_bb.xml")
