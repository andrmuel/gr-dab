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


#ifndef INCLUDED_DAB_OFDM_SAMPLER_H
#define INCLUDED_DAB_OFDM_SAMPLER_H

#include <dab/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dab {

    /*!
     * \brief <+description of block+>
     * \ingroup dab
     *
     */
    class DAB_API ofdm_sampler : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<ofdm_sampler> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dab::ofdm_sampler.
       *
       * To avoid accidental use of raw pointers, dab::ofdm_sampler's
       * constructor is in a private implementation
       * class. dab::ofdm_sampler::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned int fft_length, unsigned int cp_length, unsigned int symbols_per_frame,unsigned int gap);
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_OFDM_SAMPLER_H */

