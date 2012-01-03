#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess, shutil, sys, shlex
import Env, Regions
import NoaaXmlParser
from BsbHeader import BsbHeader
from FilePathSearch import FilePathSearch
from FindZoom import getKapZoom
      
class createTiles():
    def __init__(self, directory, regiondir, filter = None):
        if not os.path.isdir(regiondir):
            os.mkdir(regiondir)
        fps = FilePathSearch(directory, 'KAP', filter)
        logfile = directory + "/tilelog.txt"
        log = open(logfile, "wb")
        count = 1
        total = fps.filePaths.__len__()
        wgs84compat = ["WGS84", "NAD83"]
        for kapPath in fps.getfilePaths():
            print "Creating tileset ###", count, "of", total, "###"
            header = BsbHeader(kapPath)
            if wgs84compat.__contains__(header.getprojection()):
                self.doTile2(kapPath, log, regiondir)
            else:
                print "this set is not wgs84 projected... using alternative tiling method"
                self.doTile2(kapPath, log, regiondir)
            count += 1
        log.close()
        
    def doTile(self, kapPath, log, regiondir):
        command = "python %smap2gdal.py -q --cut-file %s" %(Env.tilersToolsDir, kapPath)
        #print command
        thisone = subprocess.Popen(shlex.split(command), stdout=log)
        thisone.wait()
        
        gmtPath = kapPath[0:-4]+".gmt"
        print gmtPath, "\n"
        if os.path.isfile(gmtPath):
            command = "python %sgdal_tiler.py --overview-resampling=bilinear --base-resampling=bilinear -t " %(Env.tilersToolsDir) + regiondir + \
                      " --cut --cutline " + gmtPath + " -z " + str(getKapZoom(kapPath)) + " " + kapPath
            destdir = regiondir + "/" + os.path.basename(kapPath)[0:-4]+".zxy"
            #print destdir
            if not os.path.isdir(destdir):
                print command
                thisone = subprocess.Popen(shlex.split(command), stdout=log)
                thisone.wait()
            else:
                print "this chart has already been tiled"
        else:
            print "Something went wrong creating vrt from: " + kapPath
            sys.exit()
            
    def doTile2(self, kapPath, log, regiondir):
        command = "python %smap2gdal.py -q %s" %(Env.tilersToolsDir, kapPath)
        print command
        thisone = subprocess.Popen(shlex.split(command), stdout=log)
        thisone.wait()
        
        #kstz = KapScaleToZoom(kapPath)
        vrtPath = kapPath[0:-4]+".vrt"
        #vrtPath = kapPath.rstrip(".KAP")+".vrt"
        print vrtPath, "\n"
        if os.path.isfile(vrtPath):
            command = "python %sgdal_tiler.py --overview-resampling=bilinear --base-resampling=bilinear -t " %(Env.tilersToolsDir) + regiondir + \
                      " -c " + vrtPath + " -z " + str(getKapZoom(kapPath))
            destdir = regiondir + "/" + os.path.basename(kapPath)[0:-4]+".zxy"
            #print destdir
            if not os.path.isdir(destdir):
                print command
                thisone = subprocess.Popen(shlex.split(command), stdout=log)
                thisone.wait()
            else:
                print "this chart has already been tiled"
        else:
            print "Something went wrong creating vrt from: " + kapPath
            sys.exit()
           
class purgeZxy():
    def __init__(self, dir):
        fps = FilePathSearch(dir, 'zxy')
        for each in fps.getfilePaths():
            shutil.rmtree(each)
    
def purgeVrt(dir):
    fps = FilePathSearch(dir, 'vrt')
    count = 0
    for map_file in fps.getfilePaths():
        os.remove(map_file)
        count += 1
    print str(count) + " vrt files purged!"
    
def purgeGmt(dir):
    fps = FilePathSearch(dir, 'gmt')
    count = 0
    for map_file in fps.getfilePaths():
        os.remove(map_file)
        count += 1
    print str(count) + " gmt files purged!"
    
def countVrts(dir):
    fps = FilePathSearch(dir, 'vrt')
    print str(fps.getfilePaths().__len__()) + " vrt files"
    
def vrtCheck(kapList):
    fps = FilePathSearch(dir, 'vrt')
    vrtList = []
    for vrt in fps.getfilePaths():
        vrt = vrt.split("/")[-1].rstrip(".vrt")
        vrtList.append(vrt)
    nKapList = []
    for kap in kapList:
        kap = kap.rstrip(".KAP")
        nKapList.append(kap)
    missing = []
    for each in nKapList:
        if not vrtList.__contains__(each):
            missing.append(each)
    return missing
    
def renderRegion(region):
    filter = Regions.getRegionFilterList(region)
    #print filter
    tileDir = Regions.getRegionUnMergedTileDir(region)
    bsbDir = Regions.getRegionBsbDir(region)
    if filter != None:
        createTiles(bsbDir, tileDir, filter)
    else:
        print region + " does not exist"
        
if __name__== "__main__":
    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        Regions.printRegionList()
        sys.exit()
    else:
        renderRegion(sys.argv[1])
