#!/usr/bin/env python


import yaml
import os

class Configuration():

  def __init__(self, folder):
    self.folder = folder
    self.adjust_file_name = "".join([self.folder,"/adjustment.yaml"])
    self.adjust_config = {}
    self.read()


  def read(self):

    try:
      with open(self.adjust_file_name, 'r') as ymlfile:
        self.adjust_config = yaml.load(ymlfile)
    except IOError:
      pass
      

  def save(self):
    try:
      os.makedirs(self.folder)
    except OSError:
      pass # If already exists

    with open(self.adjust_file_name, 'w') as ymlfile:
      yamlcontent = yaml.dump(self.adjust_config)
      ymlfile.write(yamlcontent)

