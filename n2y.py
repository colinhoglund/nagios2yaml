#!/usr/bin/env python

from sys import argv
import re

script, filename = argv

text = open(filename)

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

obj = {}
obj_type = ''

for line in text.readlines():
    if '#' in line:
        continue
    if ';' in line:
        line = re.sub(';.*$', '', line)
    if '{' in line:
        line = re.sub('{', ' { ', line)
        obj_type = line.split()[1] + 's'
        continue
    if '}' in line:
        line = re.sub('}', ' } ', line)
        objects.get(obj_type).append(obj)
        obj = {}
        obj_type = ''
        continue
    if not obj_type:
        continue
    obj[line.split()[0]] = ' '.join(line.split()[1:])

print objects
