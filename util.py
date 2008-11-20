import os

class LogicError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class CannotComply(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def y_or_n(prompt):
  while True:
    inp = raw_input(prompt + ' (y/n)')
    if inp == 'y' or inp == 'Y':
      return True
    if inp == 'n' or inp == 'N':
      return False



def text(comment):
  file_id = 0
  
  tmp = cfg.cfg_file('tmp/text')
  
