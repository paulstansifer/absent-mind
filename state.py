#! /usr/bin/python
import os, os.path

from util import *



class BadState(LogicError):
  pass
#  def __init__(self, value):
#    self.value = value
#  def __str__(self):
#    return repr(self.value)



class State:
  def __init__(self):
    self.config_path = os.path.expanduser('~/.absent-mind/')
    self.ensure_file_exists('cur_mode')
    if os.path.exists(self.real_path('shell_cmds')):
      print """
It looks like your shell isn't configured for absent-mind.  Your
prompt may not be correctly updated for modes.

Run the following command:
  am () { am $@; source %s; rm %s; }

      """ % (
             self.real_path('shell_cmds'),
             self.real_path('shell_cmds'))

    #TODO: maybe it should be closed
    self.shell_cmds = self.cfg_file('shell_cmds', 'w') #we clear and rewrite it each time

  def exists(self, path):
    return os.path.exists(self.real_path(path))

  def ensure_file_exists(self, path):
    if not os.path.exists(self.real_path(path)):
      self.ensure_file_empty(path)

  def ensure_file_empty(self, path):
    f = self.cfg_file(path, 'w')
    f.write('')
    f.close()

  def set_env_var(self, var, value):
    self.shell_cmds.write('export '+var+'=\''+value+'\'\n')

  def real_path(self, path):
    return os.path.normpath(os.path.realpath(self.config_path + path))

  

  #TODO we can probably do something cool with properties here
  def cfg_file(self, path, mode='r'):
    proper_path = self.real_path(path)
    if not proper_path.startswith(self.config_path):
      raise am.LogicError('Path "'+proper_path+'" tries to escape the config directory.')
    else:
      return open(proper_path, mode)

  def file_contents(self, path):
    #with self.cfg_file(path) as f:
    #  return f.read()
    f = self.cfg_file(path)
    ret_val = f.read()
    f.close()
    return ret_val

  
  def get_file_var(self, path):
    '''Treats a file as an individual value, stripping trailing newlines.'''
    return self.file_contents(path).rstrip('\n')

  def set_file_var(self, path, val):
    #with self.cfg_file(path, mode='w') as f:
    #  f.write(val)
    f = self.cfg_file(path, 'w')
    f.write(val)
    f.close()
    
  
  def _kill_dir(self, path):
    path = os.path.normpath(os.path.realpath(path)) #'path' is kinda a funny word
    if exists(path + '/am_autogen_ok_to_delete'):
      if path.starts_with(self.config_path):
        rmdir(path)
      else:
        raise BadState('Directory "'+path+'" isn\'t located in our config directory.')
    else:  
      raise BadState('Directory "'+path+'" doesn\'t look safe to delete.')

  def _make_dir(self, path):
    mkdir(path)
    f = open(path+'/am_autogen_ok_to_delete', 'w')
    f.write(' ')
    f.close()

cfg = State()
