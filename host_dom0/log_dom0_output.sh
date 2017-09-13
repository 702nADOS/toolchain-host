#!/bin/bash

echo "" > dom0_output.log 
date
sudo cat /dev/ttyUSB0 >> dom0_output.log
