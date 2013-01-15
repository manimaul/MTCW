#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
home = os.getenv("HOME")

######EDIT THIS ONLY###############
#where this (MTCW) lives 
mtcwDir = home + "/Documents/workspace-python/MTCW/"

######YOU DON'T NEED TO EDIT ANYTHING ELSE

#Output directory
rootDir = "/media/AE9A81169A80DC69/Users/will/charts/"

#bsb directory
bsbDir = rootDir + "BSB_ROOT/"
brazilBsbDir = bsbDir + "BR_BSB_ROOT/"
canadaBsbDir = bsbDir + "BC_BSB_ROOT/"
newZelandBsbDir = bsbDir + "NZ_BSB_ROOT/"
ngaBsbDir = bsbDir + "NGA_BSB_ROOT/"
noaaBsbDir = bsbDir + "NOAA_BSB_ROOT/"

#gemf directory
gemfDir = rootDir + "gemf/"

#tile directories
tileDir = rootDir + "tiles/"
mergedTileDir = tileDir + "merged/"
unMergedTileDir = tileDir + "unmerged/"

#xml cache directory
xmlCacheDir = rootDir + "xml/"


#where tilers_tools is
tilersToolsDir = mtcwDir + "tilers_tools/"

#where nga region filters live
ngaRegionDir = mtcwDir + "nga_regions/"

if __name__== "__main__":
    print "Setting up MTCW directory structure."
    if not os.path.isdir(rootDir):
        print "creating directory: " + rootDir
        os.makedirs(rootDir)
        
    if not os.path.isdir(gemfDir):
        print "creating directory: " + gemfDir
        os.mkdir(gemfDir)
        
    if not os.path.isdir(bsbDir):
        print "creating directory: " + bsbDir
        os.mkdir(bsbDir)
        
    if not os.path.isdir(tileDir):
        print "creating directory: " + tileDir
        os.mkdir(tileDir)
        
    if not os.path.isdir(mergedTileDir):
        print "creating directory: " + mergedTileDir
        os.mkdir(mergedTileDir)
        
    if not os.path.isdir(unMergedTileDir):
        print "creating directory: " + unMergedTileDir
        os.mkdir(unMergedTileDir)
        
    if not os.path.isdir(xmlCacheDir):
        print "creating directory: " + xmlCacheDir
        os.mkdir(xmlCacheDir)
        
    print "MTCW directory structure is ready :)"
        
    
        