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

#include <stdio.h>

#include <gnuradio/io_signature.h>
#include "fib_sink_vb_impl.h"
#include <stdexcept>
#include "crc16.h"
#include "FIC.h"

namespace gr {
    namespace dab {

        fib_sink_vb::sptr
        fib_sink_vb::make() {
            return gnuradio::get_initial_sptr
                    (new fib_sink_vb_impl());
        }


        fib_sink_vb_impl::fib_sink_vb_impl()
                : gr::sync_block("fib_sink_vb",
                                 gr::io_signature::make(1, 1, sizeof(char) * 32),
                                 gr::io_signature::make(0, 0, 0)) {
        }

        void
        fib_sink_vb_impl::dump_fib(const char *fib) {
            printf("FIB dump: ");
            for (int i = 0; i < FIB_LENGTH; i++)
                printf("%.2x ", (uint8_t) fib[i]);
            printf("\n");
        }

        int
        fib_sink_vb_impl::process_fib(const char *fib) {
            uint8_t type, length, pos;
            if (crc16(fib, FIB_LENGTH, FIB_CRC_POLY, FIB_CRC_INITSTATE) != 0) {
                fprintf(stderr, "FIB CRC error\n");
                return 1;
            }
            printf("FIB correct: processing FIGs..................................................................................................\n");
            pos = 0;
            while (pos < FIB_LENGTH - FIB_CRC_LENGTH && (uint8_t) fib[pos] != FIB_ENDMARKER &&
                   (uint8_t) fib[pos] != 0) { //TODO correct?
                type = fib[pos] >> 5;
                length = fib[pos] & 0x1f;
                assert(pos + length <= FIB_LENGTH - FIB_CRC_LENGTH);
                assert(length != 0);
                process_fig(type, &fib[pos], length);
                pos += length + 1;
            }
            return 0;
        }

        int
        fib_sink_vb_impl::process_fig(uint8_t type, const char *data, uint8_t length) {
            uint8_t cn, oe, pd, extension;
            switch (type){
                case FIB_FIG_TYPE_MCI:
                    printf("\tFIG type 0: ");
                    extension = (uint8_t)(data[1] & 0x1f);
                    cn = (uint8_t)(data[1] & 0x80);
                    if(cn == 1) printf("[WARNING, INFO FOR FUTURE CONFIGURATION]: ");
                    oe = (uint8_t)(data[1] & 0x40);
                    if(cn == 1) printf("[WARNING, INFO FOR OTHER ENSEMBLE");
                    pd = (uint8_t)(data[1] & 0x20);
                    if(pd == 1) printf("[WARNING, LONG IDENTIFIER");

                    switch (extension){
                        case FIB_MCI_EXTENSION_ENSEMBLE_INFO: {
                            printf("ensemble info: ");
                            uint16_t ensemble_reference = (uint16_t) (data[2]&0x0f)<<8 | (uint8_t) data[3];
                            printf("reference %d ", ensemble_reference);
                            uint8_t change_flag = (uint8_t)((data[4] & 0xc0)>>6);
                            uint8_t occurrence_change = data[6];
                            if (change_flag != 0)
                                printf(", [CHANGE OF SUBCHANNEL OR SERVICE ORGA (%d)](at CIF %d) ", change_flag,
                                       occurrence_change);
                            uint8_t alarm_flag = (uint8_t)((data[4] & 0x20)>>5);
                            if (alarm_flag == 1) printf(", [ALARM MESSAGE ACCESSIBLE] ");
                            uint16_t CIF_counter = (uint16_t)((data[4] & 0x1f) * 250 + (data[5]));
                            printf(", CIF counter = %d", CIF_counter);
                            printf("\n");
                            break;
                        }
                        case FIB_MCI_EXTENSION_SUBCHANNEL_ORGA: {
                            uint8_t subch_counter = 0;
                            printf("subchannel orga: ");
                            do{
                                uint8_t subchID = (uint8_t)((data[2+subch_counter]&0xfc)>>2);
                                printf("\n\t\t\t\tsubchID = %d ", subchID);
                                uint16_t start_adress = (uint16_t)((data[2+subch_counter]&0x03)<<8) | (uint8_t)(data[3+subch_counter]);
                                printf(", start adress = %d", start_adress);
                                uint8_t sl_form = (uint8_t)(data[4]&0x80);
                                if(sl_form == 0) {
                                    uint8_t table_switch = (uint8_t)(data[4+subch_counter]&0x40);
                                    if(table_switch != 0) printf(" [WARNING: OTHER TABLE USED] ");
                                    uint8_t table_index = (uint8_t)(data[4+subch_counter]&0x3f);
                                    printf(", index %d", table_index);
                                    subch_counter += 3;
                                }
                                else{
                                    uint8_t option = (uint8_t)(data[4+subch_counter]&0x70);
                                    uint8_t protect_level = (uint8_t)((data[4+subch_counter]&0x0c)>>2);
                                    uint16_t subch_size = (uint16_t)((data[4+subch_counter]&0x03)<<8) | (uint8_t)(data[5+subch_counter]);
                                    printf(", option %d, protect level %d, subch size %d", option, protect_level, subch_size);
                                    subch_counter += 4;
                                }
                            }while(1 + subch_counter < length);
                            printf("\n");
                            break;
                        }
                        case FIB_MCI_EXTENSION_SERVICE_ORGA: {
                            uint8_t service_counter = 1;
                            printf("service orga: ");
                            do { //iterate over services
                                uint16_t service_reference = (uint16_t)(data[service_counter+1]&0x0f)<<8 | (uint8_t)data[service_counter+2];
                                printf("\n\t\treference %d ", service_reference);
                                uint8_t local_flag = (uint8_t)((data[service_counter+3] & 0x80)>>7);
                                if (local_flag == 1) printf(", [LOCAL FLAG SET] ");
                                uint8_t ca = (uint8_t)((data[service_counter+3] & 0x70)>>4);
                                if (ca != 0) printf(", [CONDITIONAL ACCESS USED] ");
                                uint8_t num_service_comps = (uint8_t)(data[service_counter+3] & 0x0f);
                                printf(" (%d components):", num_service_comps);
                                for (int i = 0; i < num_service_comps; i++) { //iterate over service components
                                    uint8_t TMID = (uint8_t)((data[service_counter+4 + i * 2] & 0xc0)>>6);
                                    uint8_t comp_type = (uint8_t)(data[service_counter+4 + i * 2] & 0x3f);
                                    uint8_t subchID = (uint8_t)((data[service_counter+5 + i * 2] & 0xfc)>>2);
                                    uint8_t ps = (uint8_t)((data[service_counter+5 + i * 2 + 1] & 0x02)>>1);
                                    if (TMID == 0)
                                        printf("\n\t\t\t\t(audio stream, type %d, subchID %d, primary %d)", comp_type, subchID, ps);
                                    else if (TMID == 1)
                                        printf("\n\t\t\t\t(data stream, type %d, subchID %d, primary %d)", comp_type, subchID, ps);
                                    else if (TMID == 2)
                                        printf("\n\t\t\t\t(FIDC, type %d, subchID %d, primary %d)", comp_type, subchID, ps);
                                    else printf("\n\t\t\t\t[packed data]");
                                }
                                service_counter += 3 + 2*num_service_comps;
                            }while(service_counter < length);
                            printf("\n");
                            break;
                        }
                        case FIB_MCI_EXTENSION_SERVICE_ORGA_PACKET_MODE:
                            printf("service orga packet mode \n");
                            break;
                        case FIB_MCI_EXTENSION_SERVICE_ORGA_CA:
                            printf("service orga conditional access \n");
                            break;
                        case FIB_SI_EXTENSION_SERVICE_COMP_LANGUAGE:
                            printf("service comp language \n");
                            break;
                        case FIB_MCI_EXTENSION_SERVICE_COMP_GLOBAL_DEFINITION: {
                            printf("service component global definition: ");
                            uint8_t service_comp_counter = 0;
                            do{
                                uint16_t service_reference = (uint16_t)(data[service_comp_counter+2]&0x0f)<<8 | (uint8_t)data[service_comp_counter+3];
                                printf("reference %d ", service_reference);
                                uint8_t SCIdS = (uint8_t)(data[service_comp_counter+4]&0x0f);
                                printf(", SCIdS = %d", SCIdS);
                                if(data[service_comp_counter+5]&0x80 == 0){
                                    uint8_t subchID = (uint8_t)(data[service_comp_counter+5]&0x3f);
                                    printf(", subchID = %d", subchID);
                                    service_comp_counter += 5;
                                } else{
                                    uint16_t subchID = (uint16_t)(data[service_comp_counter+5]&0x0f)<<8 | (uint8_t)data[service_comp_counter+6];
                                    printf(", subchID %d ", subchID);
                                    service_comp_counter += 6;
                                }
                                printf(" | ");
                            }while(1 + service_comp_counter < length);
                            printf("\n");
                            break;
                        }
                        case FIB_SI_EXTENSION_COUNTRY_LTO:
                            printf("country LTO \n");
                            break;
                        case FIB_SI_EXTENSION_USER_APPLICATION_INFO:
                            printf("user application info \n");
                            break;
                        case FIB_MCI_EXTENSION_SUBCHANNEL_PACKET_MODE_FEC:
                            printf("subchannel orga packet mode fec \n");
                            break;
                        case FIB_SI_EXTENSION_PROGRAMME_NUMBER:
                            printf("programme number \n");
                            break;
                        case FIB_SI_EXTENSION_PROGRAMME_TYPE:
                            printf("programme type \n");
                            break;
                        case FIB_SI_EXTENSION_ANNOUNCEMENT_SUPPORT:
                            printf("announcement support \n");
                            break;
                        case FIB_SI_EXTENSION_ANNOUNCEMENT_SWITCHING:
                            printf("announcement switching \n");
                            break;
                        default:
                            printf("unsupported extension (%d) \n", extension);
                            break;
                    }
                    break;
                case FIB_FIG_TYPE_LABEL1:
                case FIB_FIG_TYPE_LABEL2:
                    printf("\tFIG type 2: ");
                    char label[16];
                    extension = (uint8_t)(data[1] & 0x07);
                    switch (extension){
                        case FIB_SI_EXTENSION_ENSEMBLE_LABEL:
                            memcpy(label, &data[4], 16);memcpy(label, &data[4], 16);
                            printf("[ensemble label]: %s \n", label);
                            break;
                        case FIB_SI_EXTENSION_PROGRAMME_SERVICE_LABEL: {
                            uint16_t service_reference = (uint16_t)(data[2] & 0x0f) << 8 | (uint8_t) data[3];
                            memcpy(label, &data[4], 16);
                            printf("[programme service label] (reference %d): %s \n", service_reference, label);
                            break;
                        }
                        case FIB_SI_EXTENSION_SERVICE_COMP_LABEL:
                            memcpy(label, &data[5], 16);
                            printf("[service component label] %s\n", label);
                            break;
                        case FIB_SI_EXTENSION_DATA_SERVICE_LABEL:
                            memcpy(label, &data[5], 16);
                            printf("[data service label]: %s \n", label);
                            break;
                        default:
                            printf("[unknown extension (%d) \n", extension);
                            break;
                    }
                    break;
                case FIB_FIG_TYPE_FIDC:
                    printf("\tFIG type 5: ");
                    extension = (uint8_t)(data[1] & 0x07);
                    switch (extension) {
                        case FIB_FIDC_EXTENSION_PAGING:
                            printf("paging - not supported yet\n");
                            break;
                        case FIB_FIDC_EXTENSION_TMC:
                            printf("TMC (traffic message channel) - not supported yet\n");
                            break;
                        case FIB_FIDC_EXTENSION_EWS:
                            printf("EWS (emergency warning service) - not supported yet\n");
                            break;
                        default:
                            printf("unsupported extension (%d)\n", extension);
                    }
                    break;
                case FIB_FIG_TYPE_CA:
                    printf("\tFIB type CA (conditional access) not supported yet\n");
                    break;
                default:
                    printf("\tunsupported FIG type\n");
                    break;
            }
            return 0;
        }

        int
        fib_sink_vb_impl::work(int noutput_items,
                               gr_vector_const_void_star &input_items,
                               gr_vector_void_star &output_items) {
            const char *in = (const char *) input_items[0];

            for (int i = 0; i < noutput_items; i++) {
                // dump_fib(in);
                process_fib(in);
                in += 32;
            }

            return noutput_items;
        }

    }
}
