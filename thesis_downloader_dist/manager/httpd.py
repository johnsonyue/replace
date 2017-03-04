import time
import json
import BaseHTTPServer
import cgi

import manager

HOST_NAME = '172.17.0.4'
PORT_NUMBER = 80

class Server(BaseHTTPServer.HTTPServer):
	def __init__(self, (HOST_NAME, PORT_NUMBER), handler, config):
		BaseHTTPServer.HTTPServer.__init__(self, (HOST_NAME, PORT_NUMBER), handler)
		self.config = config
	
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
	def do_GET(self):
		"""Respond to a GET request."""
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write("<html><head><title>BaseHTTPServer</title></head>")
		self.wfile.write("<body><p>It works!</p>")
		self.wfile.write("</body></html>")
	def do_POST(self):
		action = self.path.replace('/','')
		valid_action = [ "get_task", "on_notify", "auth" ]
		if ( action not in valid_action ):
			self.wfile.write("Invalid Action: %s" % action)
			return
		
		#get the config file from server.
		#note that the http request handler is not stateful.
		#however it can access the server data members.
		config = self.server.config
		log_file_name = config["log_file_name"]
		state_file_name = config["state_file_name"]
		secret_file_name = config["secret_file_name"]

		post = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
			'CONTENT_TYPE':self.headers['Content-Type'],
		})

		if ( action == "get_task" ):
			task = manager.get_task(state_file_name)
			self.wfile.write(task)
		elif ( action == "on_notify" ):
			notify_type = post["notify_type"]
			node_id = post["node_id"]
			task = post["task"]
			dir = post["dir"]
			time_used = "" #optional
			if (post.has_key("time_used")):
				time_used = post["time_used"]
			args = {
				"node_id" : node_id,
				"task" : task,
				"dir" : dir,
				"time_used" : time_used
			}
			result = manager.on_notify(log_file_name, state_file_name, notify_type, args);
			self.wfile.write(result)
		elif ( action == "auth" ):
			node_id = post["node_id"]
			node_key = post["node_key"]
			result = manager.auth_node(secret_file_name, node_id, node_key);
			self.wfile.write(result)
		elif ( action == "get_path" ):
			print "SHIT"

if __name__ == '__main__':
	config = json.loads(open("config.json").read())
	httpd = Server( (HOST_NAME, PORT_NUMBER), Handler, config )
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
