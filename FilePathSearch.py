#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

class FilePathSearch():
    def __init__(self, directory, extention="KAP", filter=None):
        """Searches for files ending in <extention> in <directory> and all subdirectories
           Optionally supply list of file names <filter> to only search for files in filter list
           Returns list of string paths"""
        self.extention = extention
        self.filePaths = []
        self.fileList = []
        self.filter = filter
        if os.path.exists(directory):
            self.__listFiles(directory)
        else:
            print directory, "is not a directory."
        
    def __mywalker(self, arg, dir, file):
        if self.filter == None:
            for f in file:
                if f.upper().endswith(self.extention):
                    self.filePaths.append(dir+"/"+f)
                    self.fileList.append(f)
        else:
            for f in file:
                if f.endswith(self.extention) and ( self.filter.count(f) > 0 ):
                    self.filePaths.append(dir+"/"+f)
                    self.fileList.append(f)
        
    def __listFiles(self, dir):
        os.path.walk(dir, self.__mywalker, None)
        
    def getfilePaths(self):
        return self.filePaths

if __name__== "__main__":
    dir = "/home/will/charts/BSB_ROOT"
    filePathSearch = FilePathSearch(dir, 'KAP')
    for path in filePathSearch.getfilePaths():
        print path
