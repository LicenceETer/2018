#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import time
class cpu:
    usage = psutil.cpu_percent(1)

class mem:
    m = psutil.virtual_memory()
    total = float(m.total)
    free = m.free
    used = float(m.used)
    usage = float(used/total)*100.0

class disk:
    d = psutil.disk_partitions()
    usage = psutil.disk_usage('/')
    read = psutil.disk_io_counters()[2]
    write = psutil.disk_io_counters()[4]
    test = psutil.disk_io_counters()

class network:
    input = psutil.net_io_counters()[1]
    output = psutil.net_io_counters()[0]
    total = input + output

time.sleep(1)

print('The cpu usage is : '),
print(cpu.usage)
print('The mem usage is : '),
print(mem.usage)
print('The disk usage is : '),
print(disk.usage)
print('The net network count in is : '),
print(network.input)
print('The disk read is : '),
print(disk.read),
print(' the write is :'),
print(disk.write)
print(disk.test.read_bytes)
