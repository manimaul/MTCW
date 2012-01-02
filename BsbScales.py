#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FilePathSearch import FilePathSearch

""" Scales in 2011 NOAA BSB Catalog
2500, 3500, 5000, 6000, 6500, 7500, 8000, 10000, 12000, 12500, 
15000, 20000, 24000, 25000, 25475, 26420, 30000, 32500, 36481, 
38730, 40000, 41275, 42240, 45602, 47750, 47943, 48000, 48149, 
48767, 48973, 49177, 49590, 49794, 50000, 50204, 50615, 50819, 
51024, 51639, 52150, 60000, 72962, 75000, 77062, 77477, 77812, 
78000, 78900, 79291, 79334, 80000, 80660, 80728, 80905, 81326, 
81436, 81529, 81847, 82662, 83074, 100000, 106600, 120000, 135000, 
150000, 160000, 170000, 175000, 176253, 180000, 180789, 185238, 
191730, 194154, 196948, 200000, 207840, 209978, 210668, 216116, 
217828, 220000, 229376, 232188, 234270, 240000, 247482, 250000, 
300000, 326856, 350000, 378838, 400000, 419706, 432720, 449659, 
456394, 458596, 460732, 466940, 470940, 500000, 600000, 642271, 
653219, 663392, 675000, 700000, 736560, 811980, 868003, 875000, 
931650, 969756, 969761, 1023188, 1058400, 1126321, 1200000, 1444000, 
1500000, 1534076, 1587870, 1650000, 2100000, 2160000, 3121170, 
3500000, 4860700, 10000000
"""

class BsbScales():
    def __init__(self, directory, filter=None):
        self.scales = {}
        self.projections = {}
        fps = FilePathSearch(directory, 'KAP', filter)
        for map_file in fps.getfilePaths():
            self.__readScale(map_file)
    
    def __readScale(self, map_file):
        with open(map_file,'rU') as kapFile:
            for line in kapFile:
                if '\x1A' in line:
                    break
                line=line.decode('cp1252','ignore')
                if line.find("KNP/SC") > -1:
                    scale = int(line[line.find("KNP/SC")+7:line.find(",")])
                    if not self.scales.__contains__(scale):
                        self.scales[scale] = []
                    self.scales[scale].append(map_file)
                    start = line.find("GD=")+3
                    end = line.find(",", start)
                    projection = line[start:end]
                    if not self.projections.__contains__(projection):
                        self.projections[projection] = []
                    self.projections[projection].append(map_file)

    def getChartsAtScale(self, scale):
        if self.scales.has_key(scale):
            charts = []
            for chart in self.scales[scale]:
                charts.append(chart.split("/")[-1])
                charts.sort()
            return charts
        
    def getScaleList(self):
        keyList = self.scales.keys()
        keyList.sort()
        return keyList
    
    def printScales(self):
        keyList = self.scales.keys()
        keyList.sort()
        for key in keyList:
            print key
    
    def printProjections(self):
        keyList = self.projections.keys()
        for key in keyList:
            print key, self.projections[key].__len__()
            
    def getKapsSortedByScale(self, addExt = ""):
        lst = []
        keyList = self.scales.keys()
        keyList.sort()
        keyList.reverse()
        for key in keyList:
            for scale in self.scales[key]:
                item = scale.split("/")[-1].rstrip(".KAP")
                item = item.rstrip(".kap")
                lst.append(item+addExt)
        return lst
            
               
if __name__== "__main__":
#    import sys, os.path
#    if not sys.argv.__len__() == 2:
#        print "You must supply a ROOT BSB directory"
#        sys.exit()
#    
#    dir = sys.argv[1]
#    if not os.path.isdir(dir):
#        print dir, "is not a directory"
#        sys.exit()

    import os.path, subprocess, shutil
    dir = "/home/will/charts/BSB_ROOT"
    bsbScales = BsbScales(dir)
    tiledir = '/home/will/charts/BSB_ALL/'
    #lst = bsbScales.getChartsAtScale(10000)
    lst = os.listdir(tiledir)
    i = 1;
    for ch in lst:
        target = tiledir+os.path.basename(ch).rstrip("KAP")#+"zxy"
        if os.path.isdir(target):
#            shutil.rmtree(target)
            i += 1;
            if (i < 5):
                command = ["firefox", target + "/viewer-google.html"]
                subprocess.Popen(command)
        else:
            print "missing " + target