#! /usr/local/bin/python
#       D
# /^^^\/
# \__.|
#    \\
import sys

import mode

def execute():
  print sys.argv[0]
  
  command = sys.argv[1]
  args = sys.argv[2:]

  #pick a command, and execute it with remaining args
  {'push': mode.push,
   'pop': mode.pop,
   'temp-mode': 0}[command](*args)

if __name__ == "__main__":
  execute()


