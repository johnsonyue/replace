from worker import multi_thread
import time
import random

def task(argv):
	sleep_time = random.randint(1,5)
	for arg in argv:
		print str(arg)+" ",
	print "sleep "+str(sleep_time)
	time.sleep(sleep_time)
		
	result = False
	if (random.randint(1,100) % 2):
		result = True

	for arg in argv:
		print str(arg)+" ",
	print str(result)
	
	return result

argv_list = [(1,1,1), (2,2,2), (3,3,3), (4,4,4)]
multi_thread.run_with_multi_thread(task,argv_list,2)
