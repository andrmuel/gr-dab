/* -*- c++ -*- */
/*
 * Copyright 2008 Free Software Foundation, Inc.
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

#include <dab_concatenate_signals_cc.h>
#include <gr_io_signature.h>

dab_concatenate_signals_sptr
dab_make_concatenate_signals ()
{
  return dab_concatenate_signals_sptr (new dab_concatenate_signals ());
}

dab_concatenate_signals::dab_concatenate_signals ()
  : gr_block ("concatenate_signals_cc",
       gr_make_io_signature (1, -1, sizeof (gr_complex)),
       gr_make_io_signature (1,  1, sizeof (gr_complex))),
    d_current_signal(0), d_next(0)
{
}

void 
dab_concatenate_signals::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
  unsigned ninputs = ninput_items_required.size ();

  if (d_next==1) {
    if (d_current_signal<ninputs-1) {
      d_next = 0;
      d_current_signal++;
    }
  }


  for (unsigned i = 0; i < ninputs; i++)
    ninput_items_required[i] = 0;
  ninput_items_required[d_current_signal] = noutput_items;

  for (unsigned i = 0; i < ninputs; i++)
    printf("ninput_items_required[%d]: %d\n", i, ninput_items_required[i]);

  printf("forecast: noutput_items: %d\n", noutput_items);
  printf("forecast: current_signal: %d\n\n", d_current_signal);

  if (noutput_items==1)
      d_next = 1;
}

int
dab_concatenate_signals::general_work(int noutput_items,
              gr_vector_int &ninput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items)
{
  gr_complex *optr = (gr_complex *) output_items[0];

  int ninputs = input_items.size ();
  int i;

  for (i=0; i < ninputs; i++) 
    printf("input %d: has %d items\n", i, ninput_items[i]);

  for (i=0; (i<noutput_items) && (i<ninput_items[d_current_signal]); i++) 
    *optr++ = ((gr_complex *) input_items[d_current_signal])[i];

  consume(d_current_signal,i);
  return i;
}
