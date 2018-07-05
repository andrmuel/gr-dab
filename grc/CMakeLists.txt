# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
install(FILES
    dab_ofdm_sync_dab.xml
    dab_ofdm_sync_dab2.xml
    dab_detect_null.xml
    dab_moving_sum_ff.xml
    dab_ofdm_ffe_all_in_one.xml
    dab_ofdm_sampler.xml
    dab_ofdm_coarse_frequency_correct.xml
    dab_diff_phasor_vcc.xml
    dab_ofdm_remove_first_symbol_vcc.xml
    dab_frequency_interleaver_vcc.xml
    dab_qpsk_demapper_vcb.xml
    dab_complex_to_interleaved_float_vcf.xml
    dab_modulo_ff.xml
    dab_measure_processing_rate.xml
    dab_fic_decode.xml
    dab_ofdm_demod.xml
    dab_ofdm_mod.xml
    dab_select_vectors.xml
    dab_repartition_vectors.xml
    dab_unpuncture_vff.xml
    dab_prune_vectors.xml
    dab_fib_sink_vb.xml
    dab_estimate_sample_rate_bf.xml
    dab_fractional_interpolator_triggered_update_cc.xml
    dab_magnitude_equalizer_vcc.xml
    dab_qpsk_mapper_vbc.xml
    dab_ofdm_insert_pilot_vcc.xml
    dab_sum_phasor_trig_vcc.xml
    dab_ofdm_move_and_insert_zero.xml
    dab_insert_null_symbol.xml
    dab_time_deinterleave_ff.xml
    dab_crc16_bb.xml
    dab_msc_decode.xml
    dab_select_subch_vfvf.xml
    dab_unpuncture_ff.xml
    dab_prune.xml
    dab_firecode_check_bb.xml
    dab_puncture_bb.xml
    dab_mp2_decode_bs.xml
    dab_mp4_decode_bs.xml
    dab_reed_solomon_decode_bb.xml
    dab_dabplus_audio_decoder_ff.xml
    dab_valve_ff.xml
    dab_peak_detector_fb.xml DESTINATION share/gnuradio/grc/blocks
)
