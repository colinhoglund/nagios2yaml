#!/usr/bin/env python
'''
Tool for converting Nagios object definitions
  to YAML format. Simply pass n2y.py a text
  file with nagios objects.

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

failed_objects = []

# prints out YAML formatted configuration
def output_yaml(obj_type, name_directive):
    for obj in objects.get(obj_type):
        if not obj.get(name_directive):
            failed_objects.append(str(obj))
            break
        if obj_type == 'services':
            print '  \'' + obj.get(name_directive) + '\':'
        else:
            print '  ' + obj.get(name_directive) + ':'
        for directive in obj.iteritems():
            if directive[0] == name_directive:
                continue
            print '    ' + directive[0] + ': ' + '\'' + directive[1] + '\''

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
    if line == '\n':
        continue
    temp_obj[line.split()[0]] = ' '.join(line.split()[1:])

for obj_type in objects.iteritems():
    if len(obj_type[1]) > 0:
        print 'nagios::' + obj_type[0] + ':'
        if obj_type[0] == 'services':
            output_yaml(obj_type[0], 'service_description')
        else:
            output_yaml(obj_type[0], obj_type[0][:-1] + '_name')

if len(failed_objects) > 0:
    print "The following objects failed to compile:"
    for obj in failed_objects:
        print obj
