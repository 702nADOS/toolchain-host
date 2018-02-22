#!/usr/bin/env python3

from dom0_client import *
from dom0_sql import *
import sys
import time

session = Dom0_session('10.200.40.11', 3001)
session.reboot()
