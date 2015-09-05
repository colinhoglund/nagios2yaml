#!/usr/bin/env python
'''
Tool for converting Nagios object definitions
  to YAML format.

Usage: ./n2y.py <filename>
'''
from sys import argv
import re

script, filename = argv
text = open(filename)

# Create a dictionary of lists to
#   store Nagios objects definitions
objects = {
'commands': [],
'contacts': [],
'contactgroups': [],
'hosts': [],
'hostgroups': [],
'services': [],
'serviceescalations': [],
'servicegroups': [],
'timeperiods': [],
}

temp_obj = {}
obj_type = ''
for line in text.readlines():
    # remove comments
    if '#' in line:
        continue
    if ';' in line:
        line = re.sub(';.*$', '', line)
    # start building Nagios object
    if '{' in line:
        # create white space around curly
        #   braces for string splitting
        line = re.sub('{', ' { ', line)
        obj_type = line.split()[1] + 's'
        continue
    # finish building Nagios object
    if '}' in line:
        line = re.sub('}', ' } ', line)

        # write temp_obj to objects
        objects.get(obj_type).append(temp_obj)
        temp_obj = {}
        obj_type = ''
        continue
    # skip line if { hasn't been encountered
    if not obj_type:
        continue

    # update temp_obj
    temp_obj[line.split()[0]] = ' '.join(line.split()[1:])

print objects
