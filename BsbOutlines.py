from FilePathSearch import FilePathSearch
from BsbHeader import BsbHeader

class BsbOutlines():
    def __init__(self, directory="/home/will/charts/BSB_ROOT", filter=None):
        self.data = {}
        fps = FilePathSearch(directory, 'KAP', filter)
        for map_file in fps.getfilePaths():
            self._read(map_file)
    
    def _read(self, map_file):
        header = BsbHeader(map_file)
        key = header.getbasefile()
        data = [header.getname(), header.getupdated(), header.getscale(), header.getOutline(), header.getDepthUnits(), "NULL"]
        self.data[key] = data
        
    def printdata(self):
        for key in self.data.keys():
            print key
            for line in self.data[key]:
                print line
            print "\n"
            
    def getkeys(self):
        return self.data.keys()
            
    def getname(self, key):
        return self.data[key][0]
    
    def getupdated(self, key):
        return self.data[key][1]
    
    def getscale(self, key):
        return self.data[key][2]
    
    def getoutline(self, key):
        return self.data[key][3]
    
    def getdepthunits(self, key):
        return self.data[key][4]
    
    def getzooms(self, key):
        return self.data[key][5]
        
    
if __name__== "__main__":
    from Sqlite3 import DataStore, createdb
    import NoaaXmlParser as nxl
    import os.path
    import time
    now = str(int(time.time()))
    
    for key in nxl.descriptions.keys():
        if len(key) is 9:
            dbf = '/home/will/charts/gemfs/%s.s3db' %(key)
            if os.path.isfile(dbf):
                print "removing: " + dbf
                os.remove(dbf)
            if not os.path.isfile(dbf):
                print "creating: " + dbf
                createdb(dbf)
            print dbf.rstrip(".s3db")+".gemf"
            ds = DataStore(os.path.abspath(dbf))
            #date, initcenter, initzoom, name, description
            ds.addmain(now, 0, 0, key, nxl.descriptions[key])
            dir = "/home/will/charts/BSB_ROOT"
            filter = nxl.NoaaXmlParser(key).getKapFiles()
            bo = BsbOutlines(dir, filter)
            for key in bo.getkeys():
                #print key
                ds.addchart(key, bo.getname(key), bo.getupdated(key), bo.getscale(key), bo.getoutline(key), bo.getdepthunits(key), bo.getzooms(key))
            ds.Close()
