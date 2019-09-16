#!/usr/bin/env python

import sys, os

if len(sys.argv) < 2:
    exit(0)   

filname = sys.argv[1]

if not os.path.exists(filname):
    print('file does not exist')
    exit(0)   

with open(filname, "rb") as infil:
    lines = infil.readlines();
    for line in lines:
        if '---+---' in line:
            continue
        line = line.strip()
        fields = line.split('|')
        newlist = []
        for f in fields:
            f = f.strip()
            if f:
                newlist.append('"{0}"'.format(f))
        outline = ','.join(newlist)
        print(outline)
           
