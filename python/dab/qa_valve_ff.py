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
import dab_python as grdab

class qa_valve_ff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        src_data = (1, 2, 3, 4)
        expected_result = (1, 2, 3, 4)
        src = blocks.vector_source_f(src_data)
        valve = grdab.valve_ff(False)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, valve, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(expected_result, result_data)

    def test_002_t (self):
        src_data = (1, 2, 3, 4)
        expected_result = (0, 0, 0, 0)
        src = blocks.vector_source_f(src_data)
        valve = grdab.valve_ff(True, True)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, valve, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(expected_result, result_data)


if __name__ == '__main__':
    gr_unittest.run(qa_valve_ff, "qa_valve_ff.xml")
