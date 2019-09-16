#!/bin/bash

. ../../../scripts/set_local_env.sh 


for i in $(seq -f "%02g" 1 4); do
    mysql --table -u $(echo $UTLS_DB_USER) -p$(echo $UTLS_DB_PASSWORD) -h $(echo $UTLS_DB_HOST) $(echo $UTLS_DB_NAME) <stat_query_${i}.sql > result${i}.txt
    ./mkcsv.py result${i}.txt > result${i}.csv
done

zip nanosourcer_csv.zip result*.csv

rm result*txt
