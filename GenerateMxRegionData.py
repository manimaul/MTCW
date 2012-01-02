#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import os.path, time, sys
import BsbOutlines, Regions, Env

# CREATE TABLE charts ( 
    # region  TEXT,
    # file    TEXT,
    # name    TEXT,
    # updated TEXT,
    # scale   INT,
    # outline TEXT,
    # depths  TEXT 
# );


#str0 = "UPDATE regions SET installeddate='%s' WHERE name='%s';\n"
str0custom = "DELETE from regions WHERE name='%s';\n"
str0custom2 = "INSERT into [regions] ([name], [description], [installeddate] ) VALUES ('%s', '%s', '%s');\n"
str1 = "DELETE from charts where region='%s';\n"
str2 = "INSERT INTO [charts] ([region], [file], [name], [updated], [scale], [outline], [depths]) VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s');\n"
#dir = '/home/will/charts/gemfs_version2'
#region = "REGION_40"
#epoch = "1324500235"
epoch = int(time.time())

def generateUpdate():
    sqlf = open(Env.gemfDir+"/UPDATE.sql", "w")
    os.chdir(Env.gemfDir)
    lst = os.listdir(Env.gemfDir)
    lst.sort()
    
    sqlstr = "update regions set latestdate='%s', size='%s' where name='%s';"
    epoch = "1324500235"
    #epoch = int(time.time())
    sqlf.write("mx.mariner.update\n")
    for p in lst:
        if p.endswith(".gemf"):
            size = str(os.path.getsize(p))
            region = p.rstrip(".gemf")
            sqlf.write(sqlstr %(epoch, size, region)+"\n")
    print "update writen to: " + Env.gemfDir+'/UPDATE.sql'

def generateNOAA():
    import NoaaXmlParser
    for region in NoaaXmlParser.xmlUrls.keys():
        generateRegion(region)
        
def generateRegion(region):
    print "generating data for " + region
    filter = Regions.getRegionFilterList(region)
    bo = BsbOutlines.BsbOutlines(Env.bsbDir, filter)
    sqlf = open(Env.gemfDir+"/"+region+".data", "w")
    sqlf.write("mx.mariner.data\n")
    sqlf.write(str0custom %(region))
    sqlf.write(str0custom2 %(region, Regions.descriptions[region], epoch))
    #sqlf.write( str0 %(epoch, region) )
    sqlf.write( str1 %(region) )
    for kapfile in bo.getkeys():
        sqlf.write( str2 %(region, kapfile, bo.getname(kapfile), bo.getupdated(kapfile), bo.getscale(kapfile), bo.getoutline(kapfile), bo.getdepthunits(kapfile)) )

def isEven(i):
    return i%2 and True or False

def printByteItemArray():
    out = ""
    i=0;
    lst = os.listdir(Env.gemfDir)
    os.chdir(Env.gemfDir)
    lst.sort()
    for p in lst:
        if p.endswith(".gemf"):
            out += "<item>" + str(os.path.getsize(p)) + "</item>"
            if isEven(i):
                out+="\n"
            i+=1
    print out
    
if __name__== "__main__":
    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        Regions.printRegionList()
        print "Or you can also do: ALL_NGA, ALL_NOAA, or PRINTARRAY"
        sys.exit()
    else:
        arg = sys.argv[1]
        if arg == "ALL_NOAA":
            generateNOAA()
        elif arg == "ALL_NGA":
            print "not yet implemented"
        elif arg == "PRINTARRAY":
            printByteItemArray()
        elif Regions.descriptions.has_key(arg):
            generateRegion(arg)
        else:
            print "invalid argument"
            print arg
