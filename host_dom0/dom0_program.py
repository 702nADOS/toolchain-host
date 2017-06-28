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
	print("You need to specify the path to task*.xml file")
	sys.exit(1)
elif len(sys.argv)>2:
	print("Only one path is allowed")
	sys.exit(1)


try:
	session = Dom0_session('192.168.217.21', 3001)
	input_file_pattern = sys.argv[1]
	
	#Used to catch the kill signal
	signal.signal(signal.SIGINT, kill_sig)	
	
	counter=0
	if os.path.isfile(input_file_pattern+str(counter)+".xml"):
		session.read_tasks(input_file_pattern+str(counter)+".xml")
		session.send_descs()
		session.send_bins()
		session.start()
		time.sleep(1)
		print("Write logfile")
		session.live(input_file_pattern+str(counter)+"_output.xml");
		session.clear()
		counter+=1
	else:
		raise Exception("Cannot load taskfile")
		
	#generate tubles of input and output files
	while (os.path.isfile(input_file_pattern+str(counter)+".xml")):
		session.read_tasks(input_file_pattern+str(counter)+".xml")
		session.send_descs()
		session.start()
		time.sleep(1)
		
		
		print("Write logfile")
		session.live(input_file_pattern+str(counter)+"_output.xml");
		session.clear()
		counter+=1
	
	
	
	


except:
	print("ERROR!") 
	session.clear()
	session.close()               
	raise
