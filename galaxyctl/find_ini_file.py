#!/usr/bin/env python
''' Load INI Config File order(first found is used): ENV, /etc/ansible '''

import sys

def is_virtual():
    """ Return if we run in a virtual environtment. """
    # Check supports venv && virtualenv
    return (getattr(sys, 'base_prefix', sys.prefix) != sys.prefix or
            hasattr(sys, 'real_prefix'))

def find_ini_file():

  path='/etc/galaxyctl'
  
  if is_virtual() is True:
    path = sys.prefix + '/etc/galaxyctl/'

  ini_file = path + '/galaxyctl.ini'
  return ini_file
