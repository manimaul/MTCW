import RegionNGAParser, Env
import os, sys

def isEven(i):
    return i%2 and True or False

def printNGANames():
    nameStr = "<string name=\"%s\">%s</string> "
    strOut = ""
    num = 0
    regionList = RegionNGAParser.getDescriptions().keys()
    regionList.sort()
    for region in regionList:
        base = region.lower().replace("_", "")
        strOut += nameStr %(base, region)
        if isEven(num):
            strOut += "\n"
        num +=1
    print strOut

def printNGANameArray():
    nameItemStr = "<item>@string/%s</item> "
    strOut = ""
    num = 0
    regionList = RegionNGAParser.getDescriptions().keys()
    regionList.sort()
    for region in regionList:
        base = region.lower().replace("_", "")
        strOut += nameItemStr %(base)
        if isEven(num):
            strOut += "\n"
        num +=1
    print strOut
    
def printNGADescs():
    descStr = "<string name=\"desc_%s\">%s</string> "
    strOut = ""
    num = 0
    regionDescs = RegionNGAParser.getDescriptions()
    regionList = regionDescs.keys()
    regionList.sort()
    for region in regionList:
        base = region.lower().replace("_", "")
        strOut += descStr %(base, regionDescs[region])
        if isEven(num):
            strOut += "\n"
        num +=1
    print strOut
    
def printNGADescArray():
    descItem = "<item>@string/desc_%s</item>"
    strOut = ""
    num = 0
    regionDescs = RegionNGAParser.getDescriptions()
    regionList = regionDescs.keys()
    regionList.sort()
    for region in regionList:
        base = region.lower().replace("_", "")
        strOut += descItem %(base)
        if isEven(num):
            strOut += "\n"
        num +=1
    print strOut
    
def printNGAIntegers():
    intStr = "<integer name=\"bytes_%s\">%s</integer>"
    strOut = ""
    num=0
    
    regionList = RegionNGAParser.getDescriptions().keys()
    regionList.sort()
    for region in regionList:
        base = region.lower().replace("_", "")
        gemf = Env.gemfDir + region + ".gemf"
        if os.path.isfile(gemf):
            strOut += intStr %(base, str(os.path.getsize(gemf)))
        else:
            strOut += intStr %(base, "0")
            
        if isEven(num):
            strOut +="\n"
        num+=1
        
    print strOut
    
def printNGAIntArray():
    descItem = "<item>@integer/bytes_%s</item>"
    strOut = ""
    num = 0
    regionDescs = RegionNGAParser.getDescriptions()
    regionList = regionDescs.keys()
    regionList.sort()
    for region in regionList:
        base = region.lower().replace("_", "")
        strOut += descItem %(base)
        if isEven(num):
            strOut += "\n"
        num +=1
    print strOut
        
printNGAIntegers()