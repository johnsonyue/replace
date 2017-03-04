import geoip
import sys
import signal
import re

country_ip = {"country":{}, "city":{}}
AF = []
cnt = 0

def parse_trace():
	geoip_helper = geoip.geoip_helper()
	
	try:
		global cnt
		while True:
			line = raw_input()
			ip = line.strip('\n')
			cnt = cnt + 1
			try:
				geo = (geoip_helper.query(ip)["mmdb"])
			except:
				print ip
				continue
			insert_geoip(geo)
			if geo["country"] == "AF":
				AF.append((ip, geo))
	except Exception, ex:
		return

def insert_geoip(geo):
	country = geo["country"]
	city = geo["city"]
	if not country_ip["country"].has_key(country):
		country_ip["country"][country] = 1
	else:
		country_ip["country"][country] = country_ip["country"][country] + 1
	if not country_ip["city"].has_key(country):
		country_ip["city"][country] = {city:1}
	elif not country_ip["city"][country].has_key(city):
		country_ip["city"][country][city] = 1
	else:
		country_ip["city"][country][city] = country_ip["city"][country][city] + 1

def print_result(country_ip):
	print cnt
	country = country_ip["country"]
	city = country_ip["city"]
	for k in country.keys():
		print k + " " + str(country[k])
		for c in city[k].keys():
			print "\t" + c.encode('utf-8') + " " + str(city[k][c])
	
	for i in range(len(AF)):
		print AF[i][0] + "\t" + str(AF[i][1])

def sig_handler(sig, frame):
	print_result(country_ip)
	exit()

def main(argv):
	signal.signal(signal.SIGINT, sig_handler)
	parse_trace()
	print_result(country_ip)
	
if __name__ == "__main__":
	main(sys.argv)
