#!/bin/sh

year=""
stockFile="/mnt/production/config/securitiesInformation/NSE/EQUITY_L.csv"
outDir="/mnt/production/data"

while getopts "h?y:" opt; do
    case "$opt" in
    h|\?)
	echo "sh nseStockDailyDownloader.sh -y yyyy -o <output Directory>"
        exit 0
        ;;
    y)  year="$OPTARG"
        ;;
    esac
done

endDay=$(cal 12 $year | grep -v "^$" | tail -1 | awk '{print $NF}')
start=$year"0101"
end=$year"12$endDay"

mkdir -p "$outDir/$year"
stocks=$(awk '{if (NR!=1) {print}}'  $stockFile |awk -F "\"*,\"*" '{print $1}')

for i in $stocks ;
do
    echo "Fetching $i $start to $end"
    node nseStockScraper.js  --symbol=$i\.NS --startDate=$start --endDate=$end > \
              $outDir/$year/$i.json 
    sleep 5
done
