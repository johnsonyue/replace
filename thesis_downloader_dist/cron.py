import datetime

from worker import caida
from manager import manager

start_time = "20070913"
#date = datetime.date.today().isoformat().replace('-','')
#auth_info = caida.load_auth("../worker/accounts.json")
#username=auth_info["username"]
#password=auth_info["password"]
#caida.get_latest_time_from_site("state",date,start_time,is_init=True)
manager.update_state_file("state","20160727",start_time="20070913",is_init=True);
#update_state_file("state","20160802");

#auth = iplane.read_auth("auth","iplane");
#end_time = iplane.get_latest_time_fromsite(auth[0],auth[1])
#update_state_file("state",end_time,start_time="20060623",is_init=True);
