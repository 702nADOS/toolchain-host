from dom0_client import *
#from dom0_sql import *
import time
import sys
import signal
import os

#Catch STRG+C -> Clear all running tasks and close the connection
def kill_sig(signal, frame):
	session.clear()
	session.close()
	print("Killed dom0 client")
	sys.exit(0)

#check input argument
if len(sys.argv)<2:
	print("You need to specify a task.xml file")
	sys.exit(1)
elif len(sys.argv)>2:
	print("Only one task.xml file allowed")
	sys.exit(1)
elif not(os.path.isfile(sys.argv[1])):
	print("Cannot reach task.xml")
	sys.exit(1) 

print("Using xml file "+ sys.argv[1])

try:
	session = Dom0_session('192.168.217.21', 3001)
	session.read_tasks(script_dir + sys.argv[1])
	session.send_descs()
	session.send_bins()
	session.start()

	#Used to catch the kill signal
	signal.signal(signal.SIGINT, kill_sig)

	print("Init done waiting 2 seconds to go...")

	time.sleep(2)
	print("")
	print("Write logfile")
	
	session.profile("log_profile.xml");
	#session.live("log_live.xml");
	print("Done! Parse logfile to DB")

	#xml2sql(script_dir + 'log.xml', script_dir + 'dom0.db')

	#while True:
		#-> get xml log and see if task is still running?!?
		#-> yes -> break
		#-> no -> continue

	#Execution loop
	#while True:
	#	session.live()
	#	#xml2sql(script_dir + sys.argv[1], script_dir + 'dom0.db')
	#	time.sleep(1)

except:
	print("ERROR!") 
	session.clear()
	session.close()               
	raise
