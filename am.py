#! /usr/bin/python
import sys

import mode

def execute():
  command = sys.argv[0]

  if command == 'am.py': #the command is the second argument
    command = sys.argv[1]
    args = sys.argv[2:]
  else:
    args = sys.argv[1:]

  #pick a command, and execute it with remaining args
  {'push': mode.push,
   'pop': mode.pop,
   'temp-mode': 0}[command](*args)

if __name__ == "__main__":
  execute()


