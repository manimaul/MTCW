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

from SimpleXMLWriter import XMLWriter

#        CREATE TABLE regions ( 
#            name          TEXT,
#            description   TEXT,
#            image         TEXT,
#            size          INT,
#            installeddate INT,
#            latestdate    INT );

#str0 = "UPDATE regions SET installeddate='%s' WHERE name='%s';\n"
#strcustom0 = u"DELETE from regions WHERE name='%s';\n"
#strcustom1 = u"INSERT into [regions] ([name], [description], [image], [size], [installeddate] ) VALUES ('%s', '%s', '%s', '%s', '%s');\n"
#str1 = u"DELETE from charts where region='%s';\n"
#str2 = u"INSERT INTO [charts] ([region], [file], [name], [updated], [scale], [outline], [depths], [zoom]) VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s', '%s');\n"

epoch = "1354751224"
#epoch = int(time.time())
custom = False;


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
    
    xmlFname = region+".xml"
    xmlPath = Env.gemfDir+"/"+xmlFname
    zxmlPath = Env.gemfDir+"/"+region+".zxml"
    xml = XMLWriter(codecs.open(xmlPath, "w", "utf-8"))
    zxml = zipfile.ZipFile(zxmlPath, "w", zipfile.ZIP_DEFLATED)
    gemfFile = Env.gemfDir+region+".gemf"
    
    xml.start("rml", version='1.0')
    
    xml.start("region", description=Regions.getRegionDescription(region), bytes = str(os.path.getsize(gemfFile)))
    
    
    
    
    for kapfile in bo.getkeys():
        xml.start("chart", file=kapfile, name=bo.getname(kapfile), scale=str(bo.getscale(kapfile)), depths=bo.getdepthunits(kapfile), zoom=str(bo.getzoom(kapfile)));
        xml.data(bo.getoutline(kapfile))
        xml.end("chart")
    
    xml.end("region")
    
    xml.end("rml")
    xml.close(1)
    cmd = "tidy -xml -imq " + xmlPath
    os.popen(cmd)
    zxml.write(xmlPath, xmlFname)
    os.remove(xmlPath)
    zxml.close()     

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
