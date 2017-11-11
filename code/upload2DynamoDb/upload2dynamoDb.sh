#!/bin/sh

base="/mnt/production/data"
while getopts "h?y:" opt; do
    case "$opt" in
    h|\?)
        echo "sh upload2dynamoDb.sh -y yyyy"
        exit 0
        ;;
    y)  year="$OPTARG"
        ;;
    esac
done
for i in `ls $base/$year/*`
do 
    python upload2dynamoDb.py $i nseDaily
done
