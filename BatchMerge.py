#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, subprocess, shlex, sys
from BsbScales import BsbScales

class mergeTiles():
    def __init__(self, regiondir, kapDir, tileDir, filter=None):
        ##get merge order
        bsbScales = BsbScales(kapDir, filter)
        sortList = bsbScales.getKapsSortedByScale(".zxy")
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
        command = "python /home/will/tilers_tools_plus/tiles_merge_simple.py -l %s %s/merge" %(moPath, regiondir)
        print command
        print "merging", sortList.__len__(), "tile sets..."
        #print command
        thisone = subprocess.Popen(shlex.split(command), stdout=log)
        thisone.wait()
        log.close()
        
if __name__== "__main__":
    import NoaaXmlParser
    
    regionlst = NoaaXmlParser.xmlUrls.keys()

    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        sys.exit()
    
    region = sys.argv[1]
    
    if not regionlst.__contains__(region):
        print "Invalid region:"
        sys.exit()
    
    #region = "WA"
    tileDir = "/home/will/charts/BSB_ALL"
    kapDir = "/home/will/charts/BSB_ROOT"
    regiondir = "/home/will/charts/" + region
    filter = NoaaXmlParser.NoaaXmlParser(region).getKapFiles()    
    mergeTiles(regiondir, kapDir, tileDir, filter)
    
