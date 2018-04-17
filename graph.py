#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  rrdtool
import time

title = "Server Network traffic flow ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"

rrdtool.graph("Flow.png",)
