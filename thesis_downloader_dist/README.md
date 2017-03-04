##usage:
* manager:
	* modify config.ini (3 items: state_file_name, log_file_name, secret_file)
	* generate state file using manager.py (e.g. manager.update_state_file("state","20160727",start_time="20070913",is_init=True);)
	* create secret file for node authentication (1 node per line, e.g. node_ca 123456)
	* copy contents in web folder into your html dir (e.g. cp web/\* /var/www/html/)
	* modify config.ini in html dir (1 item: code_path)
	* chmod -R 777 manager (to give full caps of www-data)

* node:
	* modify config.ini (handler 5 items: site, get_task, notify, node_id, node_key, data 1 item: root_dir, proxy 1 item: proxy_file)
	* use proxy.py to generate proxy_list, or use create proxy file by yourself from your own proxys.
	* python run.py to start downloading.
	* to terminate , use ctrl+c.
