# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT dab_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT dab_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND dab_python_files
    complex_to_interleaved_float_vcf_python.cc
    control_stream_to_tag_cc_python.cc
    crc16_bb_python.cc
    diff_phasor_vcc_python.cc
    estimate_sample_rate_bf_python.cc
    fib_sink_vb_python.cc
    firecode_check_bb_python.cc
    fractional_interpolator_triggered_update_cc_python.cc
    frequency_interleaver_vcc_python.cc
    insert_null_symbol_python.cc
    magnitude_equalizer_vcc_python.cc
    measure_processing_rate_python.cc
    modulo_ff_python.cc
    moving_sum_ff_python.cc
    mp2_decode_bs_python.cc
    mp4_decode_bs_python.cc
    ofdm_coarse_frequency_correct_python.cc
    ofdm_ffe_all_in_one_python.cc
    ofdm_insert_pilot_vcc_python.cc
    ofdm_move_and_insert_zero_python.cc
    ofdm_remove_first_symbol_vcc_python.cc
    ofdm_sampler_python.cc
    peak_detector_fb_python.cc
    prune_python.cc
    prune_vectors_python.cc
    puncture_bb_python.cc
    qpsk_demapper_vcb_python.cc
    qpsk_mapper_vbc_python.cc
    reed_solomon_decode_bb_python.cc
    repartition_vectors_python.cc
    select_subch_vfvf_python.cc
    select_vectors_python.cc
    sum_phasor_trig_vcc_python.cc
    time_deinterleave_ff_python.cc
    unpuncture_ff_python.cc
    unpuncture_vff_python.cc
    valve_ff_python.cc
    xrun_monitor_cc_python.cc
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(dab
   ../../..
   gr::dab
   "${dab_python_files}")

# copy in bindings .so file for use in QA test module
add_custom_target(
  copy_bindings_for_tests ALL
  COMMAND
    ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_BINARY_DIR}/*.so"
    ${CMAKE_BINARY_DIR}/test_modules/dab/
  DEPENDS dab_python)

install(TARGETS dab_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/dab COMPONENT pythonapi)
