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

#include <pthread.h>
#include <stdio.h>

#include <dab_concatenate_signals.h>
#include <gr_io_signature.h>

dab_concatenate_signals_sptr
dab_make_concatenate_signals (size_t itemsize)
{
  return gnuradio::get_initial_sptr (new dab_concatenate_signals (itemsize));
}

dab_concatenate_signals::dab_concatenate_signals (size_t itemsize)
  : gr_block ("concatenate_signals",
       gr_make_io_signature (1, -1, itemsize),
       gr_make_io_signature (1,  1, itemsize)),
    d_itemsize(itemsize), d_current_signal(0), d_callmetwice(1)
{
}

void 
dab_concatenate_signals::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
  unsigned int ninputs = ninput_items_required.size();
  // printf("noutput_items: %d\n", noutput_items);

  if (d_current_signal<ninputs) {
    for (unsigned i = 0; i < ninputs; i++)
      ninput_items_required[i] = (i==d_current_signal)?noutput_items-1:0; /* must be -1, so we get to zero at the end of the stream */
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
  unsigned int ninputs = input_items.size ();
  int produced;

  // for (unsigned int i=0; i < ninputs; i++) 
  //   printf("input %d: has %d items\n", i, ninput_items[i]);
  // printf("current signal: %d\n", d_current_signal);

  if (d_current_signal == ninputs) /* no more streams - finished */
    return -1;

  if (ninput_items[d_current_signal]==0) { /* no more input - go to next stream */
    if (d_callmetwice == 0) /* workaround: general_work gets called with no inputs right at the start in any case */
      d_current_signal++;
    else 
      d_callmetwice--;
    // sched_yield(); [> let other threads run .. <]
    return 0;
  }

  d_callmetwice = 1;

  produced = (noutput_items<ninput_items[d_current_signal])?noutput_items:ninput_items[d_current_signal]; /* minimum */
  memcpy(output_items[0], input_items[d_current_signal], produced*d_itemsize);

  for (unsigned int i=0; i<ninputs; i++)
    consume(i,(i==d_current_signal)?produced:0);

  return produced;
}
