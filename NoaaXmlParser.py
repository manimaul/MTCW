#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import os
from xml.dom import minidom

xmlUrls = {"BSB_ALL" : "http://www.charts.noaa.gov/RNCs/RNCProdCat_19115.xml", \
           "DISTRICT_01" : "http://www.charts.noaa.gov/RNCs/01CGD_RNCProdCat_19115.xml", \
           "DISTRICT_05" : "http://www.charts.noaa.gov/RNCs/05CGD_RNCProdCat_19115.xml", \
           "DISTRICT_07" : "http://www.charts.noaa.gov/RNCs/07CGD_RNCProdCat_19115.xml", \
           "DISTRICT_08" : "http://www.charts.noaa.gov/RNCs/08CGD_RNCProdCat_19115.xml", \
           "DISTRICT_09" : "http://www.charts.noaa.gov/RNCs/09CGD_RNCProdCat_19115.xml", \
           "DISTRICT_11" : "http://www.charts.noaa.gov/RNCs/11CGD_RNCProdCat_19115.xml", \
           "DISTRICT_13" : "http://www.charts.noaa.gov/RNCs/13CGD_RNCProdCat_19115.xml", \
           "DISTRICT_14" : "http://www.charts.noaa.gov/RNCs/14CGD_RNCProdCat_19115.xml", \
           "DISTRICT_17" : "http://www.charts.noaa.gov/RNCs/17CGD_RNCProdCat_19115.xml", \
           "REGION_02" : "http://www.charts.noaa.gov/RNCs/02Region_RNCProdCat_19115.xml", \
           "REGION_03" : "http://www.charts.noaa.gov/RNCs/03Region_RNCProdCat_19115.xml", \
           "REGION_04" : "http://www.charts.noaa.gov/RNCs/04Region_RNCProdCat_19115.xml", \
           "REGION_06" : "http://www.charts.noaa.gov/RNCs/06Region_RNCProdCat_19115.xml", \
           "REGION_07" : "http://www.charts.noaa.gov/RNCs/07Region_RNCProdCat_19115.xml", \
           "REGION_08" : "http://www.charts.noaa.gov/RNCs/08Region_RNCProdCat_19115.xml", \
           "REGION_10" : "http://www.charts.noaa.gov/RNCs/10Region_RNCProdCat_19115.xml", \
           "REGION_12" : "http://www.charts.noaa.gov/RNCs/12Region_RNCProdCat_19115.xml", \
           "REGION_13" : "http://www.charts.noaa.gov/RNCs/13Region_RNCProdCat_19115.xml", \
           "REGION_14" : "http://www.charts.noaa.gov/RNCs/14Region_RNCProdCat_19115.xml", \
           "REGION_15" : "http://www.charts.noaa.gov/RNCs/15Region_RNCProdCat_19115.xml", \
           "REGION_17" : "http://www.charts.noaa.gov/RNCs/17Region_RNCProdCat_19115.xml", \
           "REGION_22" : "http://www.charts.noaa.gov/RNCs/22Region_RNCProdCat_19115.xml", \
           "REGION_24" : "http://www.charts.noaa.gov/RNCs/24Region_RNCProdCat_19115.xml", \
           "REGION_26" : "http://www.charts.noaa.gov/RNCs/26Region_RNCProdCat_19115.xml", \
           "REGION_30" : "http://www.charts.noaa.gov/RNCs/30Region_RNCProdCat_19115.xml", \
           "REGION_32" : "http://www.charts.noaa.gov/RNCs/32Region_RNCProdCat_19115.xml", \
           "REGION_34" : "http://www.charts.noaa.gov/RNCs/34Region_RNCProdCat_19115.xml", \
           "REGION_36" : "http://www.charts.noaa.gov/RNCs/36Region_RNCProdCat_19115.xml", \
           "REGION_40" : "http://www.charts.noaa.gov/RNCs/40Region_RNCProdCat_19115.xml", \
           "AK_N" : "http://www.charts.noaa.gov/RNCs/36Region_RNCProdCat_19115.xml", \
           "AK_S" : "http://www.charts.noaa.gov/RNCs/34Region_RNCProdCat_19115.xml", \
           "CT" : "http://www.charts.noaa.gov/RNCs/CT_RNCProdCat_19115.xml", \
           "GA" : "http://www.charts.noaa.gov/RNCs/GA_RNCProdCat_19115.xml", \
           "IL" : "http://www.charts.noaa.gov/RNCs/IL_RNCProdCat_19115.xml", \
           "MA" : "http://www.charts.noaa.gov/RNCs/MA_RNCProdCat_19115.xml", \
           "MI" : "http://www.charts.noaa.gov/RNCs/MI_RNCProdCat_19115.xml", \
           "NC" : "http://www.charts.noaa.gov/RNCs/NC_RNCProdCat_19115.xml", \
           "NV" : "http://www.charts.noaa.gov/RNCs/NV_RNCProdCat_19115.xml", \
           "OR" : "http://www.charts.noaa.gov/RNCs/OR_RNCProdCat_19115.xml", \
           "PR" : "http://www.charts.noaa.gov/RNCs/PR_RNCProdCat_19115.xml", \
           "TX" : "http://www.charts.noaa.gov/RNCs/TX_RNCProdCat_19115.xml", \
           "WA" : "http://www.charts.noaa.gov/RNCs/WA_RNCProdCat_19115.xml", \
           "AL" : "http://www.charts.noaa.gov/RNCs/AL_RNCProdCat_19115.xml", \
           "DE" : "http://www.charts.noaa.gov/RNCs/DE_RNCProdCat_19115.xml", \
           "HI" : "http://www.charts.noaa.gov/RNCs/HI_RNCProdCat_19115.xml", \
           "IN" : "http://www.charts.noaa.gov/RNCs/IN_RNCProdCat_19115.xml", \
           "MD" : "http://www.charts.noaa.gov/RNCs/MD_RNCProdCat_19115.xml", \
           "MN" : "http://www.charts.noaa.gov/RNCs/MN_RNCProdCat_19115.xml", \
           "NH" : "http://www.charts.noaa.gov/RNCs/NH_RNCProdCat_19115.xml", \
           "NY" : "http://www.charts.noaa.gov/RNCs/NY_RNCProdCat_19115.xml", \
           "PA" : "http://www.charts.noaa.gov/RNCs/PA_RNCProdCat_19115.xml", \
           "RI" : "http://www.charts.noaa.gov/RNCs/RI_RNCProdCat_19115.xml", \
           "VA" : "http://www.charts.noaa.gov/RNCs/VA_RNCProdCat_19115.xml", \
           "WI" : "http://www.charts.noaa.gov/RNCs/WI_RNCProdCat_19115.xml", \
           "CA" : "http://www.charts.noaa.gov/RNCs/CA_RNCProdCat_19115.xml", \
           "FL" : "http://www.charts.noaa.gov/RNCs/FL_RNCProdCat_19115.xml", \
           "ID" : "http://www.charts.noaa.gov/RNCs/ID_RNCProdCat_19115.xml", \
           "LA" : "http://www.charts.noaa.gov/RNCs/LA_RNCProdCat_19115.xml", \
           "ME" : "http://www.charts.noaa.gov/RNCs/ME_RNCProdCat_19115.xml", \
           "MS" : "http://www.charts.noaa.gov/RNCs/MS_RNCProdCat_19115.xml", \
           "NJ" : "http://www.charts.noaa.gov/RNCs/NJ_RNCProdCat_19115.xml", \
           "OH" : "http://www.charts.noaa.gov/RNCs/OH_RNCProdCat_19115.xml", \
           "PO" : "http://www.charts.noaa.gov/RNCs/PO_RNCProdCat_19115.xml", \
           "SC" : "http://www.charts.noaa.gov/RNCs/SC_RNCProdCat_19115.xml", \
           "VT" : "http://www.charts.noaa.gov/RNCs/VT_RNCProdCat_19115.xml", \
           }

descriptions = {"BSB_ALL" : "Entire NOAA raster chart catalog", \
                "DISTRICT_01" : "US East: New Jersey to Maine", \
                "DISTRICT_05" : "US East: N. Carolina to Delaware", \
                "DISTRICT_07" : "US East: Florida to S. Carolina", \
                "DISTRICT_08" : "US East: New Mexico to Florida pan handle", \
                "DISTRICT_09" : "US North East: Great Lakes, Minnesota to New York", \
                "DISTRICT_11" : "US West: Arizona to California", \
                "DISTRICT_13" : "US West: Oregon to Washington State", \
                "DISTRICT_14" : "US West: Pacific Ocean - Hawaii", \
                "DISTRICT_17" : "US West: Pacific Ocean - Alaska", \
                "REGION_02" : "Block Island RI to the Canadian Border", \
                "REGION_03" : "New York to Nantucket and Cape May NJ", \
                "REGION_04" : "Chesapeake and Delaware Bays", \
                "REGION_06" : "Norfolk VA to Florida including the ICW", \
                "REGION_07" : "Florida East Coast and the Keys", \
                "REGION_08" : "Florida West Coast and the Keys", \
                "REGION_10" : "Puerto Rico and the U.S. Virgin Islands", \
                "REGION_12" : "Southern California: Point Arena to the Mexican Border", \
                "REGION_13" : "Lake Michigan", \
                "REGION_14" : "San Francisco to Cape Flattery", \
                "REGION_15" : "Pacific Northwest: Puget Sound to the Canadian Border", \
                "REGION_17" : "Mobile AL to the Mexican Border", \
                "REGION_22" : "Lake Superior and Lake Huron (U.S. Waters)", \
                "REGION_24" : "Lake Erie (U.S. Waters)", \
                "REGION_26" : "Lake Ontario (U.S. Waters)", \
                "REGION_30" : "Southeast Alaska", \
                "REGION_32" : "South Central Alaska: Yakutat to Kodiak", \
                "REGION_34" : "Alaska: The Aleutians and Bristol Bay", \
                "REGION_36" : "Alaska: Norton Sound to Beaufort Sea", \
                "REGION_40" : "Hawaiian Islands and U.S. Territories", \
                "AK_N" : "Alaska North", \
                "AK_S" : "Alaska South", \
                "CT" : "Connecticut", \
                "GA" : "Georgia", \
                "IL" : "Illinois", \
                "MA" : "Massachusetts", \
                "MI" : "Michigan", \
                "NC" : "North Carolina", \
                "NV" : "Nevada", \
                "OR" : "Oregon", \
                "PR" : "Puerto Rico US Virgin Is.", \
                "TX" : "Texas", \
                "WA" : "Washington State", \
                "AL" : "Alabama", \
                "DE" : "Delaware", \
                "HI" : "Hawaii", \
                "IN" : "Indiana", \
                "MD" : "Maryland", \
                "MN" : "Minnesota", \
                "NH" : "New Hampshire", \
                "NY" : "New York", \
                "PA" : "Pennsylvania", \
                "RI" : "Rhode Island", \
                "VA" : "Virginia", \
                "WI" : "Wisconsin", \
                "CA" : "Califonia", \
                "FL" : "Florida", \
                "ID" : "Indiana", \
                "LA" : "Louisiana", \
                "ME" : "Maine", \
                "MS" : "Mississippi", \
                "NJ" : "New Jersey", \
                "OH" : "Ohio", \
                "PO" : "Pacific Ocean", \
                "SC" : "South Carolina", \
                "VT" : "Vermont", \
                }

class NoaaXmlParser():
    def __init__(self, xmlUrlKey="BSB_ALL", xmlDir="/home/will/charts/NOAAxml/"):

        
        #chartCovers are not charts and should be skipped
        self.chartCovers = ['12352_8.KAP', '12364_24.KAP', '12372_19.KAP', '13221_2.KAP', '13229_15.KAP', \
                            '14786_79.KAP', '14786_80.KAP', '14786_81.KAP', '14786_82.KAP', '14786_83.KAP', \
                            '14786_84.KAP', '14786_85.KAP', '14786_86.KAP', '14786_87.KAP', '14786_88.KAP', \
                            '14842_45.KAP', '14842_46.KAP', '14842_47.KAP', '14842_48.KAP', '14842_49.KAP', \
                            '14842_50.KAP', '14842_51.KAP', '14846_39.KAP', '14846_40.KAP', '14846_41.KAP', \
                            '14846_42.KAP', '14846_43.KAP', '14846_44.KAP', '14853_48.KAP', '14853_49.KAP', \
                            '14853_50.KAP', '14853_51.KAP', '14853_52.KAP', '14853_53.KAP', '14853_54.KAP', \
                            '14886_15.KAP', '14886_16.KAP', '14886_17.KAP', '14886_18.KAP', '14886_19.KAP', \
                            '14916_37.KAP', '14916_38.KAP', '14916_39.KAP', '14916_40.KAP', '14916_41.KAP', \
                            '14916_42.KAP', '14916_43.KAP', '14926_33.KAP', '14926_34.KAP', '14926_35.KAP', \
                            '14926_36.KAP', '14926_37.KAP', '11324_2.KAP', '18423_19.KAP', '18445_17.KAP', \
                            '18652_20.KAP', '12285_19.KAP', '12285_18.KAP', '12205_13.KAP', '11451_16.KAP', \
                            '11451_17.KAP', '11326_7.KAP']
        #need to find a way to fix these
        self.problemCharts = ['12206_6.KAP', '5161_1.KAP']
        
        self.wrongZoomCharts = ["11467_1.zxy", "12285_15.zxy", "11541_5.zxy", "11534_5.zxy", "11534_1.zxy", "12324_5.zxy", \
                                "11541_3.zxy", "11507_1.zxy", "12316_4.zxy", "18445_14.zxy", "11467_6.zxy", "12324_1.zxy", \
                                "18553_3.zxy", "11534_6.zxy", "11553_1.zxy", "11507_3.zxy"]
        
        xmlUrl = xmlUrls[xmlUrlKey]
        self.regionName = xmlUrl.split("/")[-1]
        
        if os.path.isfile(xmlDir + self.regionName):
            self.xmlFile = file(xmlDir + self.regionName)
        else:
            print "retrieving xml from NOAA: " + self.regionName
            urllib.urlretrieve(xmlUrl, xmlDir + self.regionName)
            self.xmlFile = file(xmlDir + self.regionName)
        
    def getKapFiles(self):
        kaplst = []
        dom = minidom.parse(self.xmlFile)
        for node in dom.getElementsByTagName("EX_Extent"):
            for nnode in node.getElementsByTagName("gco:CharacterString"):
                str = nnode.toxml()
                kap = str[str.find("file name: ")+11:str.find(".KAP")+4]
                if not (self.chartCovers.__contains__(kap) or self.problemCharts.__contains__(kap)):
                    kaplst.append(kap)
        return kaplst

if __name__ == "__main__":
    str = """#####################
echo "merging region %s"
python BatchMerge.py %s 

echo "optimizing region %s"
python tiles_opt.py /home/will/charts/%s 

echo "creating gemf region %s"
python AutoGemf.py %s 
    """
    keys = descriptions.keys()
    keys.sort()
    for key in keys:
        if len(key) == 9:
            print str %(key, key, key, key, key, key)
    #print NoaaXmlParser("NV").getKapFiles()

