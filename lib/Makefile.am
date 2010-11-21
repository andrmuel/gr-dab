#
# Copyright 2004,2005,2006,2008,2009,2010 Free Software Foundation, Inc.
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
# 

include $(top_srcdir)/Makefile.common

# list of programs run by "make check" and "make distcheck"
TESTS = test_all

# ----------------------------------------------------------------
# dab C++ library: libgnuradio-dab.so
# ----------------------------------------------------------------

# C/C++ headers get installed in ${prefix}/include/$(modname)
modinclude_HEADERS = \
	dab_moving_sum_ff.h                     \
	dab_moving_sum_cc.h                     \
	dab_ofdm_sampler.h                      \
	dab_ofdm_coarse_frequency_correct.h     \
	dab_diff_phasor_vcc.h                   \
	dab_correct_individual_phase_offset_vff.h \
	dab_ofdm_remove_first_symbol_vcc.h      \
	dab_estimate_sample_rate_bf.h           \
	dab_ofdm_ffs_sample.h                   \
	dab_ofdm_ffe_all_in_one.h               \
	dab_fractional_interpolator_triggered_update_cc.h \
	dab_frequency_interleaver_vcc.h         \
	dab_qpsk_mapper_vbc.h                   \
	dab_qpsk_demapper_vcb.h                 \
	dab_ofdm_insert_pilot_vcc.h             \
	dab_sum_phasor_trig_vcc.h               \
	dab_ofdm_move_and_insert_zero.h         \
	dab_insert_null_symbol.h                \
	dab_concatenate_signals.h               \
	dab_measure_processing_rate.h           \
	dab_sum_elements_vff.h                  \
	dab_modulo_ff.h                         \
	dab_measure_ber_b.h                     \
	dab_select_vectors.h                    \
	dab_repartition_vectors.h               \
	dab_puncture_vbb.h                      \
	dab_unpuncture_vff.h                    \
	dab_magnitude_equalizer_vcc.h           \
	dab_complex_to_interleaved_float_vcf.h  \
	dab_prune_vectors.h                     \
	dab_fib_sink_vb.h

lib_LTLIBRARIES = libgnuradio-dab.la

libgnuradio_dab_la_SOURCES = \
	dab_moving_sum_ff.cc                    \
	dab_moving_sum_cc.cc                    \
	dab_ofdm_sampler.cc                     \
	dab_ofdm_coarse_frequency_correct.cc    \
	dab_diff_phasor_vcc.cc                  \
	dab_correct_individual_phase_offset_vff.cc \
	dab_ofdm_remove_first_symbol_vcc.cc     \
	dab_estimate_sample_rate_bf.cc          \
	dab_ofdm_ffs_sample.cc                  \
	dab_ofdm_ffe_all_in_one.cc              \
	dab_fractional_interpolator_triggered_update_cc.cc \
	dab_frequency_interleaver_vcc.cc        \
	dab_qpsk_mapper_vbc.cc                  \
	dab_qpsk_demapper_vcb.cc                \
	dab_ofdm_insert_pilot_vcc.cc            \
	dab_sum_phasor_trig_vcc.cc              \
	dab_ofdm_move_and_insert_zero.cc        \
	dab_insert_null_symbol.cc               \
	dab_concatenate_signals.cc              \
	dab_measure_processing_rate.cc          \
	dab_sum_elements_vff.cc                 \
	dab_modulo_ff.cc                        \
	dab_measure_ber_b.cc                    \
	dab_select_vectors.cc                   \
	dab_repartition_vectors.cc              \
	dab_puncture_vbb.cc                     \
	dab_unpuncture_vff.cc                   \
	dab_magnitude_equalizer_vcc.cc          \
	dab_complex_to_interleaved_float_vcf.cc \
	dab_prune_vectors.cc                    \
	dab_fib_sink_vb.cc                      \
	crc16.cc

libgnuradio_dab_la_LIBADD = \
	$(GNURADIO_CORE_LA)

libgnuradio_dab_la_LDFLAGS = $(NO_UNDEFINED) $(LTVERSIONFLAGS)

# ----------------------------------------------------------------
# howto C++ QA library: libgnuradio-dab-qa.so (not installed)
# ----------------------------------------------------------------

noinst_LTLIBRARIES = libgnuradio-dab-qa.la

libgnuradio_dab_qa_la_SOURCES = \
	qa_dab.cc
#     qa_howto_square_ff.cc \
#     qa_howto_square2_ff.cc

libgnuradio_dab_qa_la_LDFLAGS = $(NO_UNDEFINED) -version-info 0:0:0

libgnuradio_dab_qa_la_LIBADD = \
	libgnuradio-dab.la \
	$(CPPUNIT_LIBS)

# ----------------------------------------------------------------
# headers that don't get installed
# ----------------------------------------------------------------
noinst_HEADERS = \
	qa_dab.h
#     qa_howto_square_ff.h \
#     qa_howto_square2_ff.h

# ----------------------------------------------------------------
# test program
# ----------------------------------------------------------------
noinst_PROGRAMS = \
	test_all

test_all_SOURCES = test_all.cc
test_all_LDADD   = libgnuradio-dab-qa.la
