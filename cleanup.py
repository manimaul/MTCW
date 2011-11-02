#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import shutil

p = os.path.abspath('/home/will/charts/NOAA_BSB_REGION_ALL/')

#print os.listdir(p)
num = 0;
for ea in os.listdir(p):
    np = os.listdir(p+'/'+ea)

    if np.count('4')>0 and np.count('5')>0: # and np.count('12')>0:
        deldir = p+'/'+ea
        print ea
        #shutil.rmtree(deldir)
        #print "deleting: " + ea
        num += 1

print num
