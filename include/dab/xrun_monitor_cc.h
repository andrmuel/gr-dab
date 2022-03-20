/* -*- c++ -*- */
/* 
 * Copyright 2018 Ruben Undheim <ruben.undheim@gmail.com>
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


#ifndef INCLUDED_DAB_XRUN_MONITOR_CC_H
#define INCLUDED_DAB_XRUN_MONITOR_CC_H

#include <dab/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dab {

    /*!
     * \brief <+description of block+>
     * \ingroup grdab
     *
     */
    class DAB_API xrun_monitor_cc : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<xrun_monitor_cc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of grdab::xrun_monitor_cc.
       *
       * To avoid accidental use of raw pointers, grdab::xrun_monitor_cc's
       * constructor is in a private implementation
       * class. grdab::xrun_monitor_cc::make is the public interface for
       * creating new instances.
       */
      static sptr make(int length=500000);

      virtual void set_drop_when_full(bool val)=0;
      virtual void stop_until_tag()=0;
      virtual void set_report_fill(bool)=0;
    };

  } // namespace dab
} // namespace gr

#endif /* INCLUDED_DAB_XRUN_MONITOR_CC_H */

