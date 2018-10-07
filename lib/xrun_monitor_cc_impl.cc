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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "xrun_monitor_cc_impl.h"

namespace gr {
  namespace dab {

    xrun_monitor_cc::sptr
    xrun_monitor_cc::make(int length)
    {
      return gnuradio::get_initial_sptr
        (new xrun_monitor_cc_impl(length));
    }

    /*
     * The private constructor
     */
    xrun_monitor_cc_impl::xrun_monitor_cc_impl(int length)
      : gr::block("xrun_monitor_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
        d_n = 0;
        d_produce_per = 100;
        d_write_index = 0;
        d_read_index = 0;
        d_length = length;
        d_buffer = new gr_complex[d_length];
        d_first = true;
        d_starting = true;
        d_drop_when_full = false;
        d_stop_until_tag = false;
        d_report_fill = true;
    }

    /*
     * Our virtual destructor.
     */
    xrun_monitor_cc_impl::~xrun_monitor_cc_impl()
    {
        delete(d_buffer);
    }

    void
    xrun_monitor_cc_impl::set_drop_when_full(bool val)
    {
        d_drop_when_full = val;
    }

    void
    xrun_monitor_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        if (noutput_items >= 10) {
            ninput_items_required[0] = noutput_items;
        }
        else {
            int current_fill;
            if (d_read_index < d_write_index)
                current_fill = d_write_index - d_read_index;
            else if (d_read_index == d_write_index)
                current_fill = 0;
            else
                current_fill = d_length - d_read_index + d_write_index;

            float fill_percentage = (((float)current_fill)/((float)d_length))*100;
            if(fill_percentage > 10 || d_starting) {
                ninput_items_required[0] = 0;
            }
            else {
                ninput_items_required[0] = noutput_items;
                d_starting = true;
                printf("Fill fell below 10%% Starting again\n");
            }
        }

    }

    void
    xrun_monitor_cc_impl::set_report_fill(bool val)
    {
        d_report_fill = val;
    }

    void
    xrun_monitor_cc_impl::stop_until_tag()
    {
        gr::thread::scoped_lock lock(common_mutex);
        d_stop_until_tag = true;
        d_n = 0;
        d_write_index = 0;
        d_read_index = 0;
        d_first = true;
        d_starting = true;
    }

    int
    xrun_monitor_cc_impl::general_work(int noutput_items,
        gr_vector_int &ninput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = NULL;
      if (input_items.size() > 0)
        in  = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];

      gr::thread::scoped_lock lock(common_mutex);

      int end_pos = -1;
      if (d_stop_until_tag) {
        std::vector<tag_t> tags;
        get_tags_in_range(tags, 0, nitems_read(0), nitems_read(0) + ninput_items[0], pmt::mp("audio_start"));
        if (tags.size() > 0) {
          end_pos = tags[0].offset - nitems_read(0);
          d_stop_until_tag = false;
        }
        else {
          consume_each(ninput_items[0]);
          for(int i=0;i<noutput_items;i++) {
            out[i] = 0;
          }
          return noutput_items;
        }
      }
      if (end_pos > 0) {
        consume_each(end_pos);
        return 0;
      }

      // Do <+signal processing+>
      int zeros_to_produce = 0;
      int current_fill;
      if (d_read_index < d_write_index)
        current_fill = d_write_index - d_read_index;
      else if (d_read_index == d_write_index)
        current_fill = 0;
      else {
        current_fill = d_length - d_read_index + d_write_index;
      }
      float fill_percentage;
      fill_percentage = (((float)current_fill)/((float)d_length))*100;
      if (d_starting && fill_percentage < 75) {
        zeros_to_produce = noutput_items;
        noutput_items = 0;
      }
      else {
        d_starting = false;
      }

      if (d_first && ninput_items[0] > 0) {
        printf("xrun_monitor received first samples (%d). Waiting to fill up buffer..\n" , ninput_items[0]);
        d_first = false;
      }

      int produced = 0;
      int consumed = 0;
      int remaining;
      int to_produce_here;
      int toread;
      int outpos = 0;

      if (d_read_index < d_write_index) {
        toread = d_write_index - d_read_index;
        to_produce_here = std::min(toread, noutput_items);
        memcpy(out, d_buffer + d_read_index, sizeof(gr_complex) * to_produce_here);
        d_read_index += to_produce_here;
        remaining = noutput_items - to_produce_here;
        outpos = to_produce_here;
        produced += to_produce_here;
      }
      else if (d_read_index == d_write_index){
        remaining = noutput_items;
        outpos = 0;
      }
      else {
        toread = d_length - d_read_index;
        to_produce_here = std::min(toread, noutput_items);
        memcpy(out, d_buffer + d_read_index, sizeof(gr_complex) * to_produce_here);
        remaining = noutput_items - to_produce_here;
        produced += to_produce_here;
        if (remaining > 0) {
            int to_produce_here2 = std::min(d_write_index, remaining);
            memcpy(out+to_produce_here, d_buffer, sizeof(gr_complex) * to_produce_here2);
            d_read_index = to_produce_here2;
            remaining = remaining - to_produce_here2;
            outpos = to_produce_here + to_produce_here2;
            produced += to_produce_here2;
        }
        else if (remaining == 0) {
            if ((d_read_index + to_produce_here ) < d_length)
                d_read_index += to_produce_here;
            else
                d_read_index = 0;
            outpos = to_produce_here;
        }
        else {
            outpos = to_produce_here;
            d_read_index += to_produce_here;
        }
      }

      int to_produce = std::min(ninput_items[0], remaining);
      memcpy(out+outpos, in, sizeof(gr_complex) * to_produce);
      produced += to_produce;
      consumed += to_produce;
      //if ((to_produce_here + to_produce) <= d_length) {
      //}
      //else {
      //    memcpy(out+to_produce_here, in, sizeof(gr_complex) * (d_length - (to_produce_here + to_produce)));
      //    memcpy(out+to_produce_here, in, sizeof(gr_complex) * (d_length - (to_produce_here + to_produce)));
      //}
      int tosave = ninput_items[0] - (to_produce);

      if (d_read_index < d_write_index)
        current_fill = d_write_index - d_read_index;
      else if (d_read_index == d_write_index)
        current_fill = 0;
      else {
        current_fill = d_length - d_read_index + d_write_index;
      }

      if(tosave >= (d_length-current_fill)) {
        tosave = d_length - current_fill - 1;
      }

      if ((d_write_index + tosave) < d_length) {
        memcpy(d_buffer + d_write_index, in + to_produce, sizeof(gr_complex) * tosave);
        d_write_index = d_write_index + tosave;
      }
      else {
        memcpy(d_buffer + d_write_index, in + to_produce, sizeof(gr_complex) * (d_length - d_write_index));
        memcpy(d_buffer, in + to_produce + (d_length - d_write_index), sizeof(gr_complex) * (tosave - (d_length - d_write_index)));
        d_write_index = tosave - (d_length - d_write_index);
      }
      consumed += tosave;

      d_n += noutput_items;


      if (d_read_index < d_write_index)
        current_fill = d_write_index - d_read_index;
      else if (d_read_index == d_write_index)
        current_fill = 0;
      else {
        current_fill = d_length - d_read_index + d_write_index;
      }

        if (d_n > 10000) {
            //printf("ninput_items: %d, noutput_items: %d\n", ninput_items[0], noutput_items);
            if (d_report_fill)
                printf("Fill: %f %\n", (((float)current_fill)/((float)d_length))*100);
            d_n = 0;
        }

      for(int i=0;i<zeros_to_produce;i++) {
        out[i] = 0;
        produced++;
      }

      if (d_drop_when_full)
        consume_each(ninput_items[0]);
      else
        consume_each(consumed);
      // Tell runtime system how many output items we produced.
      return produced;
    }

  } /* namespace dab */
} /* namespace gr */

