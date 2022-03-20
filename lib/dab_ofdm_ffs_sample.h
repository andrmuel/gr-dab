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

class dab_ofdm_ffs_sample;

typedef std::shared_ptr<dab_ofdm_ffs_sample> dab_ofdm_ffs_sample_sptr;

dab_ofdm_ffs_sample_sptr dab_make_ofdm_ffs_sample (unsigned int symbol_length, unsigned int fft_length, unsigned int num_symbols, float alpha, unsigned int sample_rate);

/*!
 * \brief samples FFS error estimation at the correct time and averages it
 * \ingroup DAB
 * \param symbol_length number of samples in an OFDM symbol
 * \param fft_length number of samples in an OFDM symbol without the cyclic prefix
 * \param num_symbols number of symbols to use for averaging (more symbols is better, but symbols towards the end of the frame tend to have larger time offsets and worse values)
 * \param alpha how fast should we adapt to new FFS error values (1=immediately)
 * \param sample_rate sampling rate - needed to calculate the offset estimation in Hz
 *
 * input: port 0: float - actual data; port 1: byte - trigger signal indicating the start of a frame
 * output: float fine frequency offset estimation (in radian per sample)
 */
class dab_ofdm_ffs_sample : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_ofdm_ffs_sample to
    // access the private constructor.

    friend dab_ofdm_ffs_sample_sptr dab_make_ofdm_ffs_sample (unsigned int symbol_length, unsigned int fft_length, unsigned int num_symbols, float alpha, unsigned int sample_rate);

    dab_ofdm_ffs_sample (unsigned int symbol_length, unsigned int fft_length, unsigned int num_symbols, float alpha, unsigned int sample_rate);    // private constructor

    unsigned int d_symbol_length;   // length of a symbol in samples
    unsigned int d_fft_length;      // length of a symbol without cyclic prefix in samples
    unsigned int d_num_symbols;     // number of symbols per frame to average over
    float d_alpha;                  // adjustment speed factor
    unsigned int d_sample_rate;     // sample rate -- only needed to print the ffs error in Hz

    unsigned int d_cur_symbol;      // which symbol in the frame is currently under observation?
    unsigned int d_cur_sample;      // which sample in the symbol is currently under observation?
    float d_ffs_error_sum;          // sum of error samples in current frame
    float d_estimated_error;        // total estimated error
    float d_estimated_error_per_sample; // total estimated error / fft_length

  public:
    /*! \return fine frequency error estimate in Hz */
    float ffe_estimate() { return d_estimated_error_per_sample*d_sample_rate/(2*M_PI); }
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_OFDM_FFS_SAMPLE_H */
