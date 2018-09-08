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

########################################################################
# Include python install macros
########################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
  endif()


########################################################################
# Insert ICON PATH macro Insert ICON PATH macro into constants.py
########################################################################
set(GR_PKG_DAB_DATA_DIR ${GR_PKG_DATA_DIR})
set(GR_DAB_ICON_PATH ${CMAKE_INSTALL_PREFIX}/${GR_PKG_DATA_DIR})
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/constants.py.in
    ${CMAKE_CURRENT_BINARY_DIR}/constants.py
    ESCAPE_QUOTES
    @ONLY)

########################################################################
# Install python sources
########################################################################
GR_PYTHON_INSTALL(
    FILES
    __init__.py
    ofdm_sync_dab.py
    ofdm_sync_dab2.py
    detect_null.py
    ofdm.py
    parameters.py
    fic.py
    msc_decode.py
    channel_mapping.py
    app/get_channels.py
    ${CMAKE_CURRENT_BINARY_DIR}/constants.py
    dabplus_audio_decoder_ff.py DESTINATION ${GR_PYTHON_DIR}/grdab
)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-dab)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)
GR_ADD_TEST(qa_time_deinterleave_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_time_deinterleave_ff.py)
GR_ADD_TEST(qa_fib_sink_vb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_fib_sink_vb.py)
GR_ADD_TEST(qa_crc16_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_crc16_bb.py)
GR_ADD_TEST(qa_select_subch_vfvf ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_select_subch_vfvf.py)
GR_ADD_TEST(qa_unpuncture_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_unpuncture_ff.py)
GR_ADD_TEST(qa_prune ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_prune.py)
GR_ADD_TEST(qa_puncture_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_puncture_bb.py)
GR_ADD_TEST(qa_mp2_decode_bs ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_mp2_decode_bs.py)
GR_ADD_TEST(qa_mp4_decode_bs ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_mp4_decode_bs.py)
GR_ADD_TEST(qa_dabplus_audio_decoder_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_dabplus_audio_decoder_ff.py)
GR_ADD_TEST(qa_reed_solomon_decode_bb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_reed_solomon_decode_bb.py)
GR_ADD_TEST(qa_valve_ff ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_valve_ff.py)
GR_ADD_TEST(qa_peak_detector_fb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_peak_detector_fb.py)

add_subdirectory(app)
