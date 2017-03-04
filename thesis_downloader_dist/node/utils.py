def read_auth(auth_file, account):
	ret = [];

	is_provided = False;
	for line in open(auth_file, 'r'):
		if (line=="\n"):
			continue;
		if (is_provided and len(re.findall("#",line)) ==0):
			ret.append(line.strip('\n'));
		elif(is_provided):
			break;

		if (len(re.findall("#"+account,line)) != 0):
			is_provided = True;
	return ret;

#must be of the same length.
def time_cmp(t1, t2):
	for i in range(len(t1)):
		if (t1[i] != t2[i]):
			break;
	if (i < len(t1)):
		return int(t1[i]) - int(t2[i]);
	return 0;
