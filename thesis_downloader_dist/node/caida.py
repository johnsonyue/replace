import HTMLParser
import urllib2
import re
import os
import threading
import time
import download_worker

#html parsers.
class CaidaParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self);
		self.img_cnt=0;
		self.alt="";
		self.file=[];
		self.dir=[];

	def get_attr_value(self, target, attrs):
		for e in attrs:
			key = e[0];
			value = e[1];
			if (key == target):
				return value;

	def handle_starttag(self, tag, attrs):
		if (tag == "img"):
			if (self.img_cnt >=2):
				alt_value = self.get_attr_value("alt", attrs);
				self.alt=alt_value;
			self.img_cnt = self.img_cnt + 1;
		
		if (tag == "a" and self.alt == "[DIR]"):
			href_value = self.get_attr_value("href", attrs);
			self.dir.append(href_value);
		elif (tag == "a" and self.alt != ""):
			href_value = self.get_attr_value("href", attrs);
			self.file.append(href_value);

#utils.
def read_auth(auth_file, account):
	ret = [];

	is_provided = False;
	for line in open(auth_file, 'r'):
		if (line=="\n"):
			continue;
		if (is_provided and len(re.findall("#",line)) ==0):
			ret.append(line.strip('\n'));
		elif(is_provided):
			break;

		if (len(re.findall("#"+account,line)) != 0):
			is_provided = True;
	return ret;

#must be of the same length.
def time_cmp(t1, t2):
	for i in range(len(t1)):
		if (t1[i] != t2[i]):
			break;
	if (i < len(t1)):
		return int(t1[i]) - int(t2[i]);
	return 0;

#target retrieving.
#latest time.
def get_latest_time_fromsite(username, password):
	url = "https://topo-data.caida.org/team-probing/list-7.allpref24/";
	passwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm();
	passwd_mgr.add_password("topo-data", url, username, password);

	opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwd_mgr));
	team_dir = ["team-1/daily/", "team-2/daily/", "team-3/daily/"]; 

	temp = [];
	for t in team_dir:
		f = opener.open(url+t);
		text = f.read();
		parser = CaidaParser();
		parser.feed(text);
		
		e = parser.dir[-1].strip('/');
		temp.append(parse_latest_year(url+t+e, opener));
	
	res = temp[0];
	for t in temp[1:]:
		if(time_cmp(t, res) > 0):
			res = t;
	
	return res;

def parse_latest_year(url, opener):
	f = opener.open(url);
	text = f.read();
	
	parser = CaidaParser();
	parser.feed(text);
	
	res = parser.dir[-1];
	res = res.split('-')[1].strip('/');
	return res;

#url list of files with specified time.
def get_time_list_fromsite(target_time, username, password):
	url = "https://topo-data.caida.org/team-probing/list-7.allpref24/";
	passwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm();
	passwd_mgr.add_password("topo-data", url, username, password);

	opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwd_mgr));
	team_dir = ["team-1/daily/", "team-2/daily/", "team-3/daily/"]; 

	res = [];
	for t in team_dir:
		f = opener.open(url+t);
		text = f.read();
		parser = CaidaParser();
		parser.feed(text);
		
		target_year = target_time[:4];
	
		for e in parser.dir:
			if(time_cmp(e.strip('/'), target_year) == 0):
				temp = parse_year_dir(target_time, url+t+e, opener);
				res.extend(temp);
				break;
	
	return res;

def parse_year_dir(target_time, url, opener):
	f = opener.open(url);
	text = f.read();
	
	parser = CaidaParser();
	parser.feed(text);

	for e in parser.dir:
		time = e.split('-')[1].strip('/');
		if (time_cmp(time, target_time) == 0):
			res = parse_time_dir(url+e, opener);
			return res;
	
	return [];

def parse_time_dir(url, opener):
	f = opener.open(url);
	text = f.read();
	
	parser = CaidaParser();
	parser.feed(text);

	res = [];
	for e in parser.file:
		if ( len(e.split('.')) != 8 ):
			continue;
		res.append(url+e);
	
	return res;

#downloading with multi-thread support.
def download_caida_restricted_worker_mt_wrapper(url, dir, file, username, password, res_list, started_list, ind, proxy=""):
	started_list[ind] = True;
	res = download_worker.download_caida_restricted_worker(url, dir, file, username, password, proxy);
	res_list[ind] = res;
	started_list[ind] = False;
	

class DownloadThread(threading.Thread):
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

def download_date(date, root_dir="/data/data/caida/ipv4/", proxy_file="", mt_num=0 ):
	auth = read_auth("auth", "caida");
	is_succeeded = False;
	round_cnt = 1;
	while(not is_succeeded):
		try:
			url_list = get_time_list_fromsite(date, auth[0], auth[1]);
			is_succeeded = True;
		except:
			is_succeed = False;
			round_cnt = round_cnt + 1;
			time.sleep(10*round_cnt);

	dir = root_dir+date+"/";
	if (not os.path.exists(dir)):
		os.makedirs(dir);
	
	if (mt_num == 0):
		for url in url_list:
			team = url.split('/')[5];
			suffix = url.split('/')[-1].split('.',4)[-1];
			file = team+"."+suffix;
			if( not os.path.exists(dir+file) ):
				res = False;
				while(not res):
					res = download_worker.download_caida_restricted_worker(url, dir, file, auth[0], auth[1]) 

	elif (mt_num >= 1):
		is_finished = [False for i in range(len(url_list))];
		is_started = [False for i in range(len(url_list))];
		proxy_list = [];
		fp = open(proxy_file,'rb');
		for line in fp.readlines():
			proxy_list.append(line.strip('\n'));
		cur_proxy = 0;
		
		while(True):
			task_list = [];
			th_pool = [];
			has_started = False;
			for i in range(len(url_list)):
				if (not is_finished[i] and not is_started[i]):
					task_list.append(i);
				if (is_started[i]):
					has_started = True;
					
			if (len(task_list) == 0 and not has_started):
				break;
			
			for i in range(len(task_list)):
				url = url_list[task_list[i]];
				team = url.split('/')[5];
				suffix = url.split('/')[-1].split('.',4)[-1];
				file = team+"."+suffix;
				ind = task_list[i];
				proxy = proxy_list[cur_proxy];
				cur_proxy = cur_proxy + 1;
				if (cur_proxy >= len(proxy_list)):
					cur_proxy = 0;
					time.sleep(10);

				if( os.path.exists(dir+file) ):
                                        print "skipping existing file: "+file;
                                        is_finished[ind] = True;
                                        continue;

				th = DownloadThread(target=download_caida_restricted_worker_mt_wrapper, args=(url,dir,file,auth[0],auth[1],is_finished,is_started,ind,proxy,) );
				th_pool.append(th);
				th.start();
				
				while(get_alive_thread_cnt(th_pool) >= mt_num):
					time.sleep(1);
