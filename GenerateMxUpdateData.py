import os, time
import Env

#dir = "/home/will/charts/gemfs_version2"
sqlf = open(Env.gemfDir+"/UPDATE.sql", "w")
dir = Env.gemfDir+"live-online/NOAA"
os.chdir(dir)
lst = os.listdir(dir)
lst.sort()

sqlstr = "update regions set latestdate='%s', size='%s' where name='%s';"
epoch = "1349761592"
#epoch = int(time.time())
sqlf.write("mx.mariner.update\n")

for p in lst:
    if p.endswith(".gemf"):
        size = str(os.path.getsize(p))
        region = p.rstrip(".gemf")
        sqlf.write(sqlstr %(epoch, size, region)+"\n")
print "update writen to: " + Env.gemfDir+'/UPDATE.sql'
