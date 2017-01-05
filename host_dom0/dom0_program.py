#!/usr/bin/env python3

from dom0_client import *
from dom0_sql import *
import time

session = Dom0_session('192.168.217.21', 3001)


print('Waiting for 10 seconds...')
i=0
while i<100:
	session.live()
	time.sleep(0.1)
	i=i+1

session.read_tasks(script_dir + 'tasks.xml')
session.send_descs()
session.send_bins()
session.start()


while i<200:
	session.live()
	time.sleep(0.1)
	i=i+1
session.stop()


while i<300:
	session.live()
	time.sleep(0.1)
	i=i+1



session.profile(script_dir + 'log.xml')
xml2sql(script_dir + 'log.xml', script_dir + 'dom0.db')

help()
code.interact(local=locals())
