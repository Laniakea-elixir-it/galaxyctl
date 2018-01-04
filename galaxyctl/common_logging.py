#!/usr/bin/env python
''' Common logging options '''

import logging

from .find_ini_file import find_ini_file
from .read_ini_file import read_ini_file

def set_log(log_level):

  galaxyctl_log_file = read_ini_file(find_ini_file('galaxyctl.ini'), 'galaxy', 'galaxyctl_log_file')

  log = logging.getLogger(__name__)

  lv = getattr(logging, log_level)

  logging.basicConfig(filename=galaxyctl_log_file, format='%(levelname)s %(asctime)s %(message)s', level=lv)

  return log
