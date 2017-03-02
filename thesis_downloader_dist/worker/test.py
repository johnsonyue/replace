import multi_thread
import time
import random
import caida

def task(argv,resource):
	sleep_time = random.randint(1,5)
	for arg in argv:
		print str(arg)+" ",
	print "sleep "+str(sleep_time)
	time.sleep(sleep_time)
		
	result = False
	if (random.randint(1,100) % 2):
		result = True

	for arg in argv:
		print "resource: "+str(arg)+" ",
	print str(resource)+" ",
	print str(result)
	
	return result

#argv_list = [(1,1,1), (2,2,2), (3,3,3), (4,4,4), (5,5,5), (6,6,6), (7,7,7), (8,8,8)]
#resource_list  = [1,2,3,4,5]
#multi_thread.run_with_multi_thread(task,argv_list,resource_list,4)

#auth_info=caida.load_auth("accounts.json")
#print caida.get_time_list_fromsite("20161219",auth_info["username"], auth_info["password"])
caida.download_date("20161219", root_dir="./data", proxy_file="proxy_list", mt_num=3);
