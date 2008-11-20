#! /usr/bin/python
import datetime

import util
import mode

def log(contents):
  f = cfg.log('dev')

  lines = [ '  ' + line for
            line in contents.split('\n') ]
  
  now = datetime.now()
  now.microsecond = 0 #we don't need that kind of precision
  
  l.write(str(now) + ' ~~~ ' + mode.mode_as_string() + '\n')
  l.writelines(lines)
  l.write('\n---\n\n')



def extract(which_log, starting=None, ending=None, mode=None, or_parent=True):
  f = cfg.log('dev')

  while True:
    e = next_entry(f)
    

  

class entry:
  def __init__(self, lines):
    (dt, sep, self.mode) = lines[0].partition(' ~~~ ')
    self.timestamp = strptime(dt, 'YYYY-MM-DDTHH:MM:SS')
    #default output format from Python docs
    
    self.text = '\n'.join([ line[2:] for line in lines[1:] ])
    #strip the two-space prefix from each line
  
    
def next_entry(f):
  accum = []
  while True:
    line = f.readline()

    #readline repeatedly returns '' when it hits the end of a file.
    #an empty entry is the end-of-file signal
    if line == '---\n' or line == '':
      break
    if line != '\n': #ignore empty lines
      accum.append(line)
  if len(accum) == 0: #end of file
    return None
  return entry(accum)
