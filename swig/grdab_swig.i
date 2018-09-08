/* -*- c++ -*- */

#define DAB_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "grdab_swig_doc.i"

%{
#include "grdab/moving_sum_ff.h"
#include "grdab/ofdm_ffe_all_in_one.h"
#include "grdab/ofdm_sampler.h"
#include "grdab/ofdm_coarse_frequency_correct.h"
#include "grdab/diff_phasor_vcc.h"
#include "grdab/ofdm_remove_first_symbol_vcc.h"
#include "grdab/frequency_interleaver_vcc.h"
#include "grdab/qpsk_demapper_vcb.h"
#include "grdab/complex_to_interleaved_float_vcf.h"
#include "grdab/modulo_ff.h"
#include "grdab/measure_processing_rate.h"
#include "grdab/select_vectors.h"
#include "grdab/repartition_vectors.h"
#include "grdab/unpuncture_vff.h"
#include "grdab/prune_vectors.h"
#include "grdab/fib_sink_vb.h"
#include "grdab/estimate_sample_rate_bf.h"
#include "grdab/fractional_interpolator_triggered_update_cc.h"
#include "grdab/magnitude_equalizer_vcc.h"
#include "grdab/qpsk_mapper_vbc.h"
#include "grdab/ofdm_insert_pilot_vcc.h"
#include "grdab/sum_phasor_trig_vcc.h"
#include "grdab/ofdm_move_and_insert_zero.h"
#include "grdab/insert_null_symbol.h"
#include "grdab/time_deinterleave_ff.h"
#include "grdab/crc16_bb.h"
#include "grdab/select_subch_vfvf.h"
#include "grdab/unpuncture_ff.h"
#include "grdab/prune.h"
#include "grdab/firecode_check_bb.h"
#include "grdab/puncture_bb.h"
#include "grdab/mp2_decode_bs.h"
#include "grdab/mp4_decode_bs.h"
#include "grdab/reed_solomon_decode_bb.h"
#include "grdab/valve_ff.h"
#include "grdab/peak_detector_fb.h"
#include "grdab/control_stream_to_tag_cc.h"
#include "grdab/xrun_monitor_cc.h"
%}


%include "grdab/moving_sum_ff.h"
GR_SWIG_BLOCK_MAGIC2(dab, moving_sum_ff);
%include "grdab/ofdm_ffe_all_in_one.h"
GR_SWIG_BLOCK_MAGIC2(dab, ofdm_ffe_all_in_one);
%include "grdab/ofdm_sampler.h"
GR_SWIG_BLOCK_MAGIC2(dab, ofdm_sampler);
%include "grdab/ofdm_coarse_frequency_correct.h"
GR_SWIG_BLOCK_MAGIC2(dab, ofdm_coarse_frequency_correct);
%include "grdab/diff_phasor_vcc.h"
GR_SWIG_BLOCK_MAGIC2(dab, diff_phasor_vcc);
%include "grdab/ofdm_remove_first_symbol_vcc.h"
GR_SWIG_BLOCK_MAGIC2(dab, ofdm_remove_first_symbol_vcc);
%include "grdab/frequency_interleaver_vcc.h"
GR_SWIG_BLOCK_MAGIC2(dab, frequency_interleaver_vcc);
%include "grdab/qpsk_demapper_vcb.h"
GR_SWIG_BLOCK_MAGIC2(dab, qpsk_demapper_vcb);
%include "grdab/complex_to_interleaved_float_vcf.h"
GR_SWIG_BLOCK_MAGIC2(dab, complex_to_interleaved_float_vcf);
%include "grdab/modulo_ff.h"
GR_SWIG_BLOCK_MAGIC2(dab, modulo_ff);
%include "grdab/measure_processing_rate.h"
GR_SWIG_BLOCK_MAGIC2(dab, measure_processing_rate);
%include "grdab/select_vectors.h"
GR_SWIG_BLOCK_MAGIC2(dab, select_vectors);
%include "grdab/repartition_vectors.h"
GR_SWIG_BLOCK_MAGIC2(dab, repartition_vectors);
%include "grdab/unpuncture_vff.h"
GR_SWIG_BLOCK_MAGIC2(dab, unpuncture_vff);
%include "grdab/prune_vectors.h"
GR_SWIG_BLOCK_MAGIC2(dab, prune_vectors);
%include "grdab/fib_sink_vb.h"
GR_SWIG_BLOCK_MAGIC2(dab, fib_sink_vb);
%include "grdab/estimate_sample_rate_bf.h"
GR_SWIG_BLOCK_MAGIC2(dab, estimate_sample_rate_bf);
%include "grdab/fractional_interpolator_triggered_update_cc.h"
GR_SWIG_BLOCK_MAGIC2(dab, fractional_interpolator_triggered_update_cc);
%include "grdab/magnitude_equalizer_vcc.h"
GR_SWIG_BLOCK_MAGIC2(dab, magnitude_equalizer_vcc);
%include "grdab/qpsk_mapper_vbc.h"
GR_SWIG_BLOCK_MAGIC2(dab, qpsk_mapper_vbc);
%include "grdab/ofdm_insert_pilot_vcc.h"
GR_SWIG_BLOCK_MAGIC2(dab, ofdm_insert_pilot_vcc);
%include "grdab/sum_phasor_trig_vcc.h"
GR_SWIG_BLOCK_MAGIC2(dab, sum_phasor_trig_vcc);
%include "grdab/ofdm_move_and_insert_zero.h"
GR_SWIG_BLOCK_MAGIC2(dab, ofdm_move_and_insert_zero);
%include "grdab/insert_null_symbol.h"
GR_SWIG_BLOCK_MAGIC2(dab, insert_null_symbol);
%include "grdab/time_deinterleave_ff.h"
GR_SWIG_BLOCK_MAGIC2(dab, time_deinterleave_ff);
%include "grdab/crc16_bb.h"
GR_SWIG_BLOCK_MAGIC2(dab, crc16_bb);
%include "grdab/select_subch_vfvf.h"
GR_SWIG_BLOCK_MAGIC2(dab, select_subch_vfvf);
%include "grdab/unpuncture_ff.h"
GR_SWIG_BLOCK_MAGIC2(dab, unpuncture_ff);
%include "grdab/prune.h"
GR_SWIG_BLOCK_MAGIC2(dab, prune);
%include "grdab/firecode_check_bb.h"
GR_SWIG_BLOCK_MAGIC2(dab, firecode_check_bb);
%include "grdab/puncture_bb.h"
GR_SWIG_BLOCK_MAGIC2(dab, puncture_bb);

%include "grdab/mp2_decode_bs.h"
GR_SWIG_BLOCK_MAGIC2(dab, mp2_decode_bs);

%include "grdab/mp4_decode_bs.h"
GR_SWIG_BLOCK_MAGIC2(dab, mp4_decode_bs);
%include "grdab/reed_solomon_decode_bb.h"
GR_SWIG_BLOCK_MAGIC2(dab, reed_solomon_decode_bb);


%include "grdab/valve_ff.h"
GR_SWIG_BLOCK_MAGIC2(dab, valve_ff);
%include "grdab/peak_detector_fb.h"
GR_SWIG_BLOCK_MAGIC2(dab, peak_detector_fb);
%include "grdab/control_stream_to_tag_cc.h"
GR_SWIG_BLOCK_MAGIC2(dab, control_stream_to_tag_cc);

%include "grdab/xrun_monitor_cc.h"
GR_SWIG_BLOCK_MAGIC2(dab, xrun_monitor_cc);
