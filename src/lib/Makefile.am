#
# Copyright 2004,2005,2006,2008 Free Software Foundation, Inc.
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

# Install this stuff so that it ends up as the gnuradio.dab module
# This usually ends up at:
#   ${prefix}/lib/python${python_version}/site-packages/gnuradio

ourpythondir = $(grpythondir)
ourlibdir    = $(grpyexecdir)

AM_CPPFLAGS = $(STD_DEFINES_AND_INCLUDES) $(PYTHON_CPPFLAGS) $(WITH_INCLUDES)

SWIGPYTHONARGS = $(SWIGPYTHONFLAGS) $(SWIGGRFLAGS) $(WITH_SWIG_INCLUDES) \
	$(WITH_INCLUDES)

ALL_IFILES = 				\
	$(LOCAL_IFILES)			\
	$(NON_LOCAL_IFILES)		

NON_LOCAL_IFILES =			\
	$(GNURADIO_CORE_INCLUDEDIR)/swig/gnuradio.i


LOCAL_IFILES = 				\
	$(top_srcdir)/src/lib/dab.i				

# These files are built by SWIG.  The first is the C++ glue.
# The second is the python wrapper that loads the _dab shared library
# and knows how to call our extensions.

BUILT_SOURCES = 			\
	dab_swig.cc			\
	dab_swig.py				

# This gets dab.py installed in the right place
ourpython_PYTHON =			\
	dab_swig.py

ourlib_LTLIBRARIES = _dab_swig.la

# These are the source files that go into the shared library
_dab_swig_la_SOURCES = 			        \
	dab_swig.cc		                \
	dab_moving_sum_ff.cc                    \
	dab_moving_sum_cc.cc                    \
	dab_ofdm_sampler.cc                     \
	dab_ofdm_coarse_frequency_correct.cc    \
	dab_diff_phasor_vcc.cc                  \
	dab_correct_individual_phase_offset_vff.cc \
	dab_ofdm_remove_first_symbol_vcc.cc     \
	dab_estimate_sample_rate_bf.cc          \
	dab_ofdm_ffs_sample.cc                  \
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
	dab_modulo_ff.cc

# magic flags
_dab_swig_la_LDFLAGS = $(NO_UNDEFINED) -module -avoid-version

# link the library against some comon swig runtime code and the 
# c++ standard library
_dab_swig_la_LIBADD = 			\
	$(PYTHON_LDFLAGS)		\
	-lstdc++			

dab_swig.cc dab_swig.py: $(LOCAL_IFILES) $(ALL_IFILES)
	$(SWIG) $(SWIGPYTHONARGS) -module dab_swig -o dab_swig.cc $(LOCAL_IFILES)

# These headers get installed in ${prefix}/include/gnuradio
grinclude_HEADERS =			        \
	dab_moving_sum_ff.h                     \
	dab_moving_sum_cc.h                     \
	dab_ofdm_sampler.h                      \
	dab_ofdm_coarse_frequency_correct.h     \
	dab_diff_phasor_vcc.h                   \
	dab_correct_individual_phase_offset_vff.h \
	dab_ofdm_remove_first_symbol_vcc.h      \
	dab_estimate_sample_rate_bf.h           \
	dab_ofdm_ffs_sample.h                   \
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
	dab_modulo_ff.h


# These swig headers get installed in ${prefix}/include/gnuradio/swig
swiginclude_HEADERS = 			\
	$(LOCAL_IFILES)


MOSTLYCLEANFILES = $(BUILT_SOURCES) *.pyc

# Don't distribute output of swig
dist-hook:
	@for file in $(BUILT_SOURCES); do echo $(RM) $(distdir)/$$file; done
	@for file in $(BUILT_SOURCES); do $(RM) $(distdir)/$$file; done
