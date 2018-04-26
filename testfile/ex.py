#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Monitor
import sys
import time

argv = sys.argv[1]

def cpu(argv):
    text = u'WARNING! CPU占用高!'
    print(text+argv)
    pass

def mem(argv):
    text = u'WARNING! 内存占用高!'
    print(text+argv)
    pass

if argv == 'cpu':
    cpu(argv)

if argv == 'mem':
    mem(argv)
