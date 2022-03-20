/* -*- c++ -*- */
/* 
 * Copyright 2017Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
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


#ifndef INCLUDED_DAB_CRC16_BB_H
#define INCLUDED_DAB_CRC16_BB_H

#include <dab/api.h>
#include <gnuradio/block.h>

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
    class DAB_API crc16_bb : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<crc16_bb> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dab::crc16_bb.
       *
       * To avoid accidental use of raw pointers, dab::crc16_bb's
       * constructor is in a private implementation
       * class. dab::crc16_bb::make is the public interface for
       * creating new instances.
       */
      static sptr make(int length, uint16_t generator, uint16_t initial_state);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_CRC16_BB_H */

