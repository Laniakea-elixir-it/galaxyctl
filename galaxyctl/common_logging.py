#!/usr/bin/env python
''' Common logging options '''

import logging

from .find_ini_file import find_ini_file
from .read_ini_file import read_ini_file

def set_log():

  galaxyctl_config_file = find_ini_file('galaxyctl.ini')

  galaxyctl_log_file = read_ini_file(galaxyctl_config_file, 'galaxy', 'galaxyctl_log_file')

  log_level = read_ini_file(galaxyctl_config_file, 'galaxy', 'log_level')

  log = logging.getLogger(__name__)

  lv = getattr(logging, log_level)

  logging.basicConfig(filename=galaxyctl_log_file, format='%(levelname)s %(asctime)s %(message)s', level=lv)

  return log
