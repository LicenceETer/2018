#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rrdtool
import time

title = "HPC Status ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"

rrdtool.graph("/python/HPC_Monitor/HPC_Status.png","--start","-1d","--vertical-label=Usage","--x-grid",
            "MINUTE:12:HOUR:1:HOUR:1:0:%H",
            "--width","1600","--height","700","--title",title,
            "DEF:cpu=HPC.rrd:cpu_usage:AVERAGE",
            "DEF:mem=HPC.rrd:mem_usage:AVERAGE",
            "DEF:disk=HPC.rrd:disk_usage:AVERAGE",
    #        "CDEF:cpu=c,100,*",
    #        "CDEF:mem=m,100,*",
    #        "CDEF:disk=d,100,*",
            "COMMENT:\\r",
    #        "COMMENT:\\r",
            "AREA:mem#00FF00:MEM_USAGE",
            "LINE1:disk#0000FF:DISK_USAGE",
            "LINE1:cpu#FF8833:CPU_USAGE",
            "HRULE:50#FF0000:ALARM_VALUE\\r",
            "COMMENT:\\r",
            "GPRINT:cpu:MAX:MAX_CPU_USAGE\: %2.2lf %S%%",
            "GPRINT:cpu:AVERAGE:AVERAGE_CPU_USAGE\: %2.2lf %S%%\\r",
            "GPRINT:mem:MAX:MAX_MEM_USAGE\: %2.2lf %S%%",
            "GPRINT:mem:AVERAGE:AVERAGE_MEM_USAGE\: %2.2lf %S%%\\r",
            "GPRINT:disk:AVERAGE:DISK_USAGE\: %2.2lf %S%%\\r",)
