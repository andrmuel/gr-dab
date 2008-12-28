/* -*- c++ -*- */
/*
 * Copyright 2004,2006,2007 Free Software Foundation, Inc.
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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <dab_fib_sink_b.h>
#include <gr_io_signature.h>
#include <stdexcept>

dab_fib_sink_b_sptr
dab_make_fib_sink_b ()
{
  return dab_fib_sink_b_sptr (new dab_fib_sink_b ());
}

dab_fib_sink_b::dab_fib_sink_b()
  : gr_sync_block ("fib_sink_b",
		   gr_make_io_signature(1, 1, sizeof(char)*32),
		   gr_make_io_signature(0, 0, 0))
{
}

int 
dab_fib_sink_b::work (int noutput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items)
{
  const char *in = (const char *) input_items[0];

  char label[17];
  
  /* TODO */

  for (int i=0; i<noutput_items; i++) {
    if (((char)in[0])>>5==1) {
      memcpy(label,&in[4],16);
      label[16]=0;
      printf("%s\n",label);
    }
    in+=32;

  }

  return noutput_items;
}
