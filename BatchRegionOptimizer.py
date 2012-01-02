#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shlex, sys, subprocess, os
import Env, Regions

def optimizeRegion(region):
    optDir = Regions.getRegionMergedTileDir(region)
    if os.path.isdir(optDir):
        command = "python %stiles_opt.py %s" %(Env.tilersToolsDir, optDir)
        print command
        thisone = subprocess.Popen(shlex.split(command))
        thisone.wait()
    else:
        print "Region tiles don't exist... run BatchRegionMerger.py first"
    
if __name__== "__main__":
    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        Regions.printRegionList()
        sys.exit()
    else:
        optimizeRegion(sys.argv[1])