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


#ifndef INCLUDED_DAB_VALVE_FF_H
#define INCLUDED_DAB_VALVE_FF_H

#include <dab/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dab {

    /*!
     * \brief lets samples pass or not depending on the state of closed
     * \ingroup dab
     *
     */
    class DAB_API valve_ff : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<valve_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dab::valve_ff.
       *
       * To avoid accidental use of raw pointers, dab::valve_ff's
       * constructor is in a private implementation
       * class. dab::valve_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool closed, bool feed_with_zeros = false);
      virtual void set_closed(bool closed) = 0;
      virtual void set_feed_with_zeros(bool feed_with_zeros) = 0;
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_VALVE_FF_H */

