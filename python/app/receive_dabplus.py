#!/usr/bin/env python2

def receive_dabplus(frequency=220.352e6, rf_gain=25, if_gain=0, bb_gain=0, ppm=80, audio_sample_rate=48000, dab_bit_rate=64, dab_address=304, dab_subch_size=64, dab_protect_level=1):
    from gnuradio import gr, blocks, audio

    import osmosdr
    import grdab

    samp_rate = samp_rate = 2000000

    print("Setting frequency: %0.3f MHz" % (frequency/1e6))
    print("Setting RF gain to: %d" % rf_gain)
    print("Setting Frequency error (ppm) to: %d" % ppm)

    osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
    osmosdr_source_0.set_sample_rate(samp_rate)
    osmosdr_source_0.set_center_freq(frequency, 0)
    osmosdr_source_0.set_freq_corr(ppm, 0)
    osmosdr_source_0.set_dc_offset_mode(0, 0)
    osmosdr_source_0.set_iq_balance_mode(0, 0)
    osmosdr_source_0.set_gain_mode(False, 0)
    osmosdr_source_0.set_gain(rf_gain, 0)
    osmosdr_source_0.set_if_gain(if_gain, 0)
    osmosdr_source_0.set_bb_gain(bb_gain, 0)
    osmosdr_source_0.set_antenna('', 0)
    osmosdr_source_0.set_bandwidth(2000000, 0)

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
                sample_rate_correction_factor=1,
                verbose=False,
                correct_ffe=True,
                equalize_magnitude=True
              )
            )
      
    dab_dabplus_audio_decoder_ff_0 = grdab.dabplus_audio_decoder_ff(grdab.parameters.dab_parameters(mode=1, sample_rate=samp_rate, verbose=False), dab_bit_rate, dab_address, dab_subch_size, dab_protect_level, True)

    xrun_monitor = grdab.xrun_monitor_cc(500000)
    f2c = blocks.float_to_complex()
    c2f = blocks.complex_to_float()

    audio_sink_0 = audio.sink(audio_sample_rate, '', True)

    fg = gr.top_block()

    fg.connect(osmosdr_source_0, dab_ofdm_demod_0, dab_dabplus_audio_decoder_ff_0)
    fg.connect((dab_dabplus_audio_decoder_ff_0, 0), (f2c, 0))
    fg.connect((dab_dabplus_audio_decoder_ff_0, 1), (f2c, 1))
    fg.connect(f2c, xrun_monitor)
    fg.connect(xrun_monitor, c2f)
    fg.connect((c2f, 0), (audio_sink_0, 0))
    fg.connect((c2f, 1), (audio_sink_0, 1))



    fg.start()
    raw_input("Running..")
    fg.stop()
