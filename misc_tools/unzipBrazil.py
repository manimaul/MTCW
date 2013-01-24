#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shlex, subprocess

zipdir = "/home/will/zxyCharts/BSB_ROOT/BR_BSB_ROOT/zips"
outdir = "/home/will/zxyCharts/BSB_ROOT/BR_BSB_ROOT"

zips = os.listdir(zipdir)
os.chdir(zipdir)
count = 0
for zip in zips:
    count += 1
    command = "unzip -j -n -d "+outdir+" "+zip
    #print command
    subprocess.Popen(shlex.split(command))
    
print "%s zip files unzipped" %(count)