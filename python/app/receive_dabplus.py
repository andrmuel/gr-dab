#!/usr/bin/env python2

def receive_dabplus(frequency=220.352e6, rf_gain=25, if_gain=0, bb_gain=0, ppm=80, audio_sample_rate=48000, dab_bit_rate=64, dab_address=304, dab_subch_size=64, dab_protect_level=1, use_zeromq=False, dabplus=True, server="tcp://127.0.0.1:10444", server_control="tcp://127.0.0.1:10445", from_file=None, from_file_repeat=False, skip_xrun_monitor=False):
    from gnuradio import gr, blocks, audio
    if use_zeromq:
        from gnuradio import zeromq

    import time
    import osmosdr
    import gnuradio.dab as grdab

    samp_rate = samp_rate = 2048000

    print("Setting frequency: %0.3f MHz" % (frequency/1e6))
    print("Setting RF gain to: %d" % rf_gain)
    print("Setting Frequency error (ppm) to: %d" % ppm)

    fg = gr.top_block()

    if from_file != None:
        file_input = blocks.file_source(gr.sizeof_gr_complex, from_file, from_file_repeat)
        if skip_xrun_monitor:
            src = file_input
        else:
            fthrottle = blocks.throttle(gr.sizeof_gr_complex, samp_rate)
            fg.connect(file_input, fthrottle)
            src = fthrottle
        print("Run from file %s" % from_file)
    elif not use_zeromq:
        osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        osmosdr_source_0.set_sample_rate(samp_rate)
        osmosdr_source_0.set_center_freq(frequency, 0)
        osmosdr_source_0.set_freq_corr(0, 0)
        osmosdr_source_0.set_dc_offset_mode(0, 0)
        osmosdr_source_0.set_iq_balance_mode(0, 0)
        osmosdr_source_0.set_gain_mode(False, 0)
        osmosdr_source_0.set_gain(rf_gain, 0)
        osmosdr_source_0.set_if_gain(if_gain, 0)
        osmosdr_source_0.set_bb_gain(bb_gain, 0)
        osmosdr_source_0.set_antenna('RX2', 0)
        osmosdr_source_0.set_bandwidth(2000000, 0)
        src = osmosdr_source_0
    else:
        zeromq_source = zeromq.sub_source(gr.sizeof_gr_complex, 1, server, 100, False, -1)
        rpc_mgr_server = zeromq.rpc_manager()
        rpc_mgr_server.set_request_socket(server_control)
        rpc_mgr_server.request("set_sample_rate",[samp_rate])
        rpc_mgr_server.request("set_rf_gain",[rf_gain])
        rpc_mgr_server.request("set_if_gain",[if_gain])
        rpc_mgr_server.request("set_bb_gain",[bb_gain])
        rpc_mgr_server.request("set_ppm",[0]) # Not using hardware correction since it behaves differently on different hardware
        rpc_mgr_server.request("set_frequency",[frequency])
        time.sleep(0.7)
        src = zeromq_source

    sample_rate_correction_factor = 1 + float(ppm)*1e-6
    dab_ofdm_demod_0 = grdab.ofdm_demod(
              grdab.parameters.dab_parameters(
                mode=1,
                sample_rate=samp_rate,
                verbose=False
              ),
              grdab.parameters.receiver_parameters(
                mode=1,
                softbits=True,
                input_fft_filter=True,
                autocorrect_sample_rate=False,
                sample_rate_correction_factor=sample_rate_correction_factor,
                always_include_resample=True,
                verbose=False,
                correct_ffe=True,
                equalize_magnitude=True
              )
            )

    if dabplus:
        decoder = grdab.dabplus_audio_decoder_ff(grdab.parameters.dab_parameters(mode=1, sample_rate=samp_rate, verbose=False), dab_bit_rate, dab_address, dab_subch_size, dab_protect_level, True)
    else:
        decoder = grdab.dab_audio_decoder_ff(grdab.parameters.dab_parameters(mode=1, sample_rate=samp_rate, verbose=False), dab_bit_rate, dab_address, dab_subch_size, dab_protect_level, True)

    xrun_monitor = grdab.xrun_monitor_cc(100000)
    f2c = blocks.float_to_complex()
    c2f = blocks.complex_to_float()

    audio_sink_0 = audio.sink(audio_sample_rate, '', True)



    fg.connect(src, dab_ofdm_demod_0, decoder)
    fg.connect((decoder, 0), (f2c, 0))
    fg.connect((decoder, 1), (f2c, 1))
    if skip_xrun_monitor:
        fg.connect(f2c, c2f)
    else:
        fg.connect(f2c, xrun_monitor)
        fg.connect(xrun_monitor, c2f)
    fg.connect((c2f, 0), (audio_sink_0, 0))
    fg.connect((c2f, 1), (audio_sink_0, 1))



    if from_file != None and from_file_repeat == False and skip_xrun_monitor:
        fg.run()
    else:
        fg.start()
        input("Running..")
        fg.stop()
    #new = grdab.dabplus_audio_decoder_ff(grdab.parameters.dab_parameters(mode=1, sample_rate=samp_rate, verbose=False), 64, 304, 64, 1, True)
    #newaudio = audio.sink(44100, '', True)
    #fg.wait()
    #xrun_monitor.stop_until_tag()
    #fg.disconnect(src, dab_ofdm_demod_0, decoder)
    #fg.disconnect((decoder, 0), (f2c, 0))
    #fg.disconnect((decoder, 1), (f2c, 1))
    #fg.disconnect((c2f, 0), (audio_sink_0, 0))
    #fg.disconnect((c2f, 1), (audio_sink_0, 1))
    #decoder = new
    #audio_sink_0 = newaudio
    #fg.connect(src, dab_ofdm_demod_0, decoder)
    #fg.connect((decoder, 0), (f2c, 0))
    #fg.connect((decoder, 1), (f2c, 1))
    #fg.connect((c2f, 0), (audio_sink_0, 0))
    #fg.connect((c2f, 1), (audio_sink_0, 1))
    #fg.start()
    #raw_input("Running..")
    #fg.stop()
