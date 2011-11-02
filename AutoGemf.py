#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, subprocess, shlex, sys

class createGemf():
    def __init__(self, directory):
        if not os.path.isdir(directory + "/gemf"):
            os.mkdir(directory + "/gemf")
            if os.path.isdir(directory+"/merge"):
                shutil.move(directory+"/merge", directory+"/gemf")
            else:
                print "you need to merge files first!"
                sys.exit()

        logfile = directory + "/gemflog.txt"
        log = open(logfile, "wb")
        command = "python /home/will/tilers_tools_plus/generate_efficient_map_file.py " + directory + "/gemf"
        print "creating gemf..."
        #print command
        thisone = subprocess.Popen(shlex.split(command), stdout=log)
        thisone.wait()
        log.close()
        
if __name__== "__main__":
    import NoaaXmlParser
    
    regionlst = NoaaXmlParser.xmlUrls.keys()

    if not sys.argv.__len__() == 2:
        print "You must supply a region"
        sys.exit()
    
    region = sys.argv[1]
    
    if not regionlst.__contains__(region):
        print "Invalid region"
        sys.exit()
    
    #region = "NOAA_BSB_REGION_01"
    regiondir = "/home/will/charts/" + region + '.opt'
    createGemf(regiondir)
    os.rename(regiondir+'/gemf/map_data.gemf', '/home/will/charts/'+region+'.gemf')
