/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */
#ifndef INCLUDED_DAB_COMPLEX_TO_INTERLEAVED_FLOAT_VCF_H
#define INCLUDED_DAB_COMPLEX_TO_INTERLEAVED_FLOAT_VCF_H

#include <gr_sync_block.h>

class dab_complex_to_interleaved_float_vcf;

typedef boost::shared_ptr<dab_complex_to_interleaved_float_vcf> dab_complex_to_interleaved_float_vcf_sptr;

dab_complex_to_interleaved_float_vcf_sptr 
dab_make_complex_to_interleaved_float_vcf (unsigned int length);

/*!
 * \brief deinterleaves [(i0,q0),(i1,q1),(i2,q2)] to [i0,i1,i2,..., q0,q1,q2,...]
 * \ingroup math
 *
 * \param length vector length at input
 *
 * input: complex vector
 * output: float vector
 */
class dab_complex_to_interleaved_float_vcf : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_complex_to_interleaved_float_vcf to
    // access the private constructor.

    friend dab_complex_to_interleaved_float_vcf_sptr
    dab_make_complex_to_interleaved_float_vcf (unsigned int length);

    dab_complex_to_interleaved_float_vcf (unsigned int length);    // private constructor

    unsigned int d_length;

  public:
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_COMPLEX_TO_INTERLEAVED_FLOAT_VCF_H */
