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
    d_current_signal(0), d_callmetwice(1)
{
}

void 
dab_concatenate_signals::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
  int in_req  = noutput_items;
  unsigned ninputs = ninput_items_required.size ();

  if (d_current_signal<ninputs) {
    for (unsigned i = 0; i < ninputs; i++)
        ninput_items_required[i] = (i==d_current_signal)?in_req-1:0; /* must be -1, so we get to zero at the end of the stream */
  } else { /* no more streams left -> make sure the scheduler notices it */
    for (unsigned i = 0; i < ninputs; i++)
        ninput_items_required[i] = noutput_items;
  }
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

  // for (i=0; i < ninputs; i++) 
  //   printf("input %d: has %d items\n", i, ninput_items[i]);

  if (d_current_signal==ninputs) /* no more streams - finished */
    return -1;

  if (ninput_items[d_current_signal]==0) { /* no more input - go to next stream */
    if (d_callmetwice == 0) /* workaround: general_work gets called with no inputs rigth at the start in any case */
      d_current_signal++;
    else 
      d_callmetwice=0;
    return 0;
  }

  d_callmetwice=1;

  for (i=0; (i<noutput_items) && (i<ninput_items[d_current_signal]); i++) 
    *optr++ = ((gr_complex *) input_items[d_current_signal])[i];

  consume(d_current_signal,i);
  return i;
}
