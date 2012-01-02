#!/usr/bin/env python
# -*- coding: utf-8 -*-

import NoaaXmlParser, Env
import sys, os

descriptions = { \
"NGA_01" : "Mexico West Coast to Columbian Border", \
"NGA_02" : "Mediteranean Sea", \
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
"REGION_40" : "Hawaiian Islands and U.S. Territories"
}

NGA_01 = [ \
"51.kap", "502.kap", "503.kap", "18000.kap", \
"18722.kap", "18723.kap", "18766", "21005.kap", "21026.kap", "21401.kap", \
"21520.kap", "21550.kap", "21583.kap", "21008.kap", "21033.kap", "21160.kap", \
"21478.kap", "21521.kap", "21560.kap", "21584.kap", "21011.kap", "21036.kap", \
"21482.kap", "21524.kap", "21561.kap", "21601.kap", "21100.kap", "21180.kap", \
"21483.kap", "21529.kap", "21562.kap", "21603.kap", "21017.kap", "21120.kap", \
"21182.kap", "21530.kap", "21563.kap", "21604.kap", "21020.kap", "21121.kap", \
"21200.kap", "21490.kap", "21540.kap", "21580.kap", "21605.kap", "21021.kap", \
"21122.kap", "21301.kap", "21500.kap", "21544.kap", "21581.kap", "21023.kap", \
"21140.kap", "21338.kap", "21510.kap", "21546.kap", "21582.kap", "21641.kap", \
"21621.kap", "21141.kap" "22040.kap"
] ##THESE CHARTS HAVE PROBLEMS "21489.kap", "21161.kap", "21014.kap"

NGA_02 = [ \
"301.kap", "302.kap","310.kap", "51160.kap", \
"52031.kap", "52042.kap", "52046.kap", "52060.kap", "52066.kap", "52082.kap", "52092.kap", "52119.kap", "52124.kap", "52142.kap", "52164.kap", "52180.kap", "52200.kap", "52262.kap", "52282.kap", \
"52039.kap", "52043.kap", "52054.kap", "52061.kap", "52069.kap", "52083.kap", "52117.kap", "52120.kap", "52125.kap", "52160.kap", "52170.kap", "52184.kap", "52202.kap", "52263.kap", \
"52040.kap", "52045.kap", "52055.kap", "52062.kap", "52080.kap", "52088.kap", "52118.kap", "52121.kap", "52140.kap", "52161.kap", "52172.kap", "52186.kap", "52221.kap", "52281.kap", \
"53011.kap", "53061.kap", "53065.kap", "53083.kap", "53087.kap", "53091.kap", "53120.kap", "53130.kap", "53160.kap", "53180.kap", "53201.kap", "53205.kap", "53226.kap", "53263.kap", "53269.kap", "53284.kap", "53301.kap", "53322.kap", \
"53031.kap", "53062.kap", "53066.kap", "53084.kap", "53088.kap", "53093.kap", "53122.kap", "53135.kap", "53161.kap", "53182.kap", "53202.kap", "53212.kap", "53242.kap", "53264.kap", "53279.kap", "53285.kap", "53302.kap", \
"53058.kap", "53063.kap", "53081.kap", "53085.kap", "53089.kap", "53100.kap", "53123.kap", "53141.kap", "53164.kap", "53183.kap", "53203.kap", "53220.kap", "53244.kap", "53266.kap", "53281.kap", "53287.kap", "53306.kap", \
"53060.kap", "53064.kap", "53082.kap", "53086.kap", "53090.kap", "53106.kap", "53125.kap", "53147.kap", "53166.kap", "53200.kap", "53204.kap", "53223.kap", "53262.kap", "53268.kap", "53283.kap", "53290.kap", "53311.kap", \
"54040.kap", "54085.kap", "54120.kap", "54162.kap", "54180.kap", "54223.kap", "54280.kap", "54289.kap", "54318.kap", "54335.kap", "54347.kap", "54364.kap", "54380.kap", "54404.kap", "54416.kap", "54423.kap", "54481.kap", \
"54043.kap", "54089.kap", "54125.kap", "54165.kap", "54181.kap", "54224.kap", "54282.kap", "54300.kap", "54320.kap", "54340.kap", "54366.kap", "54382.kap", "54406.kap", "54417.kap", "54425.kap", \
"54060.kap", "54090.kap", "54131.kap", "54166.kap", "54200.kap", "54225.kap", "54283.kap", "54301.kap", "54322.kap", "54341.kap", "54360.kap", "54367.kap", "54386.kap", "54407.kap", "54418.kap", "54430.kap", \
"54063.kap", "54095.kap", "54140.kap", "54167.kap", "54201.kap", "54226.kap", "54284.kap", "54302.kap", "54324.kap", "54343.kap", "54361.kap", "54368.kap", "54389.kap", "54408.kap", "54419.kap", "54440.kap", \
"54064.kap", "54105.kap", "54151.kap", "54168.kap", "54220.kap", "54230.kap", "54285.kap", "54303.kap", "54332.kap", "54344.kap", "54362.kap", "54369.kap", "54412.kap", "54421.kap", "54441.kap", \
"54083.kap", "54115.kap", "54161.kap", "54169.kap", "54222.kap", "54279.kap", "54287.kap", "54314.kap", "54333.kap", "54346.kap", "54363.kap", "54372.kap", "54403.kap", "54413.kap", "54422.kap", "54480.kap", \
#"55001.kap", "55041.kap", "55044.kap", "55046.kap", "55048.kap", "55064.kap", "55085.kap", "55101.kap", "55104.kap", "55110.kap", "55127.kap", "55130.kap", "55138.kap", "55140.kap", "55150.kap", "55170.kap", "55190.kap", "55205.kap", \
#"55040.kap", "55042.kap", "55045.kap", "55047.kap", "55061.kap", "55084.kap", "55100.kap", "55102.kap", "55105.kap", "55120.kap", "55129.kap", "55131.kap", "55139.kap", "55141.kap", "55160.kap", "55180.kap", \
"56011.kap", "56041.kap", "56063.kap", "56100.kap", "56102.kap", "56104.kap", "56160.kap", "56182.kap", "56191.kap", "56195.kap", "56220.kap", "56222.kap", \
"56031.kap", "56060.kap", "56065.kap", "56101.kap", "56103.kap", "56105.kap", "56180.kap", "56190.kap", "56192.kap", "56200.kap", "56221.kap"
] ##THESE CHARTS HAVE PROBLEMS "55200.kap",  "54400.kap", "54349.kap",

ngaLinker = { \
"NGA_01" : NGA_01, \
"NGA_02" : NGA_02, \
}

def printRegionList():
    regions = descriptions.keys()
    regions.sort()
    for region in regions:
        print region

def getRegionFilterList(region):
    if ngaLinker.has_key(region):
        return ngaLinker[region]
    if NoaaXmlParser.xmlUrls.has_key(region):
        return NoaaXmlParser.NoaaXmlParser(region).getKapFiles()
    if region is "REGION_BC":
        return os.listdir(Env.canadaBsbDir)
    if region is "REGION_NZ":
        return os.listdir(Env.newZelandBsbDir)
    if region is "REGION_BR":
        return os.listdir(Env.brazilBsbDir)
    
def _getRegionTileDir(region):
    if ngaLinker.has_key(region):
        return "NGA/"
    if NoaaXmlParser.xmlUrls.has_key(region):
        return "NOAA/"
    if region is "REGION_BC":
        return "BC/"
    if region is "REGION_NZ":
        return "NZ/"
    if region is "REGION_BR":
        return "BR/"
    
def getRegionMergedTileDir(region):
    return Env.mergedTileDir + region
    
def getRegionUnMergedTileDir(region):
    return Env.unMergedTileDir + _getRegionTileDir(region)
    
def getRegionBsbDir(region):
    if ngaLinker.has_key(region):
        return Env.ngaBsbDir
    if NoaaXmlParser.xmlUrls.has_key(region):
        return Env.noaaBsbDir
    if region is "REGION_BC":
        return Env.canadaBsbDir
    if region is "REGION_NZ":
        return Env.newZelandBsbDir
    if region is "REGION_BR":
        return Env.brazilBsbDir
    

#if __name__== "__main__":
#    from FilePathSearch import FilePathSearch
#    filter = getRegionFilterList("NGA_01")
#    if filter == None:
#        sys.exit(0)
#    kapPaths = FilePathSearch(Env.bsbDir, "kap", filter)
#    for kPath in kapPaths.getfilePaths():
#        print kPath