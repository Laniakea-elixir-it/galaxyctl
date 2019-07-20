#!/usr/bin/env python
# ELIXIR-ITALY
# INDIGO-DataCloud
# IBIOM-CNR
#
# Contributors:
# author: Tangaro Marco
# email: ma.tangaro@ibiom.cnr.it
#
# Dependencies:
# uwsgi
# lsof

# Imports
import socket
import errno
import json
import os
import signal
import time
import subprocess
import platform

try:
  import ConfigParser
except ImportError:
  import configparser

# Log config
from .common_logging import set_log
logs = set_log()


####################################

class DetectGalaxyCommands:
  def __init__(self,init_system):
    self.init = init_system
    self.os, self.version, self.codename = platform.dist()

  #______________________________________
  def get_startup_command(self):
    if self.init == 'supervisord':
      if self.os == 'centos': return 'supervisord -c /etc/supervisord.conf'
      if self.os == 'Ubuntu': return 'supervisord -c /etc/supervisor/supervisord.conf'
    elif self.init == 'init':
      if self.os == 'centos': return 'systemctl start galaxy.service'
      if self.os == 'Ubuntu' and self.codename == 'xenial': return 'systemctl start galaxy.service'
      if self.os == 'Ubuntu' and self.codename == 'trusty': return 'service galaxy start'

  #______________________________________
  def get_stop_command(self):
    if self.init == 'supervisord': return 'supervisorctl stop galaxy:'
    elif self.init == 'init':
      if self.os == 'centos': return 'systemctl stop galaxy.service'
      if self.os == 'Ubuntu' and self.codename == 'xenial': return 'systemctl stop galaxy.service'
      if self.os == 'Ubuntu' and self.codename == 'trusty': return 'service galaxy stop'

  #______________________________________
  def get_start_command(self):
    if self.init == 'supervisord': return 'supervisorctl start galaxy:'
    elif self.init == 'init':
      if self.os == 'centos': return 'systemctl start galaxy.service'
      if self.os == 'Ubuntu' and self.codename == 'xenial': return 'systemctl start galaxy.service'
      if self.os == 'Ubuntu' and self.codename == 'trusty': return 'service galaxy start'

  #______________________________________
  def get_status_command(self):
    if self.init == 'supervisord': return 'supervisorctl status galaxy:'
    elif self.init == 'init':
      if self.os == 'centos': return 'systemctl status galaxy.service'
      if self.os == 'Ubuntu' and self.codename == 'xenial': return 'systemctl status galaxy.service'
      if self.os == 'Ubuntu' and self.codename == 'trusty': return 'service galaxy status'

  #______________________________________
  def get_init(self): return self.init
  def get_os(self): return self.os
  def get_version(self): return self.version
  def get_codename(self): return self.codename

  #______________________________________
  def set_init(self, init): self.init = init
  def set_os(self, os): self.os = os
  def set_version(self, version): self.version = version
  def set_codename(self, codename): self.codename = codename

####################################

class UwsgiSocket:
  def __init__(self, server=None, port=None, timeout=None, fname=None):
    self.server = server
    self.port = port
    self.timeout = timeout

    self.par = 0
    if fname is not None:
      self.fname = fname

      section = 'uwsgi'
      option = 'socket'

      filename, file_extension = os.path.splitext(fname)
      file_extension = file_extension.replace('.', '')
      if file_extension == 'ini':

        configParser = ConfigParser.RawConfigParser()
        configParser.readfp(open(fname))
        configParser.read(fname)

        if configParser.has_option(section, option):
          self.par = configParser.get(section , option)
        else:
          raise Exception('No [uwsgi] section in %s' % fname)

      elif file_extension == 'yml' or file_extension == 'yaml':

        import yaml
        with open(fname, 'r') as stream:
          try:
            config =  yaml.load(stream)
            self.par = config[section][option]
          except yaml.YAMLError as exc:
            logs.error('[galaxyctl_libs] %s' % exc)

    self.server = self.par.split(':')[0]
    self.port = int(self.par.split(':')[1])

  #______________________________________
  def get_server(self): return self.server
  def get_port(self): return self.port

  #______________________________________
  def set_server(self, server): self.server = server
  def set_port(self, port): self.port = port

  #______________________________________
  def get_uwsgi_master_pid(self):
    command = 'lsof -t -i :%s' % self.port
    proc = subprocess.Popen( args=command, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    communicateRes = proc.communicate()
    stdOutValue, stdErrValue = communicateRes
    status = proc.wait()
    return stdOutValue, stdErrValue, status

####################################

class UwsgiStatsServer:
  def __init__(self, server=None, port=None, timeout=None, fname=None):
    self.server = server
    self.port = port
    self.timeout = timeout

    self.par = 0
    if fname is not None:
      self.fname = fname

      section = 'uwsgi'
      option = 'stats'

      filename, file_extension = os.path.splitext(fname)
      file_extension = file_extension.replace('.', '')
      if file_extension == 'ini':

        configParser = ConfigParser.RawConfigParser()
        configParser.readfp(open(fname))
        configParser.read(fname)

        if configParser.has_option(section, option):
          self.par = configParser.get(section , option)
        else:
          raise Exception('No [uwsgi] section in %s' % fname)

      elif file_extension == 'yml' or file_extension == 'yaml':
  
        import yaml
        with open(fname, 'r') as stream:
          try:
            config =  yaml.load(stream)
            self.par = config[section][option]
          except yaml.YAMLError as exc:
            logs.error('[galaxyctl_libs] %s' % exc)

    self.server = self.par.split(':')[0]
    self.port = int(self.par.split(':')[1])

  #______________________________________
  def GetUwsgiStatsServer(self):

    logs.debug('[galaxyctl_libs UwsgiStatsServer] GetUwsgiStatsServer()')
    logs.debug('[galaxyctl_libs UwsgiStatsServer] Waiting Galaxy stats server')
    logs.debug('[galaxyctl_libs UwsgiStatsServer] Timeout: %s' % self.timeout)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if self.timeout:
        from time import time as now
        # time module is needed to calc timeout shared between two exceptions
        end = now() + self.timeout

    while True:
      try:
        if self.timeout:
          next_timeout = end - now()
          if next_timeout < 0:
            return False
          else:
            s.settimeout(next_timeout)

        s.connect((self.server, self.port))

      except socket.timeout, err:
        # this exception occurs only if timeout is set
        if self.timeout:
          return False

      except socket.error, err:
        # catch timeout exception from underlying network library
        # this one is different from socket.timeout
        if type(err.args) != tuple or err[0] != errno.ETIMEDOUT:
          pass
      else:
        logs.debug('[galaxyctl_libs UwsgiStatsServer] Stats server enabled on: %s:%s' % (self.server, self.port))
        return s

  #______________________________________
  def GetStatsJson(self):
    reply = self.GetUwsgiStatsServer().recv(131072)
    return reply

  #______________________________________
  # Returns params from *.ini file
  def ReadUwsgiIniFile(self, fname, section, option):

    self.par = 0
    filename, file_extension = os.path.splitext(fname)
    file_extension = file_extension.replace('.', '')

    if file_extension == 'ini':

      configParser = ConfigParser.RawConfigParser()
      configParser.readfp(open(fname))
      configParser.read(fname)

      if configParser.has_option(section, option):
        self.par = configParser.get(section , option)
      else:
        logs.debug('[galaxyctl_libs UwsgiStatsServer] No [%s] section in %s' % (section, fname))
        return False

    elif file_extension == 'yml' or file_extension == 'yaml':

      import yaml
      with open(fname, 'r') as stream:
        try:
          config =  yaml.load(stream)
          self.par = config[section][option]
        except yaml.YAMLError as exc:
          logs.error('[galaxyctl_libs] %s' % exc)

    return self.par

  #______________________________________
  # Check if uwsgi workers accept requests or not
  def CheckUwsgiWorkers(self, fname):

    if fname is not None:
      self.fname = fname

    logs.debug('[galaxyctl_libs UwsgiStatsServer] CheckUwsgiWorkers(fname=%s)' % fname)

    uwsgi_processes = self.ReadUwsgiIniFile(fname, 'uwsgi', 'processes')
    if uwsgi_processes is False:
      return False
    else:
      logs.debug('[galaxyctl_libs UwsgiStatsServer] UWSGI processes: %s' % uwsgi_processes)

    stats_json = self.GetStatsJson()
    stats_dictionary = json.loads(stats_json)

    logs.debug('[galaxyctl_libs UwsgiStatsServer] Check uWSGI workers status')

    for workers in stats_dictionary['workers']:
      workers_id = workers.get('id')
      workers_status = workers.get('accepting')
      workers_pid = workers.get('pid')
      logs.debug('[galaxyctl_libs UwsgiStatsServer] Worker pid: %s' % workers_pid)
      logs.debug('[galaxyctl_libs UwsgiStatsServer] Worker status: %s' % workers_status)
      if workers_status == 1:
        return True

    logs.debug('[galaxyctl_libs UwsgiStatsServer] No uWSGI workers accepting requests')
    return False

  #______________________________________
  def GetBusyList(self, fname=None):

    if fname is not None:
      self.fname = fname

    logs.debug('[galaxyctl_libs UwsgiStatsServer] GetBusyList(fname=%s)' % fname)

    busy_list = []

    # Get uwsgi workers number
    uwsgi_processes = self.ReadUwsgiIniFile(self.fname, 'uwsgi', 'processes')

    logs.debug('[galaxyctl_libs UwsgiStatsServer] Wait Galaxy stats server on %s:%s' % (self.server, self.port))
    stats = self.GetUwsgiStatsServer()

    if stats:
      stats_json = self.GetStatsJson()
      stats_dictionary = json.loads(stats_json)

      for workers in stats_dictionary['workers']:
        workers_id = workers.get('id')
        workers_status = workers.get('accepting')
        workers_pid = workers.get('pid')
        if workers_status == 0:
          busy_list.append(workers_pid)

      logs.debug('[galaxyctl_libs UwsgiStatsServer] Busy list: %s' % busy_list)
      return busy_list
