#!/usr/bin/env python2

import json
import time

def get_channels(frequency=220.352e6, rf_gain=25, if_gain=0, bb_gain=0, ppm=0, use_zeromq=False, server="tcp://127.0.0.1:10444", server_control="tcp://127.0.0.1:10445", from_file=None, from_file_repeat=False):
    from gnuradio import gr, blocks, audio
    if use_zeromq:
        from gnuradio import zeromq

    import osmosdr
    import gnuradio.dab as grdab
    import time

    samp_rate = samp_rate = 2048000

    print("Setting frequency: %0.3f MHz" % (frequency/1e6))

    fg = gr.top_block()

    if from_file != None:
        file_input = blocks.file_source(gr.sizeof_gr_complex, from_file, True) # Makes sense to always repeat
        src = file_input
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

    dab_fic_decode_0 = grdab.fic_decode(
              grdab.parameters.dab_parameters(
                mode=1,
                sample_rate=samp_rate,
                verbose=False
              )
            )
    #dab_fic_decode_0.set_print_channel_info(True)


    fg.connect(src, dab_ofdm_demod_0)
    fg.connect(dab_ofdm_demod_0, dab_fic_decode_0)



    fg.start()

    attempt = 0
    maxattempts = 9
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
                channels[s['reference']]['dabplus'] = s['DAB+']
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
        if attempt == maxattempts-1:
            all_have_label = True
        complete = False
        if len(channels) > 0 and all_have_label:
            print("Channels:")
            for c,item in channels.items():
                if 'subch_info' in item:
                    conv_table = [ 128, 8, 6, 5];
                    protect_level = item['subch_info']['protection']
                    subch_size = item['subch_info']['size']
                    if protect_level <= 4:
                        if 'label' in item:
                            label = item['label']
                        else:
                            label = "UNKNOWN"
                        bit_rate = subch_size * 8 / (conv_table[protect_level]);

                        print("%s: (address: %3d, subch_size: %3d, protect_level: %1d, bit_rate: %3d, classic: %1d)" % (label, item['subch_info']['address'], item['subch_info']['size'], item['subch_info']['protection'], bit_rate, not item['dabplus']))
                complete = True

        if complete:
            break
        attempt = attempt + 1
        time.sleep(1)
    fg.stop()
