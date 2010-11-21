#
# Copyright 2004 Free Software Foundation, Inc.
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

EXTRA_DIST = run_tests.in
TESTS = run_tests

modpython_PYTHON = \
	__init__.py            \
	fic.py                 \
	ofdm.py                \
	ofdm_sync_dab.py       \
	ofdm_sync_dab2.py      \
	detect_null.py         \
	parameters.py

noinst_PYTHON =       \
	qa_block_partitioning_vbb.py                   \
	qa_concatenate_signals.py                      \
	qa_correct_individual_phase_offset_vff.py      \
	qa_diff_phasor_vcc.py                          \
	qa_estimate_sample_rate.py                     \
	qa_fractional_interpolator_triggered_update.py \
	qa_frequency_interleaving.py                   \
	qa_insert_null_symbol.py                       \
	qa_measure_ber.py                              \
	qa_measure_processing_rate.py                  \
	qa_module_ff.py                                \
	qa_moving_sum.py                               \
	qa_ofdm_coarse_frequency_correct.py            \
	qa_ofdm_ffe_all_in_one.py                      \
	qa_ofdm_ffs_sample.py                          \
	qa_ofdm_insert_pilot.py                        \
	qa_ofdm_move_and_insert_zero.py                \
	qa_ofdm_remove_first_symbol.py                 \
	qa_ofdm_sampler.py                             \
	qa_puncture_vbb.py                             \
	qa_qpsk_demapper_vcb.py                        \
	qa_qpsk_mapper_vbc.py                          \
	qa_select_vectors_vbb.py                       \
	qa_sum_elements_vff.py                         \
	qa_sum_phasor_trig_vcc.py                      \
	qa_unpuncture_vbb.py
