/* -*- c++ -*- */
/*
 * Copyright belongs to Andreas Mueller
 * Modified 2017 by Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
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
#ifndef INCLUDED_DAB_FIB_SINK_VB_IMPL_H
#define INCLUDED_DAB_FIB_SINK_VB_IMPL_H

#include <dab/fib_sink_vb.h>

namespace gr {
  namespace dab {
/*! \brief sink for DAB FIBs, interprets MSC and SI
 *
 */
    class fib_sink_vb_impl : public fib_sink_vb {

    private:
      int process_fib(const char *fib);

      int process_fig(uint8_t type, const char *data, uint8_t length);

      bool d_crc_passed;

      std::string d_json_ensemble_info;
      // service info
      std::string d_json_service_info;
      std::string d_service_info_current;
      int d_service_info_written_trigger;
      // service labels
      std::string d_json_service_labels;
      std::string d_service_labels_current;
      int d_service_labels_written_trigger;
      // service subch
      std::string d_json_subch_info;
      std::string d_subch_info_current;
      int d_subch_info_written_trigger;
      // programme type
      std::string d_json_programme_type;
      std::string d_programme_type_current;
      int d_programme_type_written_trigger;


      bool d_print_channel_info;

    public:
      fib_sink_vb_impl();

      virtual std::string get_ensemble_info()
      { return d_json_ensemble_info; }

      virtual std::string get_service_info()
      { return d_json_service_info;}

      virtual std::string get_service_labels()
      { return d_json_service_labels;}

      virtual std::string get_subch_info()
      { return d_json_subch_info;}

      virtual std::string get_programme_type()
      { return d_json_programme_type;}

      virtual bool get_crc_passed()
      { return d_crc_passed;}

      int work(int noutput_items,
               gr_vector_const_void_star &input_items,
               gr_vector_void_star &output_items);
      void set_print_channel_info(bool val);
    };
  }
}

#endif /* INCLUDED_DAB_FIB_SINK_B_H */
