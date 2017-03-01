import urllib
import urllib2
import cookielib
import cPickle

url = "https://topo-data.caida.org/team-probing/list-7.allpref24/team-1/daily/2015/cycle-20151231/daily.l7.t1.c004458.20160102.yto-ca.warts.gz"
username = "nidebabalinsiqian@126.com";
password = "nidielinsiqianhaha";
#proxy="";

params = { "username": username, "password": password }; 
cj = cookielib.CookieJar();
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));

login_url = "https://access.ripe.net/?originalUrl=https%3A%2F%2Fdata-store.ripe.net%2Fdatasets%2Fiplane-traceroutes%2F&service=datarepo";
post_data = urllib.urlencode(params).encode('utf-8');
print "logging in...";
opener.open(login_url, post_data);
print "done.";

#opener.add_handler(urllib2.ProxyHandler({"http":proxy}));
#target_url = "https://data-store.ripe.net/datasets/iplane-traceroutes/2016/traces_2016_08_08.tar.gz";
