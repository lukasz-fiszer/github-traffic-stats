#!/bin/bash

save_stats_dir='save_stats/'
logs_dir=logs
# utc_datetime=`date --utc +%FT%TZ`

mkdir -p $save_stats_dir
mkdir -p $logs_dir

. venv/bin/activate
python main.py | tee $logs_dir/stats-temp.txt

# Use single generated timestamp so it is consistent across the whole run
utc_datetime=`sed -En 's/Current utc datetime: ([[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2}T[[:digit:]]{2}:[[:digit:]]{2}:[[:digit:]]{2}Z)/\1/p' $logs_dir/stats-temp.txt`
cp $logs_dir/stats-temp.txt $logs_dir/$utc_datetime.txt
