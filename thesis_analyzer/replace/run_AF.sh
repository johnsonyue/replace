ls AF/*.txt | while read line; do cat $line | python file2trace.py lg | python dump_graph.py > `echo $line | sed 's/.txt//'`.graph; done
for f in `ls AF/*.graph`; do cnt=`cat $f | head -n 1 | awk '{print $1}'`; cat $f | tail -n +2 | head -n $cnt; done | python country_ip.py >AF/result.geo
