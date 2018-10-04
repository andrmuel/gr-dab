#!/usr/bin/env python2

import channel_mapping

def get_number_of_channels():
  return len(channel_mapping.table)

def id_to_frequency(i):
  frequency = float(channel_mapping.table[int(i)]['frequency'])*1e6
  print(frequency)
  return frequency
