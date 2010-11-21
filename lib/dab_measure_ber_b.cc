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

#include <dab_measure_ber_b.h>
#include <gr_io_signature.h>
#include <stdexcept>

dab_measure_ber_b_sptr
dab_make_measure_ber_b ()
{
  return gnuradio::get_initial_sptr (new dab_measure_ber_b ());
}

dab_measure_ber_b::dab_measure_ber_b()
  : gr_sync_block ("measure_ber_b",
		   gr_make_io_signature2(2, 2, sizeof(char), sizeof(char)),
		   gr_make_io_signature(0, 0, 0)),
    d_bytes(0), d_errors(0)
{
}

unsigned int dab_measure_ber_b::bits_set(char byte) {
  char bits = 0;
  for (int i=0; i<8; i++) 
    if (byte&(1<<i))
      bits++;
  return bits;
}

int 
dab_measure_ber_b::work (int noutput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items)
{
  const char *in0 = (const char *) input_items[0];
  const char *in1 = (const char *) input_items[1];
  
  for (int i=0; i<noutput_items; i++) 
    d_errors += bits_set((*in0++) ^ (*in1++));

  d_bytes += noutput_items;
  
  return noutput_items;
}
