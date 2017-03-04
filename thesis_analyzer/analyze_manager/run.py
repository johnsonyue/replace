import sys
import analyze_manager
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
	if not source.split('_')[0] in valid_source:
		usage();
		exit();
	
	cfg = config.get_config_section_dict("config.ini","code");
	code_path = cfg["code_path"];
	cfg = config.get_config_section_dict(code_path+"/analyzer.ini","files");
	
	state_file_name = code_path+"/"+cfg["state_file_name"];
	log_file_name = code_path+"/"+cfg["log_file_name"];
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
		print analyze_manager.on_notify(log_file_name, state_file_name, notify_type, args);
	elif (type=="get_task"):
		print analyze_manager.get_task(state_file_name);
	elif (type=="auth"):
		if (len(argv) < 5):
			usage();
			exit();
		node_id = argv[3];
		node_key = argv[4];
		print analyze_manager.auth_node(secret_file, node_id, node_key);
if __name__ == "__main__":
	main(sys.argv);
