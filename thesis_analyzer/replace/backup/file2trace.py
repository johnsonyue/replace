import sys
import re

def is_notation_caida(line):
	return line.split(' ')[0] == "#"
	
def build_caida():
	sys.stderr.write("MSG: started parsing caida ...\n")
	
	while True:
		try:
			line=raw_input()
			if (line.split("\t")[0] == "!!"):
				print line
			elif (not is_notation_caida(line)):
				sections = line.strip('\n').split('\t')

				#destination ip: sections[2], is_replied: sections[6]
				sys.stdout.write(sections[2]+'\t'+sections[6])
				for i in range(14,len(sections)):
					if sections[i] == "q":
						continue
					sys.stdout.write('\t'+sections[i].split(';')[0])
				print
		except:
			sys.stderr.write("MSG: finished parsing caida.\n")
			return

def output_iplane_trace(target_ip, trace_list):
	if len(trace_list) == 0:
		return
	if target_ip == trace_list[-1]:
		is_replied = "R"
	else:
		is_replied = "N"
	sys.stdout.write(target_ip+"\t"+is_replied)
	for h in trace_list:
		if h != "0.0.0.0":
			sys.stdout.write("\t"+h)
	print
	trace_list[:] = []

def build_iplane():
	sys.stderr.write("started parsing iplane ...\n")
	trace_list = []
	target_ip = ""
	try:
		while True:
			line=raw_input()
			if (line.split("\t")[0] == "!!"):
				print line
				continue
			is_delimiter = False
			if line.split('\t')[0].split(':')[0] == "destination":
				target_ip = line.split(' ')[1]
				is_delimiter = True
			elif line.split('\t')[0].split(' ')[0] == "read":
				continue
			else:
				trace_list.append(line.split(':')[1].split(' ')[1])
			
			if is_delimiter and len(trace_list) != 0:
				output_iplane_trace(target_ip, trace_list)
			
	except:
		output_lg_trace(target_ip, trace_list)
		sys.stderr.write("finished parsing iplane.\n")
		return
	
def output_lg_trace(target_ip, trace_list):
	if target_ip == trace_list[-1]:
		is_replied = "R"
	else:
		is_replied = "N"
	sys.stdout.write(target_ip+"\t"+is_replied)
	for h in trace_list:
		sys.stdout.write("\t"+h)
	print
	trace_list[:] = []

def build_lg():
	sys.stderr.write("started parsing lg ...\n")
	trace_list = []
	target_ip = ""
	try:
		while True:
			line=raw_input()
			is_delimiter = False
			if re.findall("from", line):
				target_ip = line.split(' ')[2]
				is_delimiter = True
			elif re.findall("-", line):
				continue
			else:
				trace_list.append(line.split(':')[1].strip('\n'))
			
			if is_delimiter and len(trace_list) != 0:
				output_lg_trace(target_ip, trace_list)
			
	except:
		output_lg_trace(target_ip, trace_list)
		sys.stderr.write("finished parsing lg.\n")
		return

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
