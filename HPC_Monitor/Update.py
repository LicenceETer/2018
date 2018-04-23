#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rrdtool
import time
import Monitor

cpu_usage = Monitor.cpu.usage
mem_usage = Monitor.mem.usage
disk_usage = Monitor.disk.usage.percent
eth0_in = Monitor.network.input
eth0_out = Monitor.network.output
disk_read = Monitor.disk.read
disk_write = Monitor.disk.write

starttime = int(time.time())

"""
##The order in the rrd is
    cpu_usage->men_usage->eth0_in->eth0_out->disk_usage
  please insert in order
##
"""
update = rrdtool.updatev('/python/HPC_Monitor/HPC.rrd','%s:%s:%s:%s:%s:%s:%s:%s' % (starttime,cpu_usage,mem_usage,eth0_in,eth0_out,disk_usage,disk_read,disk_write))

if not update:
    raise error
    print('update ERROR')
print(update)
