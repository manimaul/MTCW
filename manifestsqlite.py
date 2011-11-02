import sqlite3 as sql
import sys

def createdb(filename):
    sqldat = \
'''-- Table: android_metadata
CREATE TABLE android_metadata ( 
    locale          TEXT
);

CREATE TABLE regions ( 
    name            TEXT,
    description     TEXT,
    image           TEXT,
    size            INT,
    installeddate   INT,
    latestdate      INT 
);

CREATE TABLE charts (
    region          TEXT,
    file            TEXT,
    name            TEXT,
    updated         TEXT,
    scale           INT,
    outline         TEXT,
    depths          TEXT
);

INSERT INTO android_metadata VALUES ('en_US');
'''
    
    conn = sql.connect(filename)
    curs = conn.cursor()
    curs.executescript(sqldat)
    conn.commit()
    
    curs.close()
    
class DataStore:
    def __init__(self, filename):
        self.conn = sql.connect(filename)
        self.curs = self.conn.cursor()
        
    def addregion(self, name, description, image, size, idate, ldate):
        sqlstr = "insert into regions values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" \
                 %(name, description, image, size, idate, ldate)
        try:
            self.curs.execute(sqlstr)
            self.conn.commit()
        except:
            print sqlstr
            sys.exit()
    
    def addchart(self, region, file, name, updated, scale, outline, depths):
        #chart outline should be string formated like this... 
        #15,-173.0833:71.5,-173.0833:71.5,-116.5:15,-116.5:15,-173.0833
        sqlstr = "insert into charts values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" \
                 %(region, file, name.replace("'", ""), updated, scale, outline, depths)
        try:
            self.curs.execute(sqlstr)
            self.conn.commit()
        except:
            print sqlstr
            sys.exit()
        
    def Close(self):
        self.curs.close()
    
if __name__=='__main__':
    import os.path
    import time
    import NoaaXmlParser as nxl
    import BsbOutlines
    
    epoch = int(time.time())
    gemfdir = "/home/will/charts/gemfs/"

    dbf = gemfdir+"regions.s3db"
            
    if os.path.isfile(dbf):
        print "removing old region manifest"
        os.remove(dbf)
            
    print "creating new " + dbf   
    createdb(dbf)
    
    ds = DataStore(os.path.abspath(dbf))
    regionlst = os.listdir(gemfdir)
    regionlst.sort()
    for region in regionlst:
        if region.endswith(".gemf"):
            name = region.rstrip(".gemf")
            print "adding region:", name
            description = nxl.descriptions[name]
            image = name.replace("_", "").lower()
            size = os.path.getsize(gemfdir+region)
            ds.addregion(name, description, image, size, 'NULL', epoch)
            
            filter = nxl.NoaaXmlParser(name).getKapFiles()
            bsbdir = "/home/will/charts/BSB_ROOT"
            bo = BsbOutlines.BsbOutlines(bsbdir, filter)
            for key in bo.getkeys():
                #print key
                #region, file, name, updated, scale, outline, depths
                ds.addchart(name, key, bo.getname(key), bo.getupdated(key), bo.getscale(key), \
                            bo.getoutline(key), bo.getdepthunits(key))
            
    ds.Close()
