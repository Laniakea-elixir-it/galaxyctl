#!/usr/bin/env python
"""
"""

# Imports
from flask import Flask, jsonify, request
import subprocess
import json, requests
import os, sys
from os.path import exists, pathsep
from string import split


# Create logging facility
import logging
logging.basicConfig(filename='/var/log/galaxy/galaxyctl-api.log', format='%(levelname)s %(asctime)s %(message)s', level='DEBUG')


#______________________________________
def exec_cmd(cmd):

  proc = subprocess.Popen( args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
  communicateRes = proc.communicate()
  stdOutValue, stdErrValue = communicateRes
  status = proc.wait()

  return status, stdOutValue, stdErrValue

#______________________________________
def which(name):

  PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

  for path in PATH.split(os.path.pathsep):
    full_path = path + os.sep + name
    if os.path.exists(full_path):
      return str(full_path)

#______________________________________
def galaxy_startup(endpoint):

  command = which('sudo') + ' /usr/local/bin/galaxy-startup'

  print(command)

  status, stdout, stderr = exec_cmd(command)

  logging.debug( 'Startup stdout: ' + str(stdout) )
  logging.debug( 'Startup stderr: ' + str(stderr) )
  logging.debug( 'Startup status: ' + str(status) )

  response = requests.get(endpoint, verify=False)

  sc = str(response.status_code)

  if sc == '200' or sc == '302':
     return jsonify({'galaxy': 'online' })

  else:
    return jsonify({'galaxy': 'unavailable'})
