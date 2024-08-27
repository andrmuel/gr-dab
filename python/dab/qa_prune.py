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

class qa_prune (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_prune(self):
        src_data = [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 2, 3]
        expected_result = [3, 4, 6, 5, 1, 2]
        src = blocks.vector_source_b(src_data)
        prune = grdab.prune(gr.sizeof_char, 5, 2, 1)
        dst = blocks.vector_sink_b()
        self.tb.connect(src, prune, dst)
        self.tb.run()
        result_data = dst.data()
        # print result_data
        self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)


if __name__ == '__main__':
    gr_unittest.run(qa_prune, "qa_prune.xml")
