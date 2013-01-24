#!/usr/bin/env python
# -*- coding: utf-8 -*-

import NoaaXmlParser, Env, RegionNGAParser
import os

#NGA region descriptions defined in REGION_NGA_##.dat
descriptions = {
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
"REGION_BC_01" : "Canada West Coast", \
"REGION_BR" : "Brazil: Guyana to Uruguay", \
"REGION_NZ" : "New Zealand and South Pacific: Samoa to Ross Sea"
}

def _isNGARegion(region):
    if RegionNGAParser.getDescriptions().has_key(region):
        return True
    return False
#    if os.path.isfile(Env.ngaRegionDir+region+".dat"):
#        return True
#    return False

def _isNOAARegion(region):
    if NoaaXmlParser.xmlUrls.has_key(region):
        return True
    return False

def _isBrazilRegion(region):
    if region.startswith("REGION_BR"):
        return True
    return False

def _isCanadaRegion(region):
    if region.startswith("REGION_BC"):
        return True
    return False

def _isNewZealandRegion(region):
    if region.startswith("REGION_NZ"):
        return True
    return False

def _getNGAFilterList(region):
    datFilePath = Env.ngaRegionDir+RegionNGAParser.getFiles()[region]
    #datFilePath = Env.ngaRegionDir+region+".dat"
    filterList = []
    if os.path.isfile(datFilePath):
        datFile = open(datFilePath, "r")
        for line in datFile.readlines():
            if not line.startswith("#"):
                filterList.append(line.rstrip("\n"))
        datFile.close()
    filterList.sort()
    return filterList

def printRegionList():
    regions = []
    for ea in descriptions.keys():
        regions.append(ea)
    for ea in RegionNGAParser.getDescriptions().keys():
        regions.append(ea)
    regions.sort()
    for region in regions:
        print region

def getRegionFilterList(region):
    list = []
    if _isNGARegion(region):
        return _getNGAFilterList(region)
    if _isNOAARegion(region):
        return NoaaXmlParser.NoaaXmlParser(region).getKapFiles()
    if _isCanadaRegion(region):
        for ea in os.listdir(Env.canadaBsbDir):
            if ea.endswith(".KAP"):
                list.append(ea)
            if ea.endswith(".kap"):
                list.append(ea)
        return list
    if _isNewZealandRegion(region):
        for ea in os.listdir(Env.newZelandBsbDir):
            if ea.endswith(".KAP"):
                list.append(ea)
            if ea.endswith(".kap"):
                list.append(ea)
        return list
    if _isBrazilRegion(region):
        for ea in os.listdir(Env.brazilBsbDir):
            if ea.endswith(".KAP"):
                list.append(ea)
            if ea.endswith(".kap"):
                list.append(ea)
        return list
    
def _getRegionTileDir(region):
    if _isNGARegion(region):
        return "NGA/"
    if _isNOAARegion(region):
        return "NOAA/"
    if _isCanadaRegion(region):
        return "BC/"
    if _isNewZealandRegion(region):
        return "NZ/"
    if _isBrazilRegion(region):
        return "BR/"
    
def getRegionMergedTileDir(region):
    return Env.mergedTileDir + region
    
def getRegionUnMergedTileDir(region):
    return Env.unMergedTileDir + _getRegionTileDir(region)
    
def getRegionBsbDir(region):
    if _isNGARegion(region):
        return Env.ngaBsbDir
    if _isNOAARegion(region):
        return Env.noaaBsbDir
    if _isCanadaRegion(region):
        return Env.canadaBsbDir
    if _isNewZealandRegion(region):
        return Env.newZelandBsbDir
    if _isBrazilRegion(region):
        return Env.brazilBsbDir
    
def isRegion(region):
    if _isNGARegion(region):
        return True
    if _isNOAARegion(region) and descriptions.has_key(region):
        return True
    if _isCanadaRegion(region) and descriptions.has_key(region):
        return True
    if _isNewZealandRegion(region) and descriptions.has_key(region):
        return True
    if _isBrazilRegion(region) and descriptions.has_key(region):
        return True
    return False

def getRegionDescription(region):
    if _isNGARegion(region):
        return RegionNGAParser.getDescriptions()[region]
#        datFilePath = Env.ngaRegionDir+region+".dat"
#        if os.path.isfile(datFilePath):
#            datFile = open(datFilePath, "r")
#            return datFile.readline().lstrip("#").strip()
    elif descriptions.has_key(region):
        return descriptions[region]
    return "Unknown"
    
if __name__== "__main__":
    printRegionList()
