#!/usr/bin/env python
# -*- coding: utf-8 -*-

#read README and INSTRUCTIONS first... most importantly setup and run Env.py first and/or put NGA kap files in ~/zxyCharts/BSB_ROOT/NGA_BSB_ROOT/
#this will create region directory of Physical** links to .kap files for specified region
#but will keep original directory of kaps in place so we can still rsync
#
#now you can easily view particular region of nga charts in opencpn
#
# ~/zxyCharts/BSB_ROOT/NGA_BSB_ROOT/NGA_BSB_<REGION>/
#
#** Physical links are hard links to soft links ... this is so opencpn will read kap file links

import Env, FilePathSearch, Regions, RegionNGAParser
import os, subprocess, shlex, sys

def doIt(region):
    deleted = 0
    kept = 0
    created = 0
    if region == "REGION_NGA_UNUSED":
        filter = os.listdir(Env.ngaBsbDir)
        for ngaRegion in RegionNGAParser.getFiles().keys():
            aFilter = Regions.getRegionFilterList(ngaRegion)
            for ea in aFilter:
                if filter.count(ea) > 0:
                    filter.remove(ea)
    else:
        filter = Regions.getRegionFilterList(region)
    fps = FilePathSearch.FilePathSearch(os.path.abspath(Env.ngaBsbDir), "kap", filter)
    fPaths = fps.getfilePaths()
    fPaths.sort()
    destDir = Env.bsbDir+"NGA_BSB_%s/" %(region)
    command = "ln -P %s %s"
    if not os.path.isdir(destDir):
        os.makedirs(destDir)
    kapFiles = []
    for each in fPaths:
        kapFiles.append(each.split("/")[-1])
    for existing in os.listdir(Env.bsbDir+"NGA_BSB_%s/" %(region)):
        if not kapFiles.__contains__(existing):
            #print "removing:"+existing
            os.remove(Env.bsbDir+"NGA_BSB_%s/" %(region)+existing)
            deleted += 1
        else:
            kept += 1
            #print "keeping:"+existing
    for fPath in fPaths:
        kapFile = fPath.split("/")[-1]
        link = destDir+kapFile
        if not os.path.isfile(link):
            #print link
            created += 1
            cmd = command %(fPath, link)
            subprocess.Popen(shlex.split(cmd))
    
    print "<file>.kap links created in directory: " + Env.bsbDir+"NGA_BSB_%s/" %(region)
    print "Deleted", deleted, "links"
    print "Kept", kept, "links"
    print "Created", created, "links"



if __name__=="__main__":
    err = "You must supply a valid NGA REGION"
    if not sys.argv.__len__() == 2:
        print err
    else:
        region = sys.argv[1]
        if Regions._isNGARegion(region):
            doIt(sys.argv[1])
        elif region == "REGION_NGA_UNUSED":
            doIt("REGION_NGA_UNUSED")
        else:
            print err