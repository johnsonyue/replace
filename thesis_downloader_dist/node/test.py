import urllib2

proxy_list = []
fp = open("proxy_list",'r')
for line in fp.readlines():
	proxy_list.append(line.strip('\n'))
fp.close()

auth = ["15b903031@hit.edu.cn", "yuzhuoxun123"]
url = "https://topo-data.caida.org/team-probing/list-7.allpref24/team-1/daily/2007/cycle-20070913/daily.l7.t1.c000027.20070916.amw-us.warts.gz"

opener = urllib2.build_opener(urllib2.ProxyHandler({"http":proxy}))
opener.addheaders = [('Range', 'bytes=20000-200004')]
f = opener.open(url)
fp = open("file", 'wb')
fp.write(f.read())
fp.close()
f.close()

print "done"
