#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import sqlite3 as sql
import os.path, NoaaXmlParser as nxl
import BsbOutlines
import datetime

# CREATE TABLE charts ( 
    # region  TEXT,
    # file    TEXT,
    # name    TEXT,
    # updated TEXT,
    # scale   INT,
    # outline TEXT,
    # depths  TEXT 
# );

str0 = "UPDATE regions SET installeddate='%s' WHERE name='%s';\n"
str1 = "DELETE from charts where region='%s';\n"
str2 = "INSERT INTO [charts] ([region], [file], [name], [updated], [scale], [outline], [depths]) VALUES ('%s', '%s', '%s', '%s', %s, '%s', '%s');\n"
now = datetime.datetime.now()
dir = '/home/will/charts/gemfs/BY_REGION'
#region = "REGION_40"
epoch = "1319485045"

for region in nxl.descriptions.keys():
        if len(region) is 9:
            print "generating sql for " + region
            filter = nxl.NoaaXmlParser(region).getKapFiles()
            bo = BsbOutlines.BsbOutlines(filter=filter)
            sqlf = open(dir+"/"+region+".sql", "w")
            sqlf.write( str0 %(epoch, region) )
            sqlf.write( str1 %(region) )
            for kapfile in bo.getkeys():
                sqlf.write( str2 %(region, kapfile, bo.getname(kapfile), bo.getupdated(kapfile), bo.getscale(kapfile), bo.getoutline(kapfile), bo.getdepthunits(kapfile)) )
        
        
        
