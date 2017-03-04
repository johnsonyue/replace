import HTMLParser
import urllib
import urllib2
import re
import os
import cookielib
import threading
import download_worker
import time
import math

#html parsers.
class iPlaneParser(HTMLParser.HTMLParser):
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

def get_latest_time_fromsite(username, password):
	url = "https://data-store.ripe.net/datasets/iplane-traceroutes/";
		
	print "logging in...";
	params = { "username": username, "password": password }; 
	cj = cookielib.CookieJar();
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));

	login_url = "https://access.ripe.net/?originalUrl=https%3A%2F%2Fdata-store.ripe.net%2Fdatasets%2Fiplane-traceroutes%2F&service=datarepo";
	post_data = urllib.urlencode(params).encode('utf-8');

	opener.open(login_url, post_data);
	print "done.";

	f = opener.open(url);
	text = f.read();

	parser = iPlaneParser();
	parser.feed(text);
	
	e = parser.dir[-1].strip('/');
	res = parse_latest_year(url+e, opener);
	
	return res;

def parse_latest_year(url, opener):
	f = opener.open(url);
	text = f.read();
	
	parser = iPlaneParser();
	parser.feed(text);
	
	res = parser.file[-1];
	list = res.split('.')[0].split['_'];
	res = list[1]+list[2]+list[3];
	
	return res;
	
def construct_url_fromtime(target_time):
	url = "https://data-store.ripe.net/datasets/iplane-traceroutes/";
	target_year = target_time[:4];
	target_month = target_time[4:6];
	target_day = target_time[6:8];
	
	res = url+target_year+"/traces_"+target_year+"_"+target_month+"_"+target_day+".tar.gz";

	return res;

#downloading with multi-thread support.
def download_segemeted_iplane_restricted_worker_mt_wrapper(url, dir, file, opener, start, end, res_list, started_list, ind, proxy=""):
	started_list[ind] = True;
	res = download_worker.download_segemented_iplane_restricted_worker(url, dir, file, opener, start, end, proxy);

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

def download_date(date, root_dir="/media/download_iplane/", proxy_file="", seg_size=20*1024*1024, mt_num=0):
	auth = read_auth("auth", "iplane");
	is_succeeded = False;
	url = construct_url_fromtime(date);

	dir = root_dir+"/"+date+"/";
	file = url.split('/')[-1];
	if (not os.path.exists(dir)):
		os.makedirs(dir);
	
	opener = download_worker.get_iplane_opener(auth[0], auth[1]);
	if (mt_num == 0):
		opener.open(url);
		
	elif (mt_num >= 1):
		#get the size first.
		file_size = download_worker.get_iplane_file_size(opener, url);
		if file_size == -1:
			return
		print "file_size: "+str(file_size)
		file_num = int(math.ceil(float(file_size)/seg_size));
		if file_num == 0:
			return
		
		#to get the range list.
		range_list = [];
		for i in range(0,file_num-1):
			range_list.append((i*seg_size, (i+1)*seg_size-1));
		if (file_num == 1):
			i = -1
		range_list.append(((i+1)*seg_size, file_size));
		
		is_finished = [False for i in range(file_num)];
		is_started = [False for i in range(file_num)];
		proxy_list = [];
		fp = open(proxy_file,'rb');
		for line in fp.readlines():
			proxy_list.append(line.strip('\n'));
		fp.close();
		cur_proxy = 0;
		
		while(True):
			task_list = [];
			th_pool = [];
			has_started = False;
			for i in range(file_num):
				if (not is_finished[i] and not is_started[i]):
					task_list.append(i);
				if (is_started[i]):
					has_started = True;
					
			if (len(task_list) == 0 and not has_started):
				break;
			
			for i in range(len(task_list)):
				rang = range_list[task_list[i]];
				ind = task_list[i];
				proxy = proxy_list[cur_proxy];
				cur_proxy = cur_proxy + 1;
				if (cur_proxy >= len(proxy_list)):
					cur_proxy = 0;
					time.sleep(10);

				fn = file+"."+str(ind);
				if( os.path.exists(dir+fn) ):
                                        print "skipping existing file: "+fn;
                                        is_finished[ind] = True;
                                        continue;

				th = DownloadThread(target=download_segemeted_iplane_restricted_worker_mt_wrapper, args=(url,dir,fn,opener,rang[0],rang[1],is_finished,is_started,ind,proxy,) );
				th_pool.append(th);
				th.start();
				
				while(get_alive_thread_cnt(th_pool) >= mt_num):
					time.sleep(1);
		
		download_worker.assemble_segements(dir, file);

#download_date("20160710", proxy_file="proxy_iplane", seg_size=20*1024*1024, mt_num=10);
