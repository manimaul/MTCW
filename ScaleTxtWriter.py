#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess, shutil, sys, threading, time, shlex
from BsbHeader import BsbHeader
from FilePathSearch import FilePathSearch
from KapScaleToZoom import KapScaleToZoom
from BsbScales import BsbScales
      
class createTiles():
    def __init__(self, directory, regiondir, filter = None):
        if not os.path.isdir(regiondir):
            os.mkdir(regiondir)
        fps = FilePathSearch(directory, 'KAP', filter)
        count = 1
        total = fps.filePaths.__len__()
        for kapPath in fps.getfilePaths():
            print "getting zoom ###", count, "of", total, "###"
            self.doTile(kapPath, regiondir)
            count += 1
        
    def doTile(self, kapPath, regiondir):
        command = "python /home/will/bsbTileTools/tilers_tools/map2gdal.py -q %s" %(kapPath)
        print command
        thisone = subprocess.Popen(shlex.split(command))
        thisone.wait()
        
        kstz = KapScaleToZoom(kapPath)
        vrtPath = kapPath.rstrip(".KAP")+".vrt"
        print vrtPath, "\n"
        if os.path.isfile(vrtPath):
            command = "python /home/will/bsbTileTools/tilers_tools/zoom_grabber.py -t " + regiondir + \
                      " -c " + vrtPath
            thisone = subprocess.Popen(shlex.split(command))
            thisone.wait()
        else:
            print "Something went wrong creating vrt from: " + kapPath
            sys.exit()

if __name__== "__main__":
    from NoaaXmlParser import NoaaXmlParser
    region = "NOAA_BSB_REGION_ALL"
    dir = "/home/will/charts/BSB_ROOT"
    regiondir = "/home/will/charts/" + region
    filter = NoaaXmlParser(region, dir).getKapFiles()    
    createTiles(dir, regiondir, filter)
