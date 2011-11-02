import os

dir = "/home/will/charts/gemfs/BY_REGION"
sqlf = open(dir+"/UPDATE.sql", "w")
os.chdir(dir)
lst = os.listdir(dir)
lst.sort()

sqlstr = "update regions set latestdate='%s', size='%s' where name='%s';"
epoch = "1319485045"


for p in lst:
    if p.endswith(".gemf"):
        size = str(os.path.getsize(p))
        region = p.rstrip(".gemf")
        sqlf.write(sqlstr %(epoch, size, region)+"\n")
print "update writen to: " + dir+'/UPDATE.sql'