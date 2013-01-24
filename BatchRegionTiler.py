#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BsbHeader import BsbHeader
from FilePathSearch import FilePathSearch
from FindZoom import getKapZoom
import CreateHeaderOverride
import Env
import Regions
import os
import subprocess
import shutil
import sys
import shlex
      
class createTiles():
    def __init__(self, directory, regiondir, region, pFilter = None):
        self.region = region
        if not os.path.isdir(regiondir):
            os.mkdir(regiondir)
        fps = FilePathSearch(directory, 'KAP', pFilter)
        logfile = directory + "/tilelog.txt"
        log = open(logfile, "wb")
        count = 1
        total = fps.filePaths.__len__()
        wgs84compat = ["WGS84", "NAD83"]
        for kapPath in fps.getfilePaths():
            print "Creating tileset ###", count, "of", total, "###"
            header = BsbHeader(kapPath)
            if wgs84compat.__contains__(header.getprojection()):
                self.doTile(kapPath, log, regiondir)
            else:
                print "this set is not wgs84 projected... using alternative tiling method"
                self.doTile2(kapPath, log, regiondir)
            count += 1
        log.close()
        
    def doTile(self, kapPath, log, regiondir):
        header_override = Env.mtcwDir+"header_overrides/NOAA/"+os.path.basename(kapPath)[0:-4]
        if Regions._isNOAARegion(self.region) and os.path.isfile(header_override):
            override = CreateHeaderOverride.makeHeader(kapPath)
            command = "python %smap2gdal.py -q --cut-file --header-file %s %s" %(Env.tilersToolsDir, override, kapPath)
        else:   
            command = "python %smap2gdal.py -q --cut-file %s" %(Env.tilersToolsDir, kapPath)
        #print command
        thisone = subprocess.Popen(shlex.split(command), stdout=log)
        thisone.wait()
        
        gmtPath = kapPath[0:-4]+".gmt"
        print gmtPath, "\n"
        if os.path.isfile(gmtPath):
            #--overview-resampling: (choose from 'bilinear', 'nearest', 'near', 'antialias', 'bicubic'
            #--base-resampling: (choose from 'bilinear', 'nearest', 'cubic', 'near', 'lanczos', 'cubicspline'
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
        header_override = Env.mtcwDir+"header_overrides/NOAA/"+os.path.basename(kapPath)[0:-4]
        if Regions._isNOAARegion(self.region) and os.path.isfile(header_override):
            override = CreateHeaderOverride.makeHeader(kapPath)
            command = "python %smap2gdal.py -q --header-file %s %s" %(Env.tilersToolsDir, override, kapPath)
        else:
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
    def __init__(self, pDir):
        fps = FilePathSearch(pDir, 'zxy')
        for each in fps.getfilePaths():
            shutil.rmtree(each)
    
def purgeVrt(pDir):
    fps = FilePathSearch(pDir, 'vrt')
    count = 0
    for map_file in fps.getfilePaths():
        os.remove(map_file)
        count += 1
    print str(count) + " vrt files purged!"
    
def purgeGmt(pDir):
    fps = FilePathSearch(pDir, 'gmt')
    count = 0
    for map_file in fps.getfilePaths():
        os.remove(map_file)
        count += 1
    print str(count) + " gmt files purged!"
    
def countVrts(pDir):
    fps = FilePathSearch(pDir, 'vrt')
    print str(fps.getfilePaths().__len__()) + " vrt files"
    
def vrtCheck(kapList, pDir):
    fps = FilePathSearch(pDir, 'vrt')
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
    mFilter = Regions.getRegionFilterList(region)
    #print mFilter
    tileDir = Regions.getRegionUnMergedTileDir(region)
    bsbDir = Regions.getRegionBsbDir(region)
    if mFilter != None:
        createTiles(bsbDir, tileDir, region, mFilter)
    else:
        print region + " does not exist"
        
if __name__== "__main__":
    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        Regions.printRegionList()
        sys.exit()
    else:
        renderRegion(sys.argv[1])
