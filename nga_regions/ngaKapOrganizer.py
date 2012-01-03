#!/usr/bin/env python
# -*- coding: utf-8 -*-

#read README and INSTRUCTIONS first... most importantly setup and run Env.py first and/or put NGA kap files in ~/zxyCharts/BSB_ROOT/NGA_BSB_ROOT/
#this will create an organized directory structure of Physical** links to .kap files
#but will keep original directory of kaps in place so we can still rsync
#
#now you can easily view particular sub-sections of nga charts in opencpn
#
# ~/zxyCharts/BSB_ROOT/NGA_BSB_ROOT/NGA_BSB_ORGANIZED_LINKS/
#
#** Physical links are hard links to soft links ... this is so opencpn will read kap file links


import Env, FilePathSearch
import os, subprocess, shlex

fps = FilePathSearch.FilePathSearch(os.path.abspath(Env.ngaBsbDir))
destDir = Env.bsbDir+"NGA_BSB_ORGANIZED_LINKS/"
command = "ln -P %s %s"

fPaths = fps.getfilePaths()
fPaths.sort()

for fPath in fPaths:
    kapFile = fPath.split("/")[-1]
    if len(kapFile) == 6:
        link = destDir+"10s/"+kapFile
        if not os.path.isfile(link):
            cmd = command %(fPath, link)
            print cmd
            subprocess.Popen(shlex.split(cmd))
    if len(kapFile) == 7:
        subdir = kapFile[0]+"s"
        if not os.path.isdir(destDir+"100s/%s/"%(subdir)):
            os.makedirs(destDir+"100s/%s/"%(subdir))
        link = destDir+"100s/%s/"%(subdir)+kapFile 
        if not os.path.isfile(link):
            cmd = command %(fPath, link)
            print cmd
            subprocess.Popen(shlex.split(cmd))
    if len(kapFile) == 9:
        subdir = kapFile[0]+"0000s/"+kapFile[1]+"000s/"
        if not os.path.isdir(destDir+subdir):
            os.makedirs(destDir+subdir)
        link = destDir+subdir+kapFile
        #print link
        if not os.path.isfile(link):
            cmd = command %(fPath, link)
            print cmd
            subprocess.Popen(shlex.split(cmd))
        