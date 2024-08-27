/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#include <pybind11/pybind11.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

namespace py = pybind11;

// Headers for binding functions
/**************************************/
// The following comment block is used for
// gr_modtool to insert function prototypes
// Please do not delete
/**************************************/
// BINDING_FUNCTION_PROTOTYPES(
void bind_complex_to_interleaved_float_vcf(py::module& m);
void bind_control_stream_to_tag_cc(py::module& m);
void bind_crc16_bb(py::module& m);
void bind_diff_phasor_vcc(py::module& m);
void bind_estimate_sample_rate_bf(py::module& m);
void bind_fib_sink_vb(py::module& m);
void bind_firecode_check_bb(py::module& m);
void bind_fractional_interpolator_triggered_update_cc(py::module& m);
void bind_frequency_interleaver_vcc(py::module& m);
void bind_insert_null_symbol(py::module& m);
void bind_magnitude_equalizer_vcc(py::module& m);
void bind_measure_processing_rate(py::module& m);
void bind_modulo_ff(py::module& m);
void bind_moving_sum_ff(py::module& m);
void bind_mp2_decode_bs(py::module& m);
void bind_mp4_decode_bs(py::module& m);
void bind_ofdm_coarse_frequency_correct(py::module& m);
void bind_ofdm_ffe_all_in_one(py::module& m);
void bind_ofdm_insert_pilot_vcc(py::module& m);
void bind_ofdm_move_and_insert_zero(py::module& m);
void bind_ofdm_remove_first_symbol_vcc(py::module& m);
void bind_ofdm_sampler(py::module& m);
void bind_peak_detector_fb(py::module& m);
void bind_prune(py::module& m);
void bind_prune_vectors(py::module& m);
void bind_puncture_bb(py::module& m);
void bind_qpsk_demapper_vcb(py::module& m);
void bind_qpsk_mapper_vbc(py::module& m);
void bind_reed_solomon_decode_bb(py::module& m);
void bind_repartition_vectors(py::module& m);
void bind_select_subch_vfvf(py::module& m);
void bind_select_vectors(py::module& m);
void bind_sum_phasor_trig_vcc(py::module& m);
void bind_time_deinterleave_ff(py::module& m);
void bind_unpuncture_ff(py::module& m);
void bind_unpuncture_vff(py::module& m);
void bind_valve_ff(py::module& m);
void bind_xrun_monitor_cc(py::module& m);
// ) END BINDING_FUNCTION_PROTOTYPES


// We need this hack because import_array() returns NULL
// for newer Python versions.
// This function is also necessary because it ensures access to the C API
// and removes a warning.
void* init_numpy()
{
    import_array();
    return NULL;
}

PYBIND11_MODULE(dab_python, m)
{
    // Initialize the numpy C API
    // (otherwise we will see segmentation faults)
    init_numpy();

    // Allow access to base block methods
    py::module::import("gnuradio.gr");

    /**************************************/
    // The following comment block is used for
    // gr_modtool to insert binding function calls
    // Please do not delete
    /**************************************/
    // BINDING_FUNCTION_CALLS(
    bind_complex_to_interleaved_float_vcf(m);
    bind_control_stream_to_tag_cc(m);
    bind_crc16_bb(m);
    bind_diff_phasor_vcc(m);
    bind_estimate_sample_rate_bf(m);
    bind_fib_sink_vb(m);
    bind_firecode_check_bb(m);
    bind_fractional_interpolator_triggered_update_cc(m);
    bind_frequency_interleaver_vcc(m);
    bind_insert_null_symbol(m);
    bind_magnitude_equalizer_vcc(m);
    bind_measure_processing_rate(m);
    bind_modulo_ff(m);
    bind_moving_sum_ff(m);
    bind_mp2_decode_bs(m);
    bind_mp4_decode_bs(m);
    bind_ofdm_coarse_frequency_correct(m);
    bind_ofdm_ffe_all_in_one(m);
    bind_ofdm_insert_pilot_vcc(m);
    bind_ofdm_move_and_insert_zero(m);
    bind_ofdm_remove_first_symbol_vcc(m);
    bind_ofdm_sampler(m);
    bind_peak_detector_fb(m);
    bind_prune(m);
    bind_prune_vectors(m);
    bind_puncture_bb(m);
    bind_qpsk_demapper_vcb(m);
    bind_qpsk_mapper_vbc(m);
    bind_reed_solomon_decode_bb(m);
    bind_repartition_vectors(m);
    bind_select_subch_vfvf(m);
    bind_select_vectors(m);
    bind_sum_phasor_trig_vcc(m);
    bind_time_deinterleave_ff(m);
    bind_unpuncture_ff(m);
    bind_unpuncture_vff(m);
    bind_valve_ff(m);
    bind_xrun_monitor_cc(m);

    // ) END BINDING_FUNCTION_CALLS
}
