import os
import threading

for i in range(5):
	os.system("nohup bash -c 'sleep 10; echo hello' >"+str(i)+" 2>/dev/null &")

print "finished"
