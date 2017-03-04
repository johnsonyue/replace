data_dir=$(awk -F " *= *" '/data_dir/ {print $2}' analyzer.ini)
log_dir=$(awk -F " *= *" '/log_dir/ {print $2}' analyzer.ini) #configurable: directory of downloaded data
name=$(awk -F " *= *" '/name/ {print $2}' analyzer.ini)

ls $data_dir | grep -e "[0-9]\{8\}" | while read line; do [ ! -z "`grep "$line finished" $log_dir`" ] && echo $line; done
