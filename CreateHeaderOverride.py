import os, Env, BsbHeader, codecs

def makeHeader(kapPath):
    plyinjection = False
    print "creating new header override for %s" %(os.path.basename(kapPath))
    overridePath = Env.mtcwDir+"header_overrides/NOAA/"+os.path.basename(kapPath)[0:-4]
    if os.path.isfile(kapPath) and os.path.isfile(overridePath):
        override = open(overridePath, "r")
        newFile = codecs.open(kapPath+"_header.txt", "w", "utf-8")
        plyLines = override.readlines()
        header = BsbHeader.BsbHeader(kapPath)
        for line in header.getlines():
            if line.startswith("PLY"):
                if not plyinjection:
                    plyinjection = True;
                    for ea in plyLines:
                        newFile.write(ea)
            else:
                newFile.write(line)
        override.close()
        newFile.close()
    return kapPath+"_header.txt"
    
if __name__ == "__main__":
    print makeHeader("/mnt/auxdrive/zxyCharts/BSB_ROOT/NOAA_BSB_ROOT/11412/11412_1.KAP")