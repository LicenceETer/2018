#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Monitor
import sys
import time
import warn

argv = sys.argv[1]

def cpu(argv):
    if Monitor.'argv'.usage >= 60 :
        text = u'WARNING! CPU占用高!'
        warn.send(text)
    pass

def mem(argv):
    if Monitor.'argv'.usage >= 60 :
        text = u'WARNING! 内存占用高!'
        warn.send(text)
    pass

if argv == 'cpu':
    cpu(argv)

if asgv == 'mem':
    mem(argv)
