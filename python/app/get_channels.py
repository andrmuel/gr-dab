#!/usr/bin/env python2

import json

def get_channels(frequency=220.352e6, rf_gain=25, if_gain=0, bb_gain=0, ppm=0, use_zeromq=False):
    from gnuradio import gr, blocks, audio
    if use_zeromq:
        from gnuradio import zeromq

    import osmosdr
    import grdab
    import time

    samp_rate = samp_rate = 2000000

    print("Setting frequency: %0.3f MHz" % (frequency/1e6))

    if not use_zeromq:
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
        osmosdr_source_0.set_antenna('', 0)
        osmosdr_source_0.set_bandwidth(2000000, 0)
    else:
        zeromq_source = zeromq.sub_source(gr.sizeof_gr_complex, 1, "tcp://127.0.0.1:10444", 100, False, -1)

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

    dab_fic_decode_0 = grdab.fic_decode(
              grdab.parameters.dab_parameters(
                mode=1,
                sample_rate=samp_rate,
                verbose=False
              )
            )
    #dab_fic_decode_0.set_print_channel_info(True)

    fg = gr.top_block()

    if not use_zeromq:
        fg.connect(osmosdr_source_0, dab_ofdm_demod_0)
    else:
        fg.connect(zeromq_source, dab_ofdm_demod_0)
    fg.connect(dab_ofdm_demod_0, dab_fic_decode_0)



    fg.start()

    channels = {}
    while True:
        service_labels = dab_fic_decode_0.get_service_labels()
        if service_labels.strip() != "":
            service_labels_json = json.loads(service_labels.strip())
            for s in service_labels_json:
                if s['reference'] not in channels:
                    channels[s['reference']] = {}
                channels[s['reference']]['label'] = s['label']
            subch_info = dab_fic_decode_0.get_subch_info()
        service_info = dab_fic_decode_0.get_service_info() # mapping between service_labels number and subch_info number
        if service_info.strip() != "":
            service_info_json = json.loads(service_info.strip())
            for s in service_info_json:
                if s['reference'] not in channels:
                    channels[s['reference']] = {}
                channels[s['reference']]['id'] = s['ID']
        subch_info = dab_fic_decode_0.get_subch_info() # settings needed for setting channel
        if subch_info.strip() != "":
            subch_info_json = json.loads(subch_info.strip())
            for s in subch_info_json:
                if 'ID' in s:
                    current_id = s['ID']
                    for key,val in channels.items():
                        if 'id' in val:
                            if val['id'] == current_id:
                                channels[key]['subch_info'] = s
                                break

        all_have_label = True
        for c,item in channels.items():
            if 'label' not in item:
                all_have_label = False
        complete = False
        if len(channels) > 0 and all_have_label:
            print("Channels:")
            for c,item in channels.items():
                if 'label' in item and 'subch_info' in item:
                    conv_table = [ 128, 8, 6, 5];
                    protect_level = item['subch_info']['protection']
                    subch_size = item['subch_info']['size']
                    if protect_level <= 4:
                        bit_rate = subch_size * 8 / (conv_table[protect_level]);

                        print("%s: (address: %3d, subch_size: %3d, protect_level: %1d, bit_rate: %3d)" % (item['label'], item['subch_info']['address'], item['subch_info']['size'], item['subch_info']['protection'], bit_rate))
                complete = True

        if complete:
            break
        time.sleep(1)
    fg.stop()
