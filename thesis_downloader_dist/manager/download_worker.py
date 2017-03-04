import urllib
import urllib2
import os
import cookielib
import copy
import re

#caida restricted.
def download_caida_restricted_worker(url, dir, file, username, password, proxy=""):
	passwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm();
	passwd_mgr.add_password("topo-data", url, username, password);

	opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwd_mgr));

	if(proxy != ""):
		opener.add_handler(urllib2.ProxyHandler({"http":proxy}));

	if not os.path.exists(dir):
		os.makedirs(dir);

	res = True;
	ex = None;
	try:
		if not os.path.exists(dir+file):
			f = opener.open(url, timeout=10);
			fp = open(dir+file, 'wb');
			fp.write(f.read());
			fp.close();
			f.close();
	except Exception, e:
		ex = e;
		res = False;
		if os.path.exists(dir+file):
			os.remove(dir+file);
	
	if res:
		print url.split('/')[-1] + " " + proxy + " " + str(res) + " " + (str(ex) if ex!=None else "succeeded");
	
	return res;

#iplane restricted.
def get_iplane_opener(username, password):
	print "logging in...";
	login_url = "https://access.ripe.net/?originalUrl=https%3A%2F%2Fdata-store.ripe.net%2Fdatasets%2Fiplane-traceroutes%2F&service=datarepo";
	params = { "username": username, "password": password }; 
	cj = cookielib.CookieJar();
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
	post_data = urllib.urlencode(params).encode('utf-8');

	f = opener.open(login_url, post_data);
	print "done.";

	return opener;

def get_iplane_file_size(opener, url):
	request=urllib2.Request(url);
	request.add_header("Range", "bytes=0-10737418240");
	f = opener.open(request);
	res = int(f.info()["Content-Length"])
	f.close();
	print res, str(res/1024/1024)+" MB";

	return res;

def download_segemented_iplane_restricted_worker(url, dir, file, opener, start, end, proxy=""):
	request=urllib2.Request(url);
	request.add_header( "Range", "bytes="+str(start)+"-"+str(end) )
	request.add_header("User-agent", "Mozila/5.0");

	#print ("downloading "+file+" "+str(start/1024)+"K"+"-"+str(end/1024)+"K"+" with proxy "+proxy);
	print ("downloading "+file+" "+str(start/1024)+"K"+"-"+str(end/1024)+"K"+" with proxy "+proxy+" start:"+str(start)+" end:"+str(end));
	if(proxy != ""):
		opener.add_handler(urllib2.ProxyHandler({"http":proxy}));

	if not os.path.exists(dir):
		os.makedirs(dir);

	res = True;
	ex = None;
	try:
		if not os.path.exists(dir+file):
			f = opener.open(request, timeout=10);
			fp = open(dir+file, 'wb');
			#print f.info();
			#print f.code;
			fp.write(f.read());
			fp.close();
			f.close();
	except Exception, e:
		print e
		ex = e;
		res = False;
		if os.path.exists(dir+file):
			os.remove(dir+file);
	
	#if res:
	print file + " " + proxy + " " + str(res) + " " + (str(ex) if ex!=None else "succeeded");
	
	return res;

def assemble_segements(dir, file):
	print "assembling segements ... ";
	if not os.path.exists(dir):
		os.makedirs(dir);

	file_list = os.listdir(dir);
	num_file = 0;
	for fn in file_list:
		if(re.findall(file+".\d+", fn)):
			num_file = num_file + 1;
	
	fp = open(dir+"/"+file, 'wb')
	for i in range(num_file):
		fn = dir+"/"+file+"."+str(i);
		f = open(fn, 'rb');
		fp.write(f.read());
		f.close();
		#os.system("rm -f "+fn);
	
	fp.close()
	print "finished assembling segements";
	
	return "";
	

#irr delegate
def download_irr_delegate(url_list, dir, file):
	if not os.path.exists(root+dir+file):
		urllib.urlretrieve(url, root+dir+file);

'''
url = "https://data-store.ripe.net/datasets/iplane-traceroutes/2016/traces_2016_01_01.tar.gz";
dir = "./";
file = "test";
opener = get_iplane_opener("johnsonyuehit@163.com", "johnsonyue123");
size = get_iplane_file_size(opener, url);
print size,str(size/1024/1024)+" MB";
start = 0;
end = 100;
download_segemented_iplane_restricted_worker(url, dir, file, opener, start, end);
'''
