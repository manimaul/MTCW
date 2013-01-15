#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FilePathSearch import FilePathSearch
from BsbHeader import BsbHeader
from Env import mtcwDir
from FindZoom import getZoom
import os.path

class BsbOutlines():
    def __init__(self, directory, filter=None):
        self.data = {}
        fps = FilePathSearch(directory, 'KAP', filter)
        for map_file in fps.getfilePaths():
            self._read(map_file)
    
    def _read(self, map_file):
        #see if we have a header override file
        fps = FilePathSearch(mtcwDir+"header_overrides", "txt")
        for override in fps.getfilePaths():
            if os.path.basename(override).split(".")[0] == os.path.basename(map_file).split(".")[0]:
                #print "using override", map_file
                header = BsbHeader(override)
                usedOverride = True
                break
            usedOverride = False
        #use detault header
        if not usedOverride:
            #print "not using override", map_file
            header = BsbHeader(map_file)
        key = header.getbasefile()
        data = [header.getname(), header.getupdated(), header.getscale(), header.getOutline(), header.getDepthUnits(), getZoom(header.getscale(), header.getCenter()[1])]
        self.data[key] = data
        
    def printdata(self):
        for key in self.data.keys():
            print key
            for line in self.data[key]:
                print line
            print "\n"
            
    def getkeys(self):
        return self.data.keys()
            
    def getname(self, key):
        return self.data[key][0]
    
    def getupdated(self, key):
        return self.data[key][1]
    
    def getscale(self, key):
        return self.data[key][2]
    
    def getoutline(self, key):
        return self.data[key][3]
    
    def getdepthunits(self, key):
        return self.data[key][4]
    
    def getzoom(self, key):
        return self.data[key][5]
    
if __name__== "__main__":
    
    bo = BsbOutlines("/home/will/zxyCharts.old/BSB_ROOT/BR_BSB_ROOT/200")
    for each in bo.getkeys():
        print each
        print bo.getoutline(each)
        print bo.getname(each)
        print bo.getupdated(each)
        print bo.getscale(each)
        print bo.getdepthunits(each)
        print "\n"
