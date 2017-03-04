import sys
import networkx as nx
import pickle
import bz2

import trace

graph = nx.Graph()

def build_graph():
	prev_node = -1
	while True:
		try:
			line = raw_input()
			if ( line.split(trace.header_delimiter)[0] == trace.header_indicator ):
				continue #ignore headers.
			field_list = line.split(trace.field_delimiter)

			#dst_ip = field_list[ trace.trace_index["dst_ip"] ]
			#timestamp = field_list[ trace.trace_index["timestamp"] ]
			hops = field_list[ trace.trace_index["hops"] ]
			hop_list = hops.split(trace.hop_delimiter)
			for h in hop_list:
				if h == trace.blank_holder:
					continue #ignores blank
				reply_list = h.split(trace.reply_delimiter)
				first_reply = reply_list[0]
				ip = first_reply.split(trace.ip_delimiter)[trace.hop_index["ip"]]
				if (prev_node != -1):
					graph.add_edge(prev_node, ip)
				prev_node = ip
		except:
			break

def print_graph():
	for e in graph.edges():
		print "%s %s" % (e[0], e[1])

def export_graph():
	f = bz2.BZ2File("graph.bz2",'w')
	pickle.dump(graph, f)

build_graph()
print_graph()
