#!/usr/bin/env python
# -*- coding: utf-8 -*-

import md5
import sys
import os.path

def sumfile(fobj):
    '''Returns an md5 hash for an object with read() method.'''
    m = md5.new()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()


def md5sum(fname):
    '''Returns an md5 hash for file fname, or stdin if fname is "-".'''
    if fname == '-':
        ret = sumfile(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            return 'Failed to open file'
        ret = sumfile(f)
        f.close()
    return ret

def getFilesum(path):
    if os.path.isfile(path):
        return '%32s' % (md5sum(path))


# if invoked on command line, print md5 hashes of specified files.
if __name__ == '__main__':
    pass #TODO:
    

    
