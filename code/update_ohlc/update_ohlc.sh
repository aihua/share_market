#!/bin/sh

year=""
stockFile="/mnt/production/config/securitiesInformation/NSE/EQUITY_L.csv"

stocks=$(awk '{if (NR!=1) {print}}'  $stockFile |awk -F "\"*,\"*" '{print $1}')

for i in $stocks ;
do
    echo "Fetching $i "
    python update_ohlc.py $i\.NS Daily
    sleep 5
done
