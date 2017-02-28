import sys

import trace

#uniform caida.
def build_path(hops_str,ignore_blank=True):
	if (ignore_blank):
		path=""
		hop_list = hops_str.split('\t')
		for i in range(len(hop_list)):
			if hop_list[i] != "q":
				path += hop_list[i]
		path.strip('\t')
		return path
	return hops_str

def uniform_caida():
	sys.stderr.write("Message: started parsing caida...\n")
	is_header_updated = False
	header=""
	while True:
		try:
			line=raw_input()
			if (line.split(' ')[0] == "!!"): #header
				header=line.split(' ',1)[1]
			elif (not line.split(' ')[0] == "#"): #not comment
				fields = line.strip('\n').split('\t',13)
				if (not is_header_updated):
					src_ip = fields[1]
					header = trace.update_src_ip(header,src_ip)
					print header

				dst_ip = fields[2]
				timestamp = fields[5]
				hops_str = fields[13]
				hops = build_path(hops_str)
				
				print trace.build_trace_str(dst_ip, timestamp, hops)
		except:
			break
	sys.stderr.write("Finished parsing caida.")

def usage():
	sys.stderr.write("./file2trace.py caida/iplane/lg\n")

def main(argv):
	if (len(argv) < 2):
		usage()
		exit()
	source = argv[1]
	if source == "caida":
		build_caida()
	elif source == "iplane":
		build_iplane()
	elif source == "lg":
		build_lg()

if __name__ == "__main__":
	main(sys.argv)
