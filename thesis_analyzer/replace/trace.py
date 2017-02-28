#For reference: CAIDA "warts" format
#trace = {
#	"source":0, #{caida, iplane, lg, ripeatlas ..}
#	"date":1, #{yyyymmdd}
#	"src_ip":2, #Source IP of skitter/scamper monitor performing the trace.
#	"dst_ip":3, #Destination IP being traced.
#	"timestamp":4, #Timestamp when trace began to this destination.
#	"hops":5, #Response hop list.
#	"requestttl":6, #TTL set in request packet which elicited a response from the destination.
#	"replyttl":7, #TTL found in reply packet from destination.
#	"haltreason":8, #The reason, if any, why incremental probing stopped.
#	"haltdata":9 #Extra data about why probing halted.
#}

header_index = {
	"source":0, #{caida, iplane, lg, ripeatlas ..}
	"date":1, #yyyymmdd
	"monitor":2, #name of the monitor
	"src_ip":3, #Source IP of skitter/scamper monitor performing the trace.
}
trace_index = {
	"dst_ip":0, #Destination IP being traced.
	"timestamp":1, #Timestamp when trace began to this destination.
	"hops":2 #Response hop list.
}

#use '\t' as delimiter.
#use '!!' as header indicator.
def print_header(source, date, monitor, src_ip):
	print ( "!! %s %s %s %s" % (source, date, monitor, src_ip) )

def bash_import():
	print "declare -A header"
	print "header=(",
	for k,v in header_index.items():
		print ( "[%s]=\"%d\" " % (k, v) ),
	print ")"

	print "declare -A trace"
	print "trace=(",
	for k,v in trace_index.items():
		print ( "[%s]=\"%d\" " % (k, v) ),
	print ")"

	return ""

def update_src_ip(header, src_ip):
	fields = header.split(' ')
	fields[header_index["src_ip"]] = src_ip
	
	header = "!!"
	for i in range(len(fields)):
		header += " "+fields[i]
	
	return header

def build_trace_str(dst_ip, timestamp, hops):
	field_list = ["" for i in range( len(trace_index.keys()) )]
	field_list[ trace_index["dst_ip"] ] = dst_ip
	field_list[ trace_index["timestamp"] ] = timestamp
	field_list[ trace_index["hops"] ] = hops
	
	str = ""
	for i in range(len(field_list)):
		str += field_list[i]+"\t"
	
	return str.strip('\t')

def usage():
	#sort dict by value.
	header_items = sorted( header_index.items(), lambda a,b: cmp(a[1],b[1]) )
	trace_items = sorted( trace_index.items(), lambda a,b: cmp(a[1],b[1]) )
	print "Header: "
	for k,v in header_items:
		print ( "%d. %s" % (v, k) )
	print "Trace: "
	for k,v in trace_items:
		print ( "%d. %s" % (v, k) )
	
	print "   Hop format:"
	print "          / q                               (for no responding IP)"
	print "         |"
	print "   hop= <   IP,RTT,nTries                   (for only one responding IP)"
	print "         |"
	print "          \ IP,RTT,nTries;IP,RTT,nTries;... (for multiple responding IPs)"
	print "   where"
	print "       IP -- IP address which sent a TTL expired packet"
	print "       RTT -- RTT of the TTL expired packet"
	print "       nTries -- number of tries before response received from hop"
