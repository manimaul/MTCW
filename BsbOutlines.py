#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FilePathSearch import FilePathSearch
from BsbHeader import BsbHeader

class BsbOutlines():
    def __init__(self, directory, filter=None):
        self.data = {}
        fps = FilePathSearch(directory, 'KAP', filter)
        for map_file in fps.getfilePaths():
            self._read(map_file)
    
    def _read(self, map_file):
        header = BsbHeader(map_file)
        key = header.getbasefile()
        data = [header.getname(), header.getupdated(), header.getscale(), header.getOutline(), header.getDepthUnits(), "NULL"]
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
    
    def getzooms(self, key):
        return self.data[key][5]
    
if __name__== "__main__":
    
    bo = BsbOutlines("/home/will/zxyCharts/BSB_ROOT/BR_BSB_ROOT", "210301.KAP")
    print type(bo.getname("210301.KAP"))
    print bo.getname("210301.KAP")
    print bo.getupdated("210301.KAP")
    print bo.getscale("210301.KAP")
    print bo.getoutline("210301.KAP")
    print bo.getdepthunits("210301.KAP")
