import re

ip_list = {}

while True:
	try:
		line = raw_input()
		secs = line.split('\t')
		for e in secs:
			if not re.findall("\*", e):
				ip_list[e] = ""
	except:
		for k in ip_list.keys():
			print k
		break
		
