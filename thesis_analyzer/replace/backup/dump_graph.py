import sys
import signal
import re

node = {}
edge = {}
prev_node = -1
num_node = 0
		
def parse_trace():
	try:
		cnt = 0
		node = ""
		while True:
			line = raw_input()
			if line.split('\t')[0] == "!!":
				cnt = 0
				node = line.split('\t')[2]
				continue
			prev_node = -1
			global num_node
			for n in (line.split('\t')[3:]):
				n = n.split(',')[0]
				if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",n):
					continue

				index = -1
				if not node.has_key(n):
					node[n] = num_node
					index = node[n]
					num_node = num_node + 1
				else:
					index = node[n]
				
				if (prev_node != -1):
					edge[(prev_node, index)] = ""

				prev_node = index
	except:
		return

def print_num():
	print str(len(node.keys())) + " " + str(len(edge.keys()))

def print_node():
	keys = sorted(node, key=lambda x: node[x])
	for k in keys:
		print k
def print_edge():
	for e in edge:
		print str(e[0]) + " " + str(e[1])

def usage():
	sys.stderr.write("python dump_graph.py")

def main(argv):
	parse_trace()
	print_num()
	print_node()
	print_edge()
	
if __name__ == "__main__":
	main(sys.argv)
