"""
Calculates the momentum score for a stock
"""
import json
import argparse
import boto3
import time
from enum import Enum
import urllib, json
import sys
sys.path.append("../common")
import ohlc
import datetime

class Period(Enum):
    Daily = 'Daily'
    Weekly = 'Weekly'
    Monthy = 'Monthly'

    def __str__(self):
        return self.value


class EodStockData(object):
    def __init__(self, symbol, start, end, period):
        self.__url = 'https://query2.finance.yahoo.com/v8/finance/chart/{}?&lang=en-IN&region=IN&period1={}&period2={}&interval={}'.format(symbol,start,end,period)


    def download(self):
        print self.__url
        response = urllib.urlopen(self.__url)
        d = json.load(response)
        return d



def main(args):

    dDbsession = boto3.Session(profile_name='personal', region_name = 'us-east-1')
    dynamodb = dDbsession.resource('dynamodb')
    table = dynamodb.Table("nse" + str(args.period[0]))

    k = ohlc.ohlc(str(args.period[0]))
    lastDate = k.last(args.symbol[0])
    firstDate = time.mktime(datetime.date(2010, 1, 1).timetuple())
    today = int(time.time())

    if lastDate is None :
        lastDate = firstDate

    p = ""
    if (str(args.period[0]) == "Daily") :
        p = "1d"

    j = EodStockData(args.symbol[0], lastDate,today, p )


    d = j.download()
    timestamp = d["chart"]["result"][0]["timestamp"]
    lowPrice = d['chart']['result'][0]['indicators']['quote'][0]['low']
    highPrice = d['chart']['result'][0]['indicators']['quote'][0]['high']
    closePrice = d['chart']['result'][0]['indicators']['quote'][0]['close']
    openPrice = d['chart']['result'][0]['indicators']['quote'][0]['open']
    adjustedClose = d['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
    unadjustedClose = d['chart']['result'][0]['indicators']['unadjclose'][0]['unadjclose']
    name = d["chart"]["result"][0]["meta"]["symbol"]
    volume = d['chart']['result'][0]['indicators']['quote'][0]['volume']

    for index in range(0, len(timestamp)):
        item ={
              "adjclose":  str(adjustedClose[index]),
              "close": str(closePrice[index]),
              "high": str(highPrice[index]),
              "low":  str(lowPrice[index]),
              "open": str(openPrice[index]),
              "symbol": name,
              "timestamp": str(timestamp[index]),
              "unadjclose": str(unadjustedClose[index]),
              "volume": str(volume[index])
        }
        #print item
        table.put_item(Item=item)
        print "Loaded :" , json.dumps(item)
        if (index % 100) == 0 :
            time.sleep(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload latest stock details to dynamoDb')
    parser.add_argument('symbol', metavar='symbol', type=str, nargs=1,
                        help='the symbol of the stock to upload')
    parser.add_argument('period', metavar='Period - Daily/weekly/monthly', type=Period, nargs=1,
                        help='Daily/Weekly/Monthly OHLC information')
    args = parser.parse_args()
    main(args)
