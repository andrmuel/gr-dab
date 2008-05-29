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
#ifndef INCLUDED_DAB_OFDM_INSERT_PILOT_VCC_H
#define INCLUDED_DAB_OFDM_INSERT_PILOT_VCC_H

#include <gr_block.h>

class dab_ofdm_insert_pilot_vcc;

typedef boost::shared_ptr<dab_ofdm_insert_pilot_vcc> dab_ofdm_insert_pilot_vcc_sptr;

dab_ofdm_insert_pilot_vcc_sptr dab_make_ofdm_insert_pilot_vcc (const std::vector<gr_complex> &pilot);

/*!
 * \brief Inserts the pilot symbol at the start of each frame.
 * \ingroup DAB
 * \param pilot Complex vector containing the pilot OFDM symbol
 *
 * input: port 0: complex vectors with symbols; port 1: byte stream - signal indicating the start of a frame
 * output: port 0: complex vectors with symbols; port 1: byte stream - signal indicating the start of a frame
 *
 * The pilot symbol vector must have the same width as the other symbols
 */
class dab_ofdm_insert_pilot_vcc : public gr_block
{
  private:
    // The friend declaration allows dab_make_ofdm_insert_pilot_vcc to
    // access the private constructor.

    friend dab_ofdm_insert_pilot_vcc_sptr dab_make_ofdm_insert_pilot_vcc (const std::vector<gr_complex> &pilot);

    dab_ofdm_insert_pilot_vcc (const std::vector<gr_complex> &pilot);    // private constructor

    std::vector<gr_complex> d_pilot;
    char d_start;

  public:
    void forecast (int noutput_items, gr_vector_int &ninput_items_required);

    int general_work (int noutput_items,
                      gr_vector_int &ninput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_OFDM_INSERT_PILOT_VCC_H */
