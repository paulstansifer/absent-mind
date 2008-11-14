#! /usr/bin/python
import sys

command = sys.argv[0]

if command == 'am': #the command is the second argument
  command = sys.argv[1]
  args = sys.argv[2:]
else:
  args = sys.argv[1:]

{'push': 0,
 'pop': 0,
 'temp-mode': 0}
