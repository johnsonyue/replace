import caida
import iplane
import request_handler
import config
import time
import signal
import sys

date = "";
data_source = "";
handler = request_handler.RequestHandler("config.ini");

def usage():
	print "python run.py caida/iplane/lg"
	exit()

def sig_handler(sig, frame):
	if (date != ""):
		print handler.notify_terminated(date,data_source);
	exit();

def main(argv):
	if len(argv) < 2:
		usage()
	signal.signal(signal.SIGINT, sig_handler);
	
	global date
	global data_source
	data_source = argv[1]
	
	valid_source = ["caida", "iplane"]
	if not data_source in valid_source:
		usage()
	
	if data_source == "caida":
		proxy_file = config.get_config_section_dict("config.ini", "proxy")["proxy_file"];
		root_dir = config.get_config_section_dict("config.ini", "data")["root_dir"];
	
		while(True):
			date = handler.get_task(data_source);
			print date;
			sys.stdout.flush()
			
			start_time = time.time();
			print handler.notify_started(date,data_source);
			sys.stdout.flush()
	
			caida.download_date(date, root_dir=root_dir, proxy_file=proxy_file, mt_num=10);
	
			end_time = time.time();
			time_used = end_time - start_time;
			print handler.notify_finished(date, time_used, data_source);
			sys.stdout.flush()
	
	elif data_source == "iplane":
		proxy_file = config.get_config_section_dict("config.ini", "proxy")["proxy_file_iplane"];
		root_dir = config.get_config_section_dict("config.ini", "data")["root_dir_iplane"];
	
		while(True):
			date = handler.get_task(data_source);
			print date;
			sys.stdout.flush()
			
			start_time = time.time();
			print handler.notify_started(date,data_source);
			sys.stdout.flush()
	
			iplane.download_date(date, root_dir=root_dir, proxy_file=proxy_file, mt_num=10);
	
			end_time = time.time();
			time_used = end_time - start_time;
			print handler.notify_finished(date, time_used,data_source);
			sys.stdout.flush()
	
if __name__ == '__main__':
	main(sys.argv)
