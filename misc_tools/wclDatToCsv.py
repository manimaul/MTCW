wcl = open("/home/will/Desktop/wcl.dat", "r")
lines = wcl.readlines()
print len(lines)
wclout = open("/home/will/workspace/MX-Mariner/assets/wclsm.csv", "w")
continents = []

num = 0
section = []
for line in lines:
    if not line.startswith(">"):
        latlong = line.rstrip("\n").split("\t")
        lat = int( float(latlong[0])*1E6 )
        lon = int (float(latlong[1])*1E6 )
        section.append((lat,lon))
        #wclout.write(str(lat)+","+str(lon)+"\n")
        num += 1;
    else:
        #wclout.write(">\n")
        continents.append(section)
        section = []

for ea in continents:
    if len(ea) > 0:
        wclout.write(str(ea[0][0])+","+str(ea[0][1])+"\n")
        wclout.write(str(ea[-1][0])+","+str(ea[-1][1])+"\n")
        wclout.write(">\n")
#    for ll in section:
#        wclout.write(str(ll[0])+","+str(ll[1])+"\n")
#    wclout.write(">\n")


