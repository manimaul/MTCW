#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import os.path, time, sys, codecs
import BsbOutlines, Regions, Env

#        CREATE TABLE regions ( 
#            name          TEXT,
#            description   TEXT,
#            image         TEXT,
#            size          INT,
#            installeddate INT,
#            latestdate    INT );

str0 = "UPDATE regions SET installeddate='%s' WHERE name='%s';\n"
strcustom0 = u"DELETE from regions WHERE name='%s';\n"
strcustom1 = u"INSERT into [regions] ([name], [description], [image], [size], [installeddate] ) VALUES ('%s', '%s', '%s', '%s', '%s');\n"
str1 = u"DELETE from charts where region='%s';\n"
str2 = u"INSERT INTO [charts] ([region], [file], [name], [updated], [scale], [outline], [depths]) VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s');\n"
#dir = '/home/will/charts/gemfs_version2'
#region = "REGION_40"
#epoch = "1324500235"
epoch = "1325898951"
custom = False;
#epoch = int(time.time())

def generateUpdate():
    sqlf = open(Env.gemfDir+"/UPDATE.sql", "w")
    os.chdir(Env.gemfDir)
    lst = os.listdir(Env.gemfDir)
    lst.sort()
    
    sqlstr = u"update regions set latestdate='%s', size='%s' where name='%s';"
    epoch = "u1324500235"
    #epoch = int(time.time())
    sqlf.write(u"mx.mariner.update\n")
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
    #fisrt lets see if the gemf is there
    gemfFile = Env.gemfDir+region+".gemf"
    if not os.path.isfile(gemfFile):
        print "gemf not ready:" + region
        sys.exit()
    else:
        bytes = os.path.getsize(gemfFile)
    print "generating data for " + region
    filter = Regions.getRegionFilterList(region)
    bo = BsbOutlines.BsbOutlines(Env.bsbDir, filter)
    sqlf = codecs.open(Env.gemfDir+"/"+region+".sql", "w", "utf-8")
    #sqlf = open(Env.gemfDir+"/"+region+".bin", "wb")
    
    wrt = u"mx.mariner.data\n"
    sqlf.write( codecs.encode(wrt) )
    
    if (custom):
        wrt = strcustom0 %(region)
        sqlf.write( codecs.encode(wrt) )
        
        #[name], [description], [image], [size], [installeddate]
        wrt = strcustom1 %(region, Regions.getRegionDescription(region), region.lower().replace("_", ""), bytes, epoch)
        sqlf.write( codecs.encode(wrt) )
    else:
        wrt = str0 %(epoch, region)
        sqlf.write( codecs.encode(wrt) )
    
    wrt = str1 %(region) 
    sqlf.write( codecs.encode(wrt) )
    
    for kapfile in bo.getkeys():
        wrt = str2 %(region, kapfile, bo.getname(kapfile), bo.getupdated(kapfile), bo.getscale(kapfile), bo.getoutline(kapfile), bo.getdepthunits(kapfile))
        sqlf.write( codecs.encode(wrt) )
    
    sqlf.close()
            

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
        elif Regions.isRegion(arg):
            generateRegion(arg)
        else:
            print "invalid argument", arg
