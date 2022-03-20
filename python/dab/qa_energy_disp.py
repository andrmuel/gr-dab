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

class qa_energy_disp (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

#test with reference data
    def test_001_t (self):
        energy_dispersal_undone = (0x05, 0x00, 0x10, 0xea, 0x04, 0x24, 0x06, 0x02, 0xd3, 0xa6, 0x01, 0x3f, 0x06, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4c, 0x89)
        energy_dispersal_done = (0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0xEA, 0xE9)
        fib_packed_to_unpacked = blocks.packed_to_unpacked_bb(1,gr.GR_MSB_FIRST)
        fib_unpacked_to_packed = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        src = blocks.vector_source_b(energy_dispersal_undone)
        self.dp = grdab.parameters.dab_parameters(1, 2e6, False)
        prbs_src = blocks.vector_source_b(self.dp.prbs(self.dp.energy_dispersal_fic_vector_length), True)
        add_mod_2 = blocks.xor_bb()
        dst = blocks.vector_sink_b()
        self.tb.connect(src, fib_packed_to_unpacked, add_mod_2, fib_unpacked_to_packed, dst)
        self.tb.connect(prbs_src, (add_mod_2, 1))
        self.tb.run ()
        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual(energy_dispersal_done, result_data, 6)


if __name__ == '__main__':
    gr_unittest.run(qa_energy_disp, "qa_energy_disp.xml")
