#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

'''

'''
ip_list = open('ip_list.txt','r')
for ip in ip_list
start_Time=int(time.time()) #记录开始时间
def ping_Test():
ips = open('host.txt','r')
ip_True = open('ip_True.txt','w')
ip_False = open('ip_False.txt','w')
count_True,count_False=0,0
for ip in ips.readlines():
    ip = ip.replace('\n','') #替换掉换行符
    return1=os.system('ping -n 2 -w 1 %s'%ip) #每个ip ping2次，等待时间为1s
if return1:
print 'ping %s is fail'%ip
ip_False.write(ip) #把ping不通的写到ip_False.txt中
count_False += 1
else:
print 'ping %s is ok'%ip
ip_True.write(ip) #把ping通的ip写到ip_True.txt中
count_True += 1
ip_True.close()
ip_False.close()
ips.close()
end_Time = int(time.time()) #记录结束时间
print "time(秒)：",end_Time - start_Time,"s" #打印并计算用的时间
print "ping通数：",count_True," ping不通的ip数：",count_False
ping_Test()
