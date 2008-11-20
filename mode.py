#! /usr/bin/python
import sys, os

from state import cfg
import util

def mode():
  return cfg.get_file_var('cur_mode').split(' ')


def run_dir(path):
  if not cfg.exists(path):
    raise util.CannotComply('Directory "'+path+'" does not exist')  #Safe, run_dir is called first
  
  for root, dirs, files in os.walk(cfg.real_path('modes/'+path)):
    log_entered = False
    #TODO iterate over dirs and files in alpha order, together
    dirs = [ d for d in dirs if y_or_n('Execute directory \''+d+'\'?')]
    for f in files:
      (name, dot, ext) = f.rpartition('.')
      if dot != '.':
        print 'Can\'t execute "'+f+'"; no extension.'
        continue
      if (name.endswith('.implicit') or name.endswith('.always') or 
          y_or_n('Execute "'+root+'/'+f+'"?')):
        print '-> ' + f,

        #Do something with the file, depending on extension
        if ext == '.sh':
          ret_code = spawnl(os.P_WAIT, root + '/' + f)
          if ret_code == 0:
            error = None
          else:
            error = 'Returned code ' + ret_code
        elif ext == '.txt':
          #with file(root + '/' + f) as f:
          f = file(root+'/'+f)
          print f.read()
          error = None

            
        if error == None:
          print '[OK]'
        else:
          print '[ERROR ' + error + ']'

    if not log_entered and y_or_n('Make a log entry?'):
      print "Ha!  You can't!"


def _update_ps1():
  #store old version in another enviornment variable
  os.environ['PS1'] = r'\h:\w \u['+cfg.get_file_var('cur_mode')+']\$'

  
def push(name):
  run_dir('modes/'+name+'/push')
  cfg.set_file_var('cur_mode', ' '.join(mode() + [name]))

  _update_ps1()

def pop():
  run_dir('modes/'+mode[-1]+'/pop')
  cfg.set_file_var('cur_mode', ' '.join(mode()[0:-1]))

  _update_ps1()


