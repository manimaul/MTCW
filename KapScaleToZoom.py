#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import csv

class KapScaleToZoom():
    def __init__(self, kapPath):
        self.scale = None
        if os.path.isfile(kapPath):
            self.__readScale(kapPath)
    
    def __readScale(self, kapPath):
        with open(kapPath,'rU') as kapFile:
            for line in kapFile:
                if '\x1A' in line:
                    break
                line=line.decode('cp1252','ignore')
                #print line
                if line.find("KNP/SC") > -1:
                    self.scale = int(line[line.find("KNP/SC")+7:line.find(",")])
                    
    def getScale(self):
        return self.scale
    
    def getZoom(self):
        scale = self.getScale()
        scaleDict = {}
        csvReader = csv.reader(open('/home/will/tilers_tools_plus/bsbScales.csv', 'rb'))
        for row in csvReader:
            scaleDict[int(row[0])]=row[1]
        scaleKeys = scaleDict.keys()
        scaleKeys.sort()
        for key in scaleKeys:
            if scale <= key:
                zoom = scaleDict[key]
                return "\"" + zoom.replace(" ", ", ") + "\""
        return "\"5, 6, 7\""

if __name__== "__main__":             
    kapPath = "/home/will/charts/BSB_ROOT/13227/13227_2.KAP"
    kstz = KapScaleToZoom(kapPath)
    print kstz.getZoom()
