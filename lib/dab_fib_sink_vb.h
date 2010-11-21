/* -*- c++ -*- */
/*
 * Copyright 2004,2007 Free Software Foundation, Inc.
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

#ifndef INCLUDED_DAB_FIB_SINK_B_H
#define INCLUDED_DAB_FIB_SINK_B_H

#include <gr_sync_block.h>

class dab_fib_sink_vb;
typedef boost::shared_ptr<dab_fib_sink_vb> dab_fib_sink_vb_sptr;

dab_fib_sink_vb_sptr dab_make_fib_sink_vb();

/*!
 * \brief sink for DAB FIBs
 *
 * input: port 0: fibs
 *
 * \ingroup sink
 */
class dab_fib_sink_vb : public gr_sync_block
{
  friend dab_fib_sink_vb_sptr dab_make_fib_sink_vb();

 private:
  unsigned long d_fibs; 
  void dump_fib(const char *fib);
  int process_fib(const char *fib);
  int process_fig(uint8_t type, const char *data, uint8_t length);

 protected:
  dab_fib_sink_vb();

 public:
  int work(int noutput_items,
	   gr_vector_const_void_star &input_items,
	   gr_vector_void_star &output_items);
};

#endif /* INCLUDED_DAB_FIB_SINK_B_H */
