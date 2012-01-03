#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, subprocess, shlex, sys 
import Env, Regions

def createGemf(region):
    directory = Regions.getRegionMergedTileDir(region) + ".opt"
    if not os.path.isdir(directory):
        print "Region not ready... run BatchRegionOptimizer first"
        sys.exit()
    if not os.path.isdir(directory + "/gemf"):
        os.mkdir(directory + "/gemf")
        if os.path.isdir(directory+"/merge"):
            shutil.move(directory+"/merge", directory+"/gemf")
        else:
            print "you need to merge files first!"
            sys.exit()

    logfile = directory + "/gemflog.txt"
    log = open(logfile, "wb")
    command = "python %s/generate_efficient_map_file.py %s" %(Env.tilersToolsDir, directory+"/gemf")
    print "creating gemf..."
    print command
    thisone = subprocess.Popen(shlex.split(command), stdout=log)
    thisone.wait()
    log.close()
    os.rename(directory + "/gemf/map_data.gemf", Env.gemfDir + region+".gemf")

if __name__== "__main__":
    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        Regions.printRegionList()
        sys.exit()
    else:
        createGemf(sys.argv[1])
        #os.rename(regiondir+"/gemf/map_data.gemf", Env.outPutDir+"regions/merged/"+region+'.gemf')
