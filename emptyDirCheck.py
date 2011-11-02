#!/usr/bin/env python
# -*- coding: utf-8 -*-

#print "True or False = :", True or False
#print "True and False = :", True and False
#print "bitwise or of True, False = :", True | False
#print "bitwise and of True, False = :", True & False
#print "bitwise exclusive or of True, False = :", True ^ False

import os
lst = []
dir = '/home/will/charts/NOAA_BSB_REGION_ALL/'

count = 0;
for path in os.listdir(dir):
    if not os.listdir(dir+path):
        print 'removing empty directory:' + path
        #os.removedirs(dir+path)
        count += 1

print count, 'empty directories found'
