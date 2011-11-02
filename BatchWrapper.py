#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess, shutil, sys, shlex
from BsbHeader import BsbHeader
from FilePathSearch import FilePathSearch
from KapScaleToZoom import KapScaleToZoom
      
class createTiles():
    def __init__(self, directory, regiondir, filter = None):
        if not os.path.isdir(regiondir):
            os.mkdir(regiondir)
        fps = FilePathSearch(directory, 'KAP', filter)
        logfile = directory + "/tilelog1.txt"
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
        command = "python /home/will/tilers_tools_plus/map2gdal.py -q --cut-file %s" %(kapPath)
        print command
        thisone = subprocess.Popen(shlex.split(command), stdout=log)
        thisone.wait()
        
        kstz = KapScaleToZoom(kapPath)
        gmtPath = kapPath.rstrip(".KAP")+".gmt"
        print gmtPath, "\n"
        if os.path.isfile(gmtPath):
            command = "python /home/will/tilers_tools_plus/gdal_tiler_bsb2.py --overview-resampling=bilinear --base-resampling=near -t " + regiondir + \
                      " --cut --cutline " + gmtPath + " -z " + kstz.getZoom() + " " + kapPath
            #command = "python /home/will/tilers_tools_plus/gdal_tiler_bsb2.py -r -t " + regiondir + \
            #          " --cut --cutline " + gmtPath + " " + kapPath
            destdir = regiondir + "/" + os.path.basename(kapPath).rstrip(".KAP")+".zxy"
            if not os.path.isdir(destdir):
                thisone = subprocess.Popen(shlex.split(command), stdout=log)
                thisone.wait()
                #os.remove(destdir+"/tilemap.xml")
                #os.remove(destdir+"/viewer-google.html")
                #os.remove(destdir+"/viewer-openlayers.html")
            else:
                print "this chart has already been tiled"
        else:
            print "Something went wrong creating vrt from: " + kapPath
            sys.exit()
            
    def doTile2(self, kapPath, log, regiondir):
        command = "python /home/will/tilers_tools_plus/map2gdal.py -q %s" %(kapPath)
        print command
        thisone = subprocess.Popen(shlex.split(command), stdout=log)
        thisone.wait()
        
        kstz = KapScaleToZoom(kapPath)
        vrtPath = kapPath.rstrip(".KAP")+".vrt"
        print vrtPath, "\n"
        if os.path.isfile(vrtPath):
            command = "python /home/will/tilers_tools_plus/gdal_tiler_bsb2.py --overview-resampling=bilinear --base-resampling=near -t " + regiondir + \
                      " -c " + vrtPath + " -z " + kstz.getZoom()
            #command = "python /home/will/tilers_tools_plus/gdal_tiler_bsb2.py -r -t " + regiondir + \
            #          " -c " + vrtPath
            destdir = regiondir + "/" + os.path.basename(kapPath).rstrip(".KAP")+".zxy"
            if not os.path.isdir(destdir):
                print command
                thisone = subprocess.Popen(shlex.split(command), stdout=log)
                thisone.wait()
                #os.remove(destdir+"/tilemap.xml")
                #os.remove(destdir+"/viewer-google.html")
                #os.remove(destdir+"/viewer-openlayers.html")
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
        
if __name__== "__main__":
    from NoaaXmlParser import NoaaXmlParser
    region = "BSB_ALL"
    dir = "/home/will/charts/BSB_ROOT"
    regiondir = "/home/will/charts/" + region
    filter = NoaaXmlParser(region).getKapFiles()    
    createTiles(dir, regiondir, filter)
    
