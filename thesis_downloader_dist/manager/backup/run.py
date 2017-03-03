import sys
import manager
import config

def usage():
	print "python manage.py <source> <type> <args...>";
	print "       source: caida/iplane";
	print "       type: get_task/notify/auth";
	print "       get_task";
	print "       on_notify notify_type, node_id, task, (time_used)";
	print "       auth ndoe_id, node_key";

def main(argv):
	if (len(argv) <= 1):
		usage();
		exit();
	
	source = argv[1];
	type = argv[2];
	
	valid_source = ["caida", "iplane"];
	if not source in valid_source:
		usage();
		exit();
	
	cfg = config.get_config_section_dict("config.ini","code");
	code_path = cfg["code_path"];
	cfg = config.get_config_section_dict(code_path+"/config.ini","files");
	
	if source == "caida":
		state_file_name = code_path+"/"+cfg["state_file_name"];
		log_file_name = code_path+"/"+cfg["log_file_name"];
	elif source == "iplane":
		state_file_name = code_path+"/"+cfg["state_file_name_iplane"];
		log_file_name = code_path+"/"+cfg["log_file_name_iplane"];
	secret_file = code_path+"/"+cfg["secret_file"];
	
	if (type=="on_notify"):
		if (len(argv) < 6):
			usage();
			exit();
		notify_type = argv[3];
		time_used = "";
		if (len(argv) >=7):
			time_used = argv[6];
		args = {
			"node_id" : argv[4],
			"task" : argv[5],
			"time_used" : time_used
		};
		print manager.on_notify(log_file_name, state_file_name, notify_type, args);
	elif (type=="get_task"):
		print manager.get_task(state_file_name);
	elif (type=="auth"):
		node_id = argv[3];
		node_key = argv[4];
		print manager.auth_node(secret_file, node_id, node_key);
if __name__ == "__main__":
	main(sys.argv);
