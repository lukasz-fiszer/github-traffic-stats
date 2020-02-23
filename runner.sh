#!/bin/bash

save_stats_dir='save_stats/'
logs_dir=logs
utc_datetime=`date --utc +%FT%TZ`

mkdir -p $save_stats_dir
mkdir -p $logs_dir

. venv/bin/activate
python main.py | tee $logs_dir/$utc_datetime.txt
