#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import csv
from xml.dom import minidom

#11 scales in 

class VrtScaleToZoom():
    def __init__(self, vrtPath):
        self.scale = None
        if os.path.isfile(vrtPath):
            dom = minidom.parse(vrtPath)
            for node in dom.getElementsByTagName("MDI"):
                str = node.toxml()
                if str.find("BSB_KNP") >= 0:
                    li = str.find("SC=")+3
                    ri = str.find(",", li+1)
                    self.scale = int(str[li:ri])
                    
    def getScale(self):
        return self.scale
    
    def getZoom(self):
        scale = self.getScale()
        scaleDict = {}
        csvReader = csv.reader(open('C:\\Users\will\\workspace\\bsbTileTools\\src\\bsbScales.csv', 'rb'))
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
    vrtPath = "C:\\Users\\will\\Desktop\\andoid-map-dev\\chart-tiles\\All_RNCs\BSB_ROOT\\13227\\13227_2.vrt"
    vstz = VrtScaleToZoom(vrtPath)
    print vstz.getZoom()
