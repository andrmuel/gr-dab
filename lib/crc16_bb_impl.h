/* -*- c++ -*- */
/*
 * Copyright 2017 by Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_DAB_CRC16_BB_IMPL_H
#define INCLUDED_DAB_CRC16_BB_IMPL_H

#include <dab/crc16_bb.h>

namespace gr {
  namespace dab {
/*! \brief crc16 is written in the last 2 bits of input vector
 *
 * input:  char vector of length length (packed bytes)
 *
 * output: char vector of length length (packed bytes) with crc at last 2 bytes (overwrites last 2 bytes)
 *
 * uses the crc16 function to calculate a 2 byte crc word and write it to the FIB (overwrites last 2 bytes)
 *
 * @param length Length of input and output vector in bytes. (default is 32 for DAB FIBs)
 * @param generator Generator polynom for shift register. (default is 0x1021 for DAB)
 * @param initial_state Initial state of shift register. (default is 0xffff for DAB)
 */
    class crc16_bb_impl : public crc16_bb {
    private:
      uint16_t d_crc;
      int d_length, d_generator, d_initial_state;

    public:
      crc16_bb_impl(int length, uint16_t generator, uint16_t initial_state);

      ~crc16_bb_impl();

      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);
    };

  }
}

#endif /* INCLUDED_DAB_CRC16_BB_IMPL_H */
