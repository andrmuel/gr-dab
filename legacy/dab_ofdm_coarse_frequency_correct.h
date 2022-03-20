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
#ifndef INCLUDED_DAB_OFDM_COARSE_FREQUENCY_CORRECT_H
#define INCLUDED_DAB_OFDM_COARSE_FREQUENCY_CORRECT_H

#include <gr_sync_block.h>

class dab_ofdm_coarse_frequency_correct;

typedef std::shared_ptr<dab_ofdm_coarse_frequency_correct> dab_ofdm_coarse_frequency_correct_sptr;

dab_ofdm_coarse_frequency_correct_sptr 
dab_make_ofdm_coarse_frequency_correct (unsigned int fft_length, 
                                        unsigned int num_carriers);

/*!
 * \brief Corrects coarse frequency offset in the frequency spectrum.
 * \ingroup DAB
 * 
 * \param fft_length total number of fft bins
 * \param num_carriers number of carriers with OFDM symbols, not including the zero carrier
 *
 * This block detects where the signal is (coarse frequency offset) by looking
 * at the energy and returns only the carriers containing information (i.e. it
 * removes the zeros on the left, the zeros on the right and the one zero
 * carrier in the middle). 
 */
class dab_ofdm_coarse_frequency_correct : public gr_sync_block
{
  private:
    // The friend declaration allows dab_make_ofdm_coarse_frequency_correct to
    // access the private constructor.

    friend dab_ofdm_coarse_frequency_correct_sptr
    dab_make_ofdm_coarse_frequency_correct (unsigned int fft_length, unsigned int num_carriers);

    float mag_squared(const gr_complex sample);
    dab_ofdm_coarse_frequency_correct (unsigned int fft_length, unsigned int num_carriers);    // private constructor
    void correlate_energy(const gr_complex *symbol);

    unsigned int d_fft_length;
    unsigned int d_num_carriers;
    unsigned int d_zeros_on_left;
    unsigned int d_freq_offset;

  public:
    int work (int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_OFDM_COARSE_FREQUENCY_CORRECT_H */
