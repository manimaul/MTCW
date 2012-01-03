#!/usr/bin/env python
# -*- coding: utf-8 -*-

import NoaaXmlParser, Env
import os

descriptions = { \
"REGION_NGA_01" : "Mexico West Coast to Columbian Border", \
"REGION_NGA_02" : "South America West Coast: Columbia to Cape Horn", \
"REGION_02" : "Block Island RI to the Canadian Border", \
"REGION_03" : "New York to Nantucket and Cape May NJ", \
"REGION_04" : "Chesapeake and Delaware Bays", \
"REGION_06" : "Norfolk VA to Florida including the ICW", \
"REGION_07" : "Florida East Coast and the Keys", \
"REGION_08" : "Florida West Coast and the Keys", \
"REGION_10" : "Puerto Rico and the U.S. Virgin Islands", \
"REGION_12" : "Southern California: Point Arena to the Mexican Border", \
"REGION_13" : "Lake Michigan", \
"REGION_14" : "San Francisco to Cape Flattery", \
"REGION_15" : "Pacific Northwest: Puget Sound to the Canadian Border", \
"REGION_17" : "Mobile AL to the Mexican Border", \
"REGION_22" : "Lake Superior and Lake Huron (U.S. Waters)", \
"REGION_24" : "Lake Erie (U.S. Waters)", \
"REGION_26" : "Lake Ontario (U.S. Waters)", \
"REGION_30" : "Southeast Alaska", \
"REGION_32" : "South Central Alaska: Yakutat to Kodiak", \
"REGION_34" : "Alaska: The Aleutians and Bristol Bay", \
"REGION_36" : "Alaska: Norton Sound to Beaufort Sea", \
"REGION_40" : "Hawaiian Islands and U.S. Territories", \
"REGION_BR" : "Brazil: Guyana to Uruguay"
}

def isNGARegion(region):
    if os.path.isfile(Env.ngaRegionDir+region+".dat"):
        return True
    return False

def _getNGAFilterList(region):
    datFilePath = Env.ngaRegionDir+region+".dat"
    filterList = []
    if os.path.isfile(datFilePath):
        datFile = open(datFilePath, "r")
        for line in datFile.readlines():
            if not line.startswith("#"):
                filterList.append(line.rstrip("\n"))
        datFile.close()
    filterList.sort()
    return filterList
        
#ngaLinker = { \
#"REGION_NGA01" : REGION_NGA01, \
#"REGION_NGA02" : REGION_NGA02, \
#}

def printRegionList():
    regions = descriptions.keys()
    regions.sort()
    for region in regions:
        print region

def getRegionFilterList(region):
    if isNGARegion(region):
        return _getNGAFilterList(region)
    if NoaaXmlParser.xmlUrls.has_key(region):
        return NoaaXmlParser.NoaaXmlParser(region).getKapFiles()
    if region == "REGION_BC":
        return os.listdir(Env.canadaBsbDir)
    if region == "REGION_NZ":
        return os.listdir(Env.newZelandBsbDir)
    if region == "REGION_BR":
        return os.listdir(Env.brazilBsbDir)
    
def _getRegionTileDir(region):
    if isNGARegion(region):
        return "NGA/"
    if NoaaXmlParser.xmlUrls.has_key(region):
        return "NOAA/"
    if region == "REGION_BC":
        return "BC/"
    if region == "REGION_NZ":
        return "NZ/"
    if region == "REGION_BR":
        return "BR/"
    
def getRegionMergedTileDir(region):
    return Env.mergedTileDir + region
    
def getRegionUnMergedTileDir(region):
    return Env.unMergedTileDir + _getRegionTileDir(region)
    
def getRegionBsbDir(region):
    if isNGARegion(region):
        return Env.ngaBsbDir
    if NoaaXmlParser.xmlUrls.has_key(region):
        return Env.noaaBsbDir
    if region == "REGION_BC":
        return Env.canadaBsbDir
    if region == "REGION_NZ":
        return Env.newZelandBsbDir
    if region == "REGION_BR":
        return Env.brazilBsbDir
    
if __name__== "__main__":
    regions = descriptions.keys()
    regions.sort()
    for r in regions:
        print r
