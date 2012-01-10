#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Env
import os

manifest = open(Env.ngaRegionDir+"MANIFEST", "r")

descs = []
files = []
for line in manifest.readlines():
    if not line.startswith("#"):
        try:
            region = line.split(",")
            descs.append((region[0].strip(), region[1].strip()))
            files.append((region[0].strip(), region[3].strip()))
        except:
            pass
        
ngaDescs = dict(descs)
ngaFiles = dict(files)

def getDescriptions():
    return ngaDescs
        
def getFiles():
    return ngaFiles

if __name__== "__main__":
    print getDescriptions()