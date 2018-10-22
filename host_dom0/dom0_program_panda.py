#!/usr/bin/env python3

from dom0_client import *
from dom0_sql import *
import sys
import time

session = Dom0_session('10.200.40.10', 3001)
name = str(sys.argv[1])
session.read_tasks(script_dir + name + '.xml')
session.send_descs()
session.send_bins()
session.start()
time.sleep(10)
session.live(script_dir + 'xml/' + name + '_log.xml')
session.stop()
time.sleep(1)
session.reboot()