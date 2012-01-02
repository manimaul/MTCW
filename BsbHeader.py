#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path

class BsbHeader():
    def __init__(self, kapPath):
        self.kapPath = kapPath
        self.updated = None
        self.name = None
        self.lines = []
        self.poly = []
        self.scale = None
        self.projection = None
        self.units = None
        self.__readHeader(kapPath)
    
    def __readHeader(self, kapPath):
        with open(kapPath,'rU') as kapFile:
            for line in kapFile:
                if '\x1A' in line:
                    break
                line=line.decode('cp1252','ignore')
                self.lines.append(line)
                
                if line.find("KNP/SC") > -1:
                    li = line.find("KNP/SC")+7
                    ri = line.find(",")
                    self.scale = int(line[li:ri])
                    
                    li = line.find("GD=")+3
                    ri = line.find(",", li)
                    self.projection = line[li:ri]
                    
                if line.find("UN=") > -1:
                    li = line.find("UN=")+3
                    ri = line.find(",", li)
                    self.units = line[li:ri]
                
                if line.find("CED/SE") > -1:
                    li = line.find("ED=")+3
                    ri = li+11
                    self.updated = line[li:ri]
                    
                if line.find("BSB/NA") > -1:
                    li = line.find("BSB/NA=")+7
                    ri = line.find(",")
                    self.name = line[li:ri]
                    
                if line.find("PLY/") > -1:
                    lat = line.split(",")[1].lstrip(',')
                    lon = float(line.split(",")[2])
#                    if lon > 0: #fix for osmdroid
#                        lon = lon - 360.0
                    ply = lat + "," + str(lon)
                    self.poly.append(ply.rstrip())
        if self.poly.__len__() > 0:
            self.poly.append(self.poly[0]) #add first coord to close polygon

    def getlines(self):
        return self.lines
    
    def getupdated(self):
        return self.updated.strip()
    
    def getscale(self):
        return self.scale
    
    def getprojection(self):
        return self.projection.strip()
    
    def getbasefile(self):
        return os.path.basename(self.kapPath)
    
    def getname(self):
        return self.name.strip().replace("'","")
    
    def getPolyList(self):
        return self.poly
    
    def getOutline(self):
        outline = ""
        for ply in self.getPolyList():
            outline += ply + ":"
        return outline.rstrip(":")
    
    def getDepthUnits(self):
        if self.units == None:
            self.units = "Unknown"
        return self.units
    
    def getCenter(self):
        lats = []
        lons = []
        for ll in self.poly:
            lat, lon = ll.split(",")
            lats.append(float(lat))
            lons.append(float(lon))
        centerlat =  min(lats) + (max(lats) - min(lats)) / 2
        centerlon =  min(lons) + (max(lons) - min(lons)) / 2
        return (centerlon, centerlat)
               
if __name__== "__main__":
    dir = "/home/will/charts/BSB_ROOT/16082/16082_1.KAP"
    header = BsbHeader(dir)
    print header.getCenter()
#    print header.getbasefile()
#    print header.getprojection()
#    print header.getscale()
#    print header.getupdated()
#    print header.getname()
#    print header.getPolyList()
#    print header.getOutline()
#    print header.getDepthUnits()
# for line in header.getlines():
# print line
        
        
        
