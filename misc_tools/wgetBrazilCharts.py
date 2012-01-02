#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, os.path, re

htmlFile = "/tmp/brazil.html"
url = "https://www.mar.mil.br/dhn/chm/cartas/download/cartasbsb/"
outDir = "/home/will/charts/BR_BSB_ROOT/zips"

if not os.path.isfile(htmlFile):
    print "retrieving html from mar.mil.br: "
    urllib.urlretrieve(url, "/tmp/brazil.html")
else:
    print "using html file in tmp"
    
fd = open(htmlFile)
str = fd.read()
urls = re.findall(r'href=[\'"]?([^\'" >]+)', str)
for url in urls:
    if url.endswith(".zip"):
        zipPath = outDir + "/" + url.split('/')[-1]
        if not os.path.isfile(zipPath):
            print "retrieving: "+url
            urllib.urlretrieve(url, zipPath)
fd.close()