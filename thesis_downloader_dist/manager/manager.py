import os
import time
#import caida
import iplane

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

def is_heap_year(year):
	if (not year % 400 or not year % 4):
		return True;
	return False;

def days_in_month(year, month):
	m2d = [0,31,28,31,30,31,30,31,31,30,31,30,31];

	return m2d[month]+(1 if month == 2 and is_heap_year(year) else 0);

def next_day(date):
	y=int(date[:4]);
	m=int(date[4:6]);
	d=int(date[6:8]);
	
	num = days_in_month(y,m);
	if (d+1 > num):
		m = m + 1;
		d = 1;
		if (m > 12):
			y = y + 1;
			m = 1;
	else:
		d = d + 1;
	
	str = "%d%02d%02d" % (y, m, d);
	return str;

def update_state_file(file_name, end_time, start_time="", is_init = False):
	if (is_init):
		if (not os.path.exists(file_name)):
			open(file_name,'wb').close();
		if (start_time == ""):
			print "must provide start_time";
			exit();
	
		st = start_time;
		while(is_occupied(file_name)):
			time.sleep(random.randint(1,3));
		fp = open(file_name, 'wb');
	
	else:
		if (not os.path.exists(file_name)):
			print ("file does not exist");
			exit();

		while(is_occupied(file_name)):
			time.sleep(random.randint(1,3));
		fp = open(file_name,'r');
		st = fp.readlines()[-1].split(' ')[0];
		st = next_day(st);
		fp.close();

		while(is_occupied(file_name)):
			time.sleep(random.randint(1,3));
		fp = open(file_name,'a');
	
	y = int(st[:4]);
	m = int(st[4:6]);
	d = int(st[6:8]);

	ey = int(end_time[:4]);
	em = int(end_time[4:6]);
	ed = int(end_time[6:8]);
	
	while ( y < ey ):
		while ( m <= 12 ):
			num = days_in_month(y, m);
			while( d <= num ):
				str = "%d%02d%02d" % (y, m, d);
				fp.write(str+" unassigned"+'\n');
				d = d + 1;
			d = 1;
			m = m + 1;
		m = 1;
		y = y + 1;
	
	while ( m < em ):
		num = days_in_month(ey, m);
		while ( d <= num ):
			str = "%d%02d%02d" % (y, m, d);
			fp.write(str+" unassigned"+'\n');
			d = d + 1;
		d = 1;
		m = m + 1;
	
	while ( d <= ed ):
		str = "%d%02d%02d" % (y, m, d);
		fp.write(str+" unassigned"+'\n');
		d = d + 1;

	fp.close();

def auth_node(secret_file, node_id, node_key):
	fp = open(secret_file,'r');
	for line in fp.readlines():
		list = line.split(' ');
		if (list[0] == node_id and list[1].strip('\n') == node_key):
			fp.close();
			return True;
	
	fp.close();
	return False;
			
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

#update_state_file("state","20160727",start_time="20070913",is_init=True);
#update_state_file("state","20160802");

#auth = iplane.read_auth("auth","iplane");
#end_time = iplane.get_latest_time_fromsite(auth[0],auth[1])
#update_state_file("state",end_time,start_time="20060623",is_init=True);
