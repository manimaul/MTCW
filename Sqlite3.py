#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import sqlite3 as sql

def createdb(filename):
    sqldat = \
'''-- Table: charts
CREATE TABLE charts ( 
    file       CHAR,
    name       CHAR,
    updated    DATE,
    scale      INT,
    outline    CHAR,
    depthUnits CHAR,
    zoomRange  CHAR 
);


-- Table: region
CREATE TABLE region ( 
    creationdate INT,
    initcenter   CHAR,
    initzoom     INT,
    name         CHAR,
    description  CHAR 
);'''
    conn = sql.connect(filename)
    curs = conn.cursor()
    curs.executescript(sqldat)
    conn.commit()
    
    curs.close()

class DataStore:
    def __init__(self, filename):
        #print 'sql opening datastore: ', filename
        self.conn = sql.connect(filename)
        self.curs = self.conn.cursor()
        
    def addchart(self, file, name, updated, scale, outline, units, zoomrange):
        #chart outline should be string formated like this... 
        #15,-173.0833:71.5,-173.0833:71.5,-116.5:15,-116.5:15,-173.0833
        sql = "insert into charts values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" %(file, name.replace("\'", ""), updated, scale, outline, units, zoomrange)
        try:
            self.curs.execute(sql)
            self.conn.commit()
        except:
            print sql
            import sys
            sys.exit()
        
    def dropchartdata(self):
        self.curs.execute('delete from charts')
        self.conn.commit()
        
    def addmain(self, date, initcenter, initzoom, name, description):
        sql = "insert into region values( \'%s\', \'%s\', \'%s\', \'%s\', \'%s\' )" %(date, initcenter, initzoom, name, description)
        self.curs.execute(sql)
        self.conn.commit()
        
    def Close(self):
        #print 'sql closing datastore'
        self.curs.close()
        
if __name__=='__main__':
    import os.path, NoaaXmlParser as nxl, md5sum, datetime
    now = datetime.datetime.now()
    dir = '/home/will/charts/gemfs/'
    states = nxl.descriptions.keys()
    for state in nxl.descriptions.keys():
        if len(state)< 5:
            dbf = dir+state+".s3db"
            
            if os.path.isfile(dbf):
                print "removing: " + state
                os.remove(dbf)
            
            print "creating: " + os.path.basename(dbf)    
            createdb(dbf)
            ds = DataStore(os.path.abspath(dbf))
            ds.addmain(md5sum.getFilesum(dir+state+".gemf"), now.strftime("%m/%d/%y"), 0, 0, state, nxl.descriptions[state])
            
            ds.Close()
