#!/usr/bin/env python3

from dom0_client import *
from dom0_sql import *
import sys
import time

current=int(round(time.time()*1000))
session = Dom0_session('10.200.40.11', 3001)
name = str(sys.argv[1])
new_time=int(round(time.time()*1000))
print('connect '+str(new_time-current))
current=new_time
session.read_tasks(script_dir + name + '.xml')
new_time=int(round(time.time()*1000))
print('read_desc '+str(new_time-current))
current=new_time
first_send=current
session.send_descs()
new_time=int(round(time.time()*1000))
print('send_desc '+str(new_time-current))
current=new_time
session.send_bins()
new_time=int(round(time.time()*1000))
print('send_bins '+str(new_time-current))
current=new_time
session.start()
new_time=int(round(time.time()*1000))
print('start '+str(new_time-current))
current=new_time
i=0
while 1:
	session.receive(script_dir + 'xml/' + str(i) + '_log.xml')
	i=i+1
	new_time=int(round(time.time()*1000))
	print('time_since_desc_send '+str(i)+' '+str(new_time-first_send))
	print('push_profile'+str(i)+' '+str(new_time-current))
	current=new_time

