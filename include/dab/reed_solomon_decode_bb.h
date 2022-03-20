/* -*- c++ -*- */
/* 
 * Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
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


#ifndef INCLUDED_DAB_REED_SOLOMON_DECODE_BB_H
#define INCLUDED_DAB_REED_SOLOMON_DECODE_BB_H

#include <dab/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dab {

    /*!
     * \brief Reed-Solomon decoder configured for DAB+
     * \ingroup dab
     *
     */
    class DAB_API reed_solomon_decode_bb : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<reed_solomon_decode_bb> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dab::reed_solomon3_bb.
       *
       * To avoid accidental use of raw pointers, dab::reed_solomon3_bb's
       * constructor is in a private implementation
       * class. dab::reed_solomon3_bb::make is the public interface for
       * creating new instances.
       */
      static sptr make(int bit_rate_n);
      
      virtual int get_corrected_errors() = 0;
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_REED_SOLOMON_DECODE_BB_H */

