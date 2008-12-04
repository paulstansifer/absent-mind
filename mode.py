#! /usr/bin/python
import sys, os

from state import cfg
import util

def mode():
  ret_val = cfg.get_file_var('cur_mode').split(' ')
  if ret_val == ['']:
    return []
  else:
    return ret_val


def run_dir(path):
  if not cfg.exists(path):
    raise util.CannotComply('Directory "'+path+'" does not exist')  #Safe, run_dir is called first

  log_entered = False
  for root, dirs, files in os.walk(cfg.real_path(path)):
    #TODO iterate over dirs and files in alpha order, together
    dirs = [ d for d in dirs if util.y_or_n('Execute directory \''+d+'\'?')]
    for f in files:
      (name, dot, ext) = f.rpartition('.')
      if dot != '.':
        print 'Can\'t execute "'+f+'"; no extension.'
        continue
      if (name.endswith('.implicit') or name.endswith('.always') or 
          util.y_or_n('Execute "'+root+'/'+f+'"?')):
        print '-> ' + f,

        error = None
        #Do something with the file, depending on extension
        if ext == 'sh':
          ret_code = os.spawnl(os.P_WAIT, root + '/' + f)
          if ret_code != 0:
            error = 'Returned code ' + str(ret_code)
        elif ext == 'txt':
          #with file(root + '/' + f) as f:
          f = file(root+'/'+f)
          print
          print f.read()
        else:
          print 'Don\'t know what to do with "' + ext + '".'

            
        if error == None:
          print '[OK]'
        else:
          print '[ERROR ' + error + ']'

    if not log_entered and util.y_or_n('Make a log entry?'):
      print "Ha!  You can't!"


def _update_ps1():
  #ORIG_PS1 exits if we've already mucked with PS1
  if 'ORIG_PS1' in os.environ:
    ps1 = os.environ['ORIG_PS1']
  else:
    #TODO: PS1 gets removed?
    ps1 = r'\h:\w \u\$ '#os.environ['PS1']
    cfg.set_env_var('ORIG_PS1', ps1)
    
  import re
  
  cfg.set_env_var(
    'PS1',
    re.sub(
      r'(\[[\w ]+\])?\\\$',
      '['+cfg.get_file_var('cur_mode')+']\\$',
      ps1)
  )
  

  
def push(name):
  run_dir('modes/'+name+'/push')
  cfg.set_file_var('cur_mode', ' '.join(mode() + [name]))

  _update_ps1()

def pop():
  old_mode = mode()
  if len(old_mode) == 0:
    raise util.CannotComply('No modes are active.')
  run_dir('modes/'+old_mode[-1]+'/pop')
  cfg.set_file_var('cur_mode', ' '.join(old_mode[0:-1]))

  _update_ps1()


