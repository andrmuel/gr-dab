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

class qa_puncture_bb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_puncture_ff(self):
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        punc_seq = (1, 0, 0, 0, 1, 0, 1, 1, 1)
        exp_res = [float(x) for x in (0, 4, 6, 7, 8)]
        src = blocks.vector_source_b(src_data)
        puncture = grdab.puncture_bb(punc_seq)
        dst = blocks.vector_sink_b()
        self.tb.connect(src, puncture, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(exp_res, result_data)

    def test_002_puncture_ff(self):
        src_data = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        punc_seq = (1, 0, 0)
        exp_res = [float(x) for x in (0, 3, 6, 9, 2, 5)]
        src = blocks.vector_source_b(src_data)
        puncture = grdab.puncture_bb(punc_seq)
        dst = blocks.vector_sink_b()
        self.tb.connect(src, puncture, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(exp_res, result_data)


if __name__ == '__main__':
    gr_unittest.run(qa_puncture_bb, "qa_puncture_bb.xml")
