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


#ifndef INCLUDED_DAB_TIME_DEINTERLEAVE_FF_H
#define INCLUDED_DAB_TIME_DEINTERLEAVE_FF_H

#include <dab/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace dab {

/*! \brief applies time deinterleaving to a vector
 *
 * applies time deinterleaving to a vector with its arg_max[scrambling_vector] predecessors, the scrambling_vector describes which vector element comes from which predecessors
 *
 * @param vector_length length of input vectors
 * @param scrambling_vector vector with scrambling parameters (see DAB standard p.138)
 *
 */
    class DAB_API time_deinterleave_ff : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<time_deinterleave_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dab::time_deinterleave_ff.
       *
       * To avoid accidental use of raw pointers, dab::time_deinterleave_ff's
       * constructor is in a private implementation
       * class. dab::time_deinterleave_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(int vector_length, const std::vector<unsigned char> &scrambling_vector);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_TIME_DEINTERLEAVE_FF_H */

