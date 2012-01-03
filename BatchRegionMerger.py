#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, subprocess, shlex, sys
import Regions, Env
from BsbScales import BsbScales

class mergeTiles():
    def __init__(self, regiondir, kapDir, tileDir, filter=None):
        ##get merge order
        bsbScales = BsbScales(kapDir, filter)
        sortList = bsbScales.getKapsSortedByScale(".zxy")
        sortList.reverse() #only reverse if you are rendering 2 zoom levels
        moPath = regiondir + "/mergeorder.txt"
        if not os.path.isdir(regiondir):
            os.mkdir(regiondir)
        if os.path.isfile(regiondir + "/mergeorder.txt"):
            os.remove(moPath)
        moFile = open(moPath, "w")
        exit = False
        for line in sortList:
            if os.path.isdir(tileDir + "/" + line):
                moFile.write(tileDir + "/" + line+"\n")
            else:
                print "missing tileset: " + line
                exit = True
        moFile.close()
        
        if exit:
            sys.exit()
            
        logfile = regiondir + "/mergelog.txt"
        log = open(logfile, "wb")
        #log = None
        command = "python %stiles_merge_simple.py -l %s %s/merge" %(Env.tilersToolsDir, moPath, regiondir)
        print command
        print "merging", sortList.__len__(), "tile sets..."
        #print command
        thisone = subprocess.Popen(shlex.split(command), stdout=log)
        thisone.wait()
        log.close()
    
def mergeRegion(region):
    print "merging: " + region
    mergeTiles(Regions.getRegionMergedTileDir(region), Regions.getRegionBsbDir(region), \
               Regions.getRegionUnMergedTileDir(region), Regions.getRegionFilterList(region))
        
if __name__== "__main__":
    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        Regions.printRegionList()
        sys.exit()
    else:
        mergeRegion(sys.argv[1])
    
