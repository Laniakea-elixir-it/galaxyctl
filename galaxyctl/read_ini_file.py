#!/usr/bin/env python

try:
  import ConfigParser
except ImportError:
  import configparse

def read_ini_file(config_file, section, option):

  configParser = ConfigParser.RawConfigParser()
  configParser.readfp(open(config_file))
  configParser.read(config_file)

  if configParser.has_option(section, option):
    config = configParser.get(section , option)
    return config
  else:
    raise Exception('No %s section with %s option in %s' % (section, option, config_file))
