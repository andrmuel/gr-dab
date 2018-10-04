#!/usr/bin/env python2

import channel_mapping

def get_number_of_channels():
  return len(channel_mapping.table)

def id_to_frequency(i):
  frequency_mhz = float(channel_mapping.table[int(i)]['frequency'])
  print(frequency_mhz)
  return frequency_mhz*1e6
