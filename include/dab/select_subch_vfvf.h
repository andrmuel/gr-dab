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


#ifndef INCLUDED_DAB_SELECT_SUBCH_VFVF_H
#define INCLUDED_DAB_SELECT_SUBCH_VFVF_H

#include <dab/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dab {

/*! \brief selects vectors out of input vectors that belong to one subchannel
 *
 * input:  float vector of size vlen_in
 *
 * output: float vector of size vlen_out
 *
 * selects vlen_out/vlen_in vectors of total_size input vectors, beginning at address
 *
 * @param vlen_in Length of input vector in floats.
 * @param vlen_out Length of output vector in floats.
 * @param address number of input vector where output the output vector begins
 * @param total_size size in input vectors of one frame (dumped after output vector is selected)
 */
    class DAB_API select_subch_vfvf : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<select_subch_vfvf> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dab::select_subch_vfvf.
       *
       * To avoid accidental use of raw pointers, dab::select_subch_vfvf's
       * constructor is in a private implementation
       * class. dab::select_subch_vfvf::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned int vlen_in, unsigned int vlen_out, unsigned int address, unsigned int total_size);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_SELECT_SUBCH_VFVF_H */

