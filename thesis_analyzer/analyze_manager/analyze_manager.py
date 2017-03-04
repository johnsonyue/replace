import os
import time

def get_all_pid():
	return [ i for i in os.listdir('/proc') if i.isdigit()];

def get_all_fd(file_path):
	all_fd = [];
	for pid in get_all_pid():
		fd_dir = '/proc/{pid}/fd'.format(pid = pid);
       		if os.access(fd_dir, os.R_OK) == False:
			continue;

		for fd in os.listdir(fd_dir):
			fd_path = os.path.join(fd_dir, fd);
			if os.path.exists(fd_path) and os.readlink(fd_path) == file_path:
				all_fd.append(fd_path);

        return all_fd;

def is_occupied(file_name):
	file_path = os.path.join(os.getcwd() ,file_name);
	fd_num = len(get_all_fd(file_path));
	
	return fd_num >= 1;

def auth_node(secret_file, node_id, node_key):
	fp = open(secret_file,'r');
	for line in fp.readlines():
		list = line.split(' ');
		if (list[0] == node_id and list[1].strip('\n') == node_key):
			fp.close();
			return True;
	
	fp.close();
	return False;

def update_state_file(file_name, is_init = False):
	if (is_init):
		os.system("./date.sh | sed -e 's/$/ unassigned/' > "+file_name)
	else:
		if (not os.path.exists(file_name)):
			print ("file does not exist");
			exit();
		while(is_occupied(file_name)):
			time.sleep(random.randint(1,3));
		f = os.popen("./date.sh")
		date_list = map (lambda x:x.strip('\n'), f.readlines())
		f.close()
		f = open(file_name,'r');
		state_list = f.readlines()
		f.close()
		
		fp.open(file_name,'w')
		for i in range(len(date_list)):
			state_ind = -1
			for j in range(len(state_list)):
				if date_list[i] == state_list[j].split(' ')[0]:
					state_ind = j
					break
			if state_ind != -1:
				fp.write(state_list[state_ind])
			else:
				fp.write(date_list[i] + " unassigned")

		fp.close()
#enum state={finished, unassigned, pending, terminated};
def change_state(file_name, date, state):
	while(is_occupied(file_name)):
			time.sleep(random.randint(1,3));
	fp = open(file_name, 'r');
	lines = fp.readlines();
	fp.close();

	while(is_occupied(file_name)):
			time.sleep(random.randint(1,3));
	fp = open(file_name, 'w');
	for line in lines:
		if (line.split(' ')[0] == date):
			fp.write(date+" "+state+'\n');
		else:
			fp.write(line);
	fp.close();

def get_task(file_name):
	while(is_occupied(file_name)):
			time.sleep(random.randint(1,3));
	fp = open(file_name, 'r');
	lines = fp.readlines();
	res = "";
	for i in range(len(lines)-1, -1, -1):
		state = lines[i].split(' ')[1].strip('\n');
		if(state != "finished" and state != "pending"):
			res = lines[i].split(' ')[0];
			break;
		
	return res;

def on_notify(log_file_name, state_file_name, type, args):
	while(is_occupied(log_file_name)):
			time.sleep(random.randint(1,3));
	fp = open(log_file_name, 'a');
	strftime = time.strftime("%Y-%m-%d %H:%M:%S");
	str = "";
	
	if (type == "finished"):
		node_id = args["node_id"];
		task = args["task"];
		time_used = args["time_used"];

		change_state(state_file_name, task, "finished");
		fp.write(strftime + " " + node_id + " " + task + " finished, time used:  " + time_used + "(s)\n");
		str = strftime + " " + node_id + " " + task + " finished, time used:  " + time_used + "(s)";
	elif (type == "started"):
		node_id = args["node_id"];
		task = args["task"];

		change_state(state_file_name, task, "pending");
		fp.write(strftime + " " + node_id + " " + task + " started\n");
		str = strftime + " " + node_id + " " + task + " started";
	elif (type == "terminated"):
		node_id = args["node_id"];
		task = args["task"];

		change_state(state_file_name, task, "terminated");
	
		fp.write(strftime + " " + node_id + " " + task + " terminated\n");
		str = strftime + " " + node_id + " " + task + " terminated";

	fp.close();
	
	return str;

#update_state_file("files/state" , is_init = True)
