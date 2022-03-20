#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Ruben Undheim
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

from gnuradio import gr, blocks

class osmo_or_zmq_source(gr.hier_block2):
    """
    """

    def __init__(self, frequency=220.352e6, rf_gain=25, if_gain=0, bb_gain=0, use_zeromq=False, server="tcp://127.0.0.1:10444", server_control="tcp://127.0.0.1:10445", samp_rate = 2048000, from_file=None, from_file_repeat=False):

        gr.hier_block2.__init__(self,
                                "osmo_or_zmq_source",
                                # Input signature
                                gr.io_signature(0, 0, 1),
                                # Output signature
                                gr.io_signature(1, 1, gr.sizeof_gr_complex))

        self.use_zeromq = use_zeromq
        self.from_file = from_file

        if from_file != None:
            print("Run from file %s" % from_file)
            file_input = blocks.file_source(gr.sizeof_gr_complex, from_file, from_file_repeat)
            fthrottle = blocks.throttle(gr.sizeof_gr_complex, samp_rate)
            self.connect(file_input, fthrottle)
            self.src = fthrottle
        elif not use_zeromq:
            import osmosdr
            self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
            self.osmosdr_source_0.set_sample_rate(samp_rate)
            self.osmosdr_source_0.set_center_freq(frequency, 0)
            self.osmosdr_source_0.set_freq_corr(0, 0)
            self.osmosdr_source_0.set_dc_offset_mode(0, 0)
            self.osmosdr_source_0.set_iq_balance_mode(0, 0)
            self.osmosdr_source_0.set_gain_mode(False, 0)
            self.osmosdr_source_0.set_gain(rf_gain, 0)
            self.osmosdr_source_0.set_if_gain(if_gain, 0)
            self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
            self.osmosdr_source_0.set_antenna('', 0)
            self.osmosdr_source_0.set_bandwidth(2000000, 0)
            self.src = self.osmosdr_source_0
        else:
            from gnuradio import zeromq
            self.zeromq_source = zeromq.sub_source(gr.sizeof_gr_complex, 1, server, 100, False, -1)
            self.rpc_mgr_server = zeromq.rpc_manager()
            self.rpc_mgr_server.set_request_socket(server_control)
            self.rpc_mgr_server.request("set_sample_rate",[samp_rate])
            self.rpc_mgr_server.request("set_rf_gain",[rf_gain])
            self.rpc_mgr_server.request("set_if_gain",[if_gain])
            self.rpc_mgr_server.request("set_bb_gain",[bb_gain])
            self.rpc_mgr_server.request("set_ppm",[0]) # Not using hardware correction since it behaves differently on different hardware
            self.rpc_mgr_server.request("set_frequency",[frequency])
            self.src = self.zeromq_source


        self.connect(self.src, (self, 0))


    def set_frequency(self, val):
        if self.from_file:
            print("set_frequency() Meaningless when listening to file")
        elif self.use_zeromq:
            self.rpc_mgr_server.request("set_frequency",[val]) 
        else:
            self.osmosdr_source_0.set_center_freq(val, 0)

    def set_rf_gain(self, val):
        if self.from_file:
            print("set_rf_gain() Meaningless when listening to file")
        elif self.use_zeromq:
            self.rpc_mgr_server.request("set_rf_gain",[val]) 
        else:
            self.osmosdr_source_0.set_gain(val, 0)

    def set_if_gain(self, val):
        if self.from_file:
            print("set_if_gain() Meaningless when listening to file")
        elif self.use_zeromq:
            self.rpc_mgr_server.request("set_if_gain",[val]) 
        else:
            self.osmosdr_source_0.set_if_gain(val, 0)

    def set_bb_gain(self, val):
        if self.from_file:
            print("set_bb_gain() Meaningless when listening to file")
        elif self.use_zeromq:
            self.rpc_mgr_server.request("set_bb_gain",[val]) 
        else:
            self.osmosdr_source_0.set_bb_gain(val, 0)
