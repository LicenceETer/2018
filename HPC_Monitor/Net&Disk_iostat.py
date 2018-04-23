#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rrdtool
import time

title = "HPC Network&Disk Status ("+time.strftime('%Y-%m-%d',time.localtime(time.time()))+")"

rrdtool.graph("/python/HPC_Monitor/N&D_Status.png","--start","-1d","--vertical-label=Usage","--x-grid",
            "MINUTE:12:HOUR:1:HOUR:1:0:%H",
            "--width","1500","--height","600","--title",title,
            "DEF:netin=HPC.rrd:eth0_in:AVERAGE",
            "DEF:netout=HPC.rrd:eth0_out:AVERAGE",
            "DEF:diskin=HPC.rrd:disk_read:AVERAGE",
            "DEF:diskout=HPC.rrd:disk_write:AVERAGE",
            "CDEF:disktotal=diskin,diskout,+",
            "CDEF:nettotal=netin,netout,+",
    #        "CDEF:cpu=c,100,*",
    #        "CDEF:mem=m,100,*",
    #        "CDEF:disk=d,100,*",
            "COMMENT:\\r",
    #        "COMMENT:\\r",
            "AREA:netout#00FF00:NET_OUT",
            "LINE1:netin#FF8833:NET_IN",
            "LINE1:diskin#0000FF:DISK_READ",
            "LINE1:diskout#FF0000:DISK_WRITE\\r",
            "COMMENT:\\r",
            "GPRINT:netin:MAX:MAX_NET_IN\: %2.2lf %Sbps",
            "GPRINT:netout:MAX:MAX_NET_OUT\: %2.2lf %Sbps\\r",
            "GPRINT:diskin:MAX:MAX_DISK_READ\: %2.2lf %Sb/s",
            "GPRINT:diskout:MAX:MAX_DISK_WRITE\: %2.2lf %Sb/s\\r",
            "GPRINT:disktotal:AVERAGE:AVERAGE_DISK_IO\: %2.2lf %Sb/s\\r",)
