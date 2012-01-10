#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 by Will Kamp <manimaul!gmail.com>
# This will find the appropriate zxy tiled map optimal zoom level for a BSB chart
# Accounts for latitude distortion of scales

import math
from shapely.geometry import Point
from pyproj import Proj
from BsbHeader import BsbHeader

zoomOverrides = {"NZ14065.kap" : 6, "18431_1.KAP" : 15}

#"43082.kap" : 12, "43083.kap" : 12, "43084.kap" : 12, "43100.kap" : 10, "43101.kap" : 12, "43102.kap" : 12, 
#"43104.kap" : 12, "43105.kap" : 12, "43106.kap" : 12, "43122.kap" : 12, "43123.kap" : 12, "43124.kap" : 12, 
#"43126.kap" : 12, "43141.kap" : 12, "43142.kap" : 12, "43143.kap" : 12, "43144.kap" : 11, "43145.kap" : 12, 
#"43164.kap" : 12, "43167.kap" : 12, 

def haversinedistance(origin, destination):
    lon1, lat1 = origin
    lon2, lat2 = destination
    radius = 6371 #kilometers
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d * 1000 #meters

def cartesiandistance(origin, destination):
    lon1, lat1 = origin
    lon2, lat2 = destination
    proj = Proj(init="epsg:3785") # spherical mercator, should work anywhere
    point1 = proj(lon1, lat1)
    point2 = proj(lon2, lat2)
    point1_cart = Point(point1)
    point2_cart = Point(point2)
    return point1_cart.distance(point2_cart) #meters

def latitudedistortion(latitude):
    origin = (0, latitude)
    destination = (1, latitude)
    hdist = haversinedistance(origin, destination)
    cdist = cartesiandistance(origin, destination)
    return cdist/hdist

def getZoom(scale, latitude):
    tweakPercent = .87
    scale = scale * latitudedistortion(latitude) * tweakPercent
    t = 30;
    while scale > 1:
        scale = scale / 2;
        t -= 1;
    return t

def getKapZoom(kapfile):
    key = kapfile.split("/")[-1]
    if zoomOverrides.has_key(key):
        return zoomOverrides[key]
    else:
        header = BsbHeader(kapfile)
        scale = header.getscale()
        latitude = header.getCenter()[1]
        return getZoom(scale, latitude)

if __name__== "__main__":
    print getKapZoom("/home/will/zxyCharts/BSB_ROOT/NGA_BSB_ROOT/29323.kap")
