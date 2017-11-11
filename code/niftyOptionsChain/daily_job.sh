dest="/Volumes/Public/StockExchange/data/NSE/options/"
date=`date "+%Y_%m_%d"`
#node niftyOptionsChain.js --symbol=NIFTY --expiryDate=28SEP2017 > ../data/nifty/28SEP2017/1SEP2017.json
#node niftyOptionsChain.js --symbol=LT --expiryDate=28SEP2017 > ../data/lt/28SEP2017/1SEP2017.json
for i in NIFTY LT ;
do
   fileName=$date".json"
   command="node niftyOptionsChain.js --symbol=$i --expiryDate=28SEP2017"
   echo $command
   $command > "$dest/28SEP2017/$i/$fileName"
done

