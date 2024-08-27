/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
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


#ifndef INCLUDED_DAB_MEASURE_PROCESSING_RATE_H
#define INCLUDED_DAB_MEASURE_PROCESSING_RATE_H

#include <dab/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace dab {

    /*!
     * \brief <+description of block+>
     * \ingroup dab
     *
     */
    class DAB_API measure_processing_rate : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<measure_processing_rate> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dab::measure_processing_rate.
       *
       * To avoid accidental use of raw pointers, dab::measure_processing_rate's
       * constructor is in a private implementation
       * class. dab::measure_processing_rate::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t itemsize, int samples_to_count);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_MEASURE_PROCESSING_RATE_H */

