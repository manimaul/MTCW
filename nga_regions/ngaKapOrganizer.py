#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        