#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Created 2011 by Will Kamp <manimaul!gmail.com>
#Do whatever want with this / Simplified BSD Licenced

import urllib, os, re, glob

home = os.getenv("HOME")
url = "http://www.charts.noaa.gov/NGAViewer/"
cacheRoot = home+"/NGA/htmlCache/"
zoom = "6"

def haveChartImage(chart):
    if os.path.isfile(cacheRoot+chart.rstrip("/")+".png"):
        return True
    return False
    
def havePdf(pdf):
    if os.path.isfile(cacheRoot+pdf):
        return True
    return False
    
def isPdf(url):
    if url.endswith(".pdf"):
        return True
    return False

def isChartDir(url):
    if url.endswith("/") and not url.startswith("/"):
        return True
    return False
    
def getUrlsInHtml(htmlFile):
    fd = open(htmlFile)
    str = fd.read()
    fd.close()
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', str)
    return urls

def getZoomifyTiles(chart = "11"):
    url = "http://www.charts.noaa.gov/NGAViewer/%s/" %(chart)
    
    if not os.path.isdir(cacheRoot+chart):
        os.mkdir(cacheRoot+chart)
    
    htmlFile = cacheRoot+chart+"/"+chart+".html"
    if not os.path.isfile(htmlFile):
        urllib.urlretrieve(url, htmlFile)
        
    baseChartDirs = getUrlsInHtml(htmlFile)
    for ea in baseChartDirs:
        if isChartDir(ea):
            #print url+ea
            htmlFile = cacheRoot+chart+"/"+ea.rstrip("/")+".html"
            #print htmlFile + "\n"
            if not os.path.isfile(htmlFile):
                #print "retrieving: "+url+ea
                urllib.urlretrieve(url+ea, htmlFile)
            baseTileDirs = getUrlsInHtml(htmlFile)
            for jpg in baseTileDirs:
                if jpg.startswith(zoom):
                    jpgFile = cacheRoot+chart+"/"+jpg
                    if not os.path.isfile(jpgFile):
                        #print "retrieving: "+url+ea+jpg
                        urllib.urlretrieve(url+ea+jpg, jpgFile)

def makeChart(chart = "11"):
    os.chdir(cacheRoot+chart)
    rows = []
    columns = []
    for infile in glob.glob(cacheRoot+chart+"/*.jpg"):
        #print infile
        dex = infile.rstrip(".jpg").split("-")
        #print dex
        row = int(dex[1])
        column = int(dex[2])
        #print row, column
        if rows.count(row) == 0:
            rows.append(row)
        if columns.count(column) == 0:
            columns.append(column)
    rows.sort()
    columns.sort()
    for row in rows:
        cmd = "convert "
        for column in columns:
            jpg = zoom+"-"+str(row)+"-"+str(column)+".jpg "
            cmd += jpg
        cmd += "-append "+str(row)+".png"
        print "compiling chart column "+str(row)+" of "+str(len(rows))
        os.system(cmd)
    cmd = "convert "
    for row in rows:
        png = str(row)+".png "
        cmd += png
    print "compiling final chart #"+chart+"..."
    os.system(cmd + "+append ../"+chart+".png")
    print "done :)"

if __name__=="__main__":
    htmlFile = cacheRoot+"/ngaRasterRoot.html"
    
    if not os.path.isfile(htmlFile):
        print "retrieving html from charts.noaa.gov/NGAView/: "
        urllib.urlretrieve(url, htmlFile)
        
    links = getUrlsInHtml(htmlFile)
    
    for link in links:
        #print "grabbing pdfs"
        if isPdf(link) and not havePdf(link):
            print "downloading " + url+link + "..."
            urllib.urlretrieve(url+link, cacheRoot+link)
        #print link
        #print "grabbing zoomify tiles"
        if isChartDir(link) and not haveChartImage(link):
            chart = link.rstrip("/")
            print "downloading " + chart + "..."
            getZoomifyTiles(chart)
            makeChart(chart)
    
