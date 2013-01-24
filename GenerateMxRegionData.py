#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import BsbOutlines
import Env
import Regions
import codecs
import os.path
import sys
import time
import zipfile

#        CREATE TABLE regions ( 
#            name          TEXT,
#            description   TEXT,
#            image         TEXT,
#            size          INT,
#            installeddate INT,
#            latestdate    INT );

#str0 = "UPDATE regions SET installeddate='%s', mergeorder='%s' WHERE name='%s';"
str0 = "UPDATE regions SET installeddate='%s' WHERE name='%s';\n"
strcustom0 = u"DELETE from regions WHERE name='%s';\n"
strcustom1 = u"INSERT into [regions] ([name], [description], [image], [size], [installeddate] ) VALUES ('%s', '%s', '%s', '%s', '%s');\n"
str1 = u"DELETE from charts where region='%s';\n"
str2 = u"INSERT INTO [charts] ([region], [file], [name], [updated], [scale], [outline], [depths], [zoom]) VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s', '%s');\n"
#dir = '/home/will/charts/gemfs_version2'
#region = "REGION_40"
#epoch = "1324500235"
#epoch = "1331534724"
epoch = "1358984906"
custom = False;
#epoch = int(time.time())

def generateUpdate():
    sqlFname = "UPDATE.sql"
    sqlPath = Env.gemfDir+"/"+sqlFname
    zdat = zipfile.ZipFile(Env.gemfDir+"/UPDATE.zdat", "w", zipfile.ZIP_DEFLATED)
    sqlf = open(sqlPath, "w")
    os.chdir(Env.gemfDir)
    lst = os.listdir(Env.gemfDir)
    lst.sort()
    
    sqlstr = u"update regions set latestdate='%s', size='%s' where name='%s';"
    sqlf.write(u"--MXMARINER-DBVERSION:1\n")
    for p in lst:
        if p.endswith(".gemf"):
            size = str(os.path.getsize(p))
            region = p.rstrip(".gemf")
            sqlf.write(sqlstr %(epoch, size, region)+"\n")
    print "update writen to: " + Env.gemfDir+'/UPDATE.sql'
    sqlf.close()
    zdat.write(sqlPath, sqlFname)
    os.remove(sqlPath)
    zdat.close()
    

def generateNOAA():
    import NoaaXmlParser
    for region in NoaaXmlParser.xmlUrls.keys():
        generateRegion(region)
        
def generateRegion(region):
    #fisrt lets see if the gemf is there
    
    print "generating data for " + region
    filter = Regions.getRegionFilterList(region)
    bo = BsbOutlines.BsbOutlines(Env.bsbDir, filter)
#    bsbScales = BsbScales(Env.bsbDir, filter)
#    sortList = bsbScales.getKapsSortedByScale()
#    sortList.reverse()
#    mergeorder = ""
#    for item in sortList:
#        mergeorder += item + ":"
#    mergeorder.rstrip(":")
    sqlFname = region+".sql"
    sqlPath = Env.gemfDir+"/"+sqlFname
    zdatPath = Env.gemfDir+"/"+region+".zdat"
    sqlf = codecs.open(sqlPath, "w", "utf-8")
    zdat = zipfile.ZipFile(zdatPath, "w", zipfile.ZIP_DEFLATED)
    #sqlf = open(Env.gemfDir+"/"+region+".bin", "wb")
    
    wrt = u"--MXMARINER-DBVERSION:3\n"
    #zdat.writestr( sqlFname, wrt)
    sqlf.write( wrt )
    
    if (custom):
        gemfFile = Env.gemfDir+region+".gemf"
        if not os.path.isfile(gemfFile):
            print "gemf not ready:" + region
            sys.exit()
        else:
            bytes = os.path.getsize(gemfFile)
        wrt = strcustom0 %(region)
        sqlf.write( wrt )
        #zdat.writestr( sqlFname, wrt)
        
        #[name], [description], [image], [size], [installeddate]
        wrt = strcustom1 %(region, Regions.getRegionDescription(region), region.lower().replace("_", ""), bytes, epoch)
        sqlf.write( wrt )
        #zdat.writestr( sqlFname, wrt)
    else:
        #wrt = str0 %(epoch, mergeorder, region)
        wrt = str0 %(epoch, region)
        sqlf.write( wrt )
        #zdat.writestr( sqlFname, wrt)
    
    wrt = str1 %(region) 
    sqlf.write( wrt )
    #zdat.writestr( sqlFname, wrt)
    
    for kapfile in bo.getkeys():
        wrt = str2 %(region, kapfile, bo.getname(kapfile), bo.getupdated(kapfile), bo.getscale(kapfile), \
                     bo.getoutline(kapfile), bo.getdepthunits(kapfile), bo.getzoom(kapfile));
        sqlf.write( wrt )
        #zdat.writestr( sqlFname, wrt)
    
    sqlf.close()
    zdat.write(sqlPath, sqlFname)
    os.remove(sqlPath)
    zdat.close()
#    rootlen = len(target_dir) + 1
#    zdat.write(sqlPath, compress_type)
#    zdat.write(fn, fn[rootlen:])       

if __name__== "__main__":
    if not sys.argv.__len__() == 2:
        print "You must supply a region:"
        Regions.printRegionList()
        #print "Or you can also do: ALL_NGA, ALL_NOAA, or PRINTARRAY"
        sys.exit()
    else:
        arg = sys.argv[1]
        if arg == "ALL_NOAA":
            generateNOAA()
        elif arg == "ALL_NGA":
            print "not yet implemented"
        elif Regions.isRegion(arg):
            generateRegion(arg)
        elif arg== "UPDATE":
            generateUpdate();
        else:
            print "invalid argument", arg
