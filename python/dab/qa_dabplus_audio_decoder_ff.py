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
from gnuradio import audio
import os
import dab_python as grdab
from gnuradio import audio

class qa_dabplus_audio_decoder_ff (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

# manual check, if header info makes sense and if AAC gives errors
# final check by playing the produced audio file, you may have to adjust the wavfile_sink configuration arguments to printed header info
    def test_001_t (self):
        if os.path.exists("debug/transmission_frame.dat") and os.path.exists("debug/transmission_frame_trigger.dat"):
            self.dab_params = grdab.parameters.dab_parameters(1, 208.064e6, True)
            self.src01 = blocks.file_source(gr.sizeof_float * 2 * self.dab_params.num_carriers,
                                                 "debug/transmission_frame.dat")
            self.src02 = blocks.file_source(gr.sizeof_char, "debug/transmission_frame_trigger.dat")
            self.dabplus = grdab.dabplus_audio_decoder_ff(self.dab_params, 112, 54, 84, 2, True, False, True)
            self.wav_sink = blocks.wavfile_sink("debug/music.wav", 2, 32000)
            self.file_sink_left = blocks.file_sink(gr.sizeof_float, "debug/PCM_left.dat")
            self.file_sink_right = blocks.file_sink(gr.sizeof_float, "debug/PCM_right.dat")
            self.tb.connect(self.src01, (self.dabplus, 0), self.file_sink_left)
            self.tb.connect(self.src02, (self.dabplus, 1), self.file_sink_right)
            self.tb.connect((self.dabplus, 0), (self.wav_sink, 0))
            self.tb.connect((self.dabplus, 1), (self.wav_sink, 1))
            self.audio = audio.sink(32000)

            self.tb.connect((self.dabplus, 0), (self.audio, 0))
            self.tb.connect((self.dabplus, 1), (self.audio, 1))


            self.tb.run()
        else:
            log = gr.logger("log")
            log.debug("debug file not found - skipped test")
            log.set_level("WARN")
        pass


if __name__ == '__main__':
    gr_unittest.run(qa_dabplus_audio_decoder_ff, "qa_dabplus_audio_decoder_ff.xml")
