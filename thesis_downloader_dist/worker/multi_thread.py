import threading
import time

class TaskThread(threading.Thread):
	def __init__(self, target, args):
		threading.Thread.__init__(self, target=target, args=args);
		self.start_time = time.time();
	
	def get_time_alive(self):
		end_time = time.time();
		return end_time - self.start_time;

def get_alive_thread_cnt(th_pool):
	cnt_alive = 0;
	for i in range(len(th_pool)):
		t = th_pool[i];
		#if (t.is_alive() and t.get_time_alive() >= 1):
		if (t.is_alive() ):
			cnt_alive = cnt_alive + 1;
	for th in th_pool:
		if (not th.is_alive()):
			th_pool.remove(th);
	
	return cnt_alive;

def task_wrapper(func, argv, resource, res_list, started_list, ind):
	started_list[ind] = True;
	res = func(argv, resource)
	res_list[ind] = res;
	started_list[ind] = False;
	
#each task dependently owns 1 argv, 
#all tasks share 1 same resource list.
#type of resource is <type_list>.
def run_with_multi_thread(func, argv_list, resource_list, mt_num=-1): #list of argv(s)
	if (mt_num <= 1):
		for argv in argv_list:
			func(argv,[""])
	elif (mt_num > 1): 
		#use flags to keep track of stage of each task.
		is_finished = [False for i in range(len(argv_list))]; 
		is_started = [False for i in range(len(argv_list))];

		cur_resource = 0
		while(True):
				task_list = [];
				th_pool = [];
				has_started = False;
				for i in range(len(argv_list)):
					if (not is_finished[i] and not is_started[i]):
						task_list.append(i);
					if (is_started[i]):
						has_started = True;
						
				if (len(task_list) == 0 and not has_started): #end condition.
					break;
				
				for i in range(len(task_list)):
					argv = argv_list[task_list[i]]
					ind = task_list[i]
					resource = resource_list[cur_resource]
					cur_resource += 1
					if (cur_resource >= len(resource_list)):
						cur_resource = 0
						time.sleep(1)

					th = TaskThread(target=task_wrapper, args=(func,argv,resource,is_finished,is_started,ind));
					th_pool.append(th);
					th.start();
					
					while(get_alive_thread_cnt(th_pool) >= mt_num):
						time.sleep(1); #periodically checking available slot.
