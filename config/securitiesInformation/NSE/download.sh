base='/Volumes/Public/StockExchange/data/NSE/SecuritiesInformation/'
date=`date "+%Y_%m_%d"`
mkdir "$base/$date"
cd $date
curl -O 'https://www.nseindia.com/content/equities/EQUITY_L.csv'
curl -O 'https://www.nseindia.com/content/equities/IDR_W9.csv'
curl -O 'https://www.nseindia.com/content/equities/PREF.csv'
curl -O 'https://www.nseindia.com/content/equities/DEBT.csv'
curl -O 'https://www.nseindia.com/content/equities/WARRANT.csv'
curl -O 'https://www.nseindia.com/content/equities/mf_close-end.csv'
curl -O 'https://www.nseindia.com/content/equities/eq_ilseclist.csv'
curl -O 'https://www.nseindia.com/content/equities/eq_etfseclist.csv'
curl -O 'https://www.nseindia.com/content/equities/namechange.csv'
curl -O 'https://www.nseindia.com/content/equities/symbolchange.csv'
curl -O 'https://www.nseindia.com/content/equities/delisted.csv'
curl -O 'https://www.nseindia.com/content/equities/Securities_trade.xls'
