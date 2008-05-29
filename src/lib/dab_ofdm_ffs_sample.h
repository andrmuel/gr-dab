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
#ifndef INCLUDED_DAB_OFDM_FFS_SAMPLE_H
#define INCLUDED_DAB_OFDM_FFS_SAMPLE_H

#include <gr_sync_block.h>

#define _1_OVER_2PI_T 325949.32345 /* scaling factor for printing frequency error estimates */

class dab_ofdm_ffs_sample;

typedef boost::shared_ptr<dab_ofdm_ffs_sample> dab_ofdm_ffs_sample_sptr;

dab_ofdm_ffs_sample_sptr dab_make_ofdm_ffs_sample (int symbol_length, int num_symbols, float alpha);

/*!
 * \brief samples FFS error estimation at the correct time and averages it
 * \ingroup DAB
 * \param symbol_length number of samples in an OFDM symbol
 * \param num_symbols number of symbols to use for averaging (more symbols is better, but symbols towards the end of the frame tend to have larger time offsets and worse values)
 * \param alpha how fast should we adapt to new FFS error values (1=immediately)
 *
 * input: port 0: float - actual data; port 1: byte - trigger signal indicating the start of a frame
 * output: float fine frequency offset estimation
 */
class dab_ofdm_ffs_sample : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_ofdm_ffs_sample to
    // access the private constructor.

    friend dab_ofdm_ffs_sample_sptr dab_make_ofdm_ffs_sample (int symbol_length, int num_symbols, float alpha);

    dab_ofdm_ffs_sample (int symbol_length, int num_symbols, float alpha);    // private constructor

    unsigned int d_symbol_length;   // length of a symbol in samples
    unsigned int d_num_symbols;     // number of symbols per frame to average over
    float d_alpha;                  // adjustment speed factor

    unsigned int d_cur_symbol;      // which symbol in the frame is currently under observation?
    unsigned int d_cur_sample;      // which sample in the symbol is currently under observation?
    float d_ffs_error_sum;          // sum of error samples in current frame
    float d_estimated_error;        // total estimated error

  public:
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_OFDM_FFS_SAMPLE_H */
