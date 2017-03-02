import caida
auth = caida.read_auth("auth", "caida")
print caida.get_time_list_fromsite("20161219",auth[0], auth[1])
