import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr
import json
import pandas as pd
import numpy as np

PROFILE = "personal"

class ohlc(object):
    def __init__(self, period ):
        self.__tableName = "nse" + period
        self.__dbSession = boto3.Session(profile_name='personal', region_name = 'us-east-1')
        self.__dynamodb = self.__dbSession.resource('dynamodb')
        self.__table = self.__dynamodb.Table(self.__tableName)


    def json(self, symbol, starttime=None, endtime=None):
        #print "ohlc symbol = " , symbol, " starttime = ", starttime, " endtime = ", endtime
        if (starttime != None) and (endtime != None):
            condition = Key('symbol').eq(symbol) & Key('timestamp').between(starttime, endtime)
        elif (starttime == None) and (endtime != None):
            condition = Key('symbol').eq(symbol) & Key('timestamp').between(str(0),endtime)
        elif (endtime == None) and (starttime != None):
            condition = Key('symbol').eq(symbol) & Key('timestamp').between(starttime, str(0xffffffffffffffff))
        else :
            condition = Key('symbol').eq(symbol)
        response = self.__table.query(
            KeyConditionExpression=condition
        )
        return response

    def df(self, symbol, starttime=None, endtime=None):
        response = self.json(symbol,starttime,endtime)
        df = pd.DataFrame(index=np.arange(0, len(response['Items'])),
                          columns = ['volume', 'unadjclose', 'timestamp', 'high', 'low', 'adjclose', 'close','open'])
        for index in np.arange(0, len(response['Items'])):
            item = response['Items'][index]
            if item['volume'] == "None" :
                continue
            df.loc[index] = [item['volume'],item['unadjclose'], item['timestamp'], item['high'], item['low'],
                             item['adjclose'], item['close'],item['open'] ]
        return df

    def np(self, symbol, starttime=None, endtime=None):
        response = self.json(symbol,starttime,endtime)
        n = dict(
            volume=np.zeros(shape=(len(response['Items']))),
            unadjclose=np.zeros(shape=(len(response['Items']))),
            timestamp=np.zeros(shape=(len(response['Items'])), dtype=int),
            high=np.zeros(shape=(len(response['Items']))),
            low=np.zeros(shape=(len(response['Items']))),
            adjclose=np.zeros(shape=(len(response['Items']))),
            close=np.zeros(shape=(len(response['Items']))),
            open=np.zeros(shape=(len(response['Items'])))
        )
        for index in np.arange(0, len(response['Items'])):
            item = response['Items'][index]
            if item['volume'] == "None" :
                continue
            n['volume'][index] = item['volume']
            n['unadjclose'][index] = item['unadjclose']
            n['timestamp'][index] = item['timestamp']
            n['high'][index] = item['high']
            n['low'][index] = item['low']
            n['adjclose'][index] = item['adjclose']
            n['close'][index] = item['close']
            n['open'][index] = item['open']
        return n

    def put(self,symbol, volume, unadjustedclose, timestamp, high, low, adjclose, close, open):
        item = {
            "adjclose": str(adjclose),
            "close": str(close),
            "high": str(high),
            "low": str(low),
            "open": str(open),
            "symbol": symbol,
            "timestamp": str(timestamp),
            "unadjclose": str(unadjustedclose),
            "volume": str(volume)
        }
        self.__table.put_item(Item=item)
        return item

    def get(self, symbol, timestamp):
        rs = self.__table.query(KeyConditionExpression=Key('symbol').eq(symbol) & Key('timestamp').eq(timestamp) ,
                                Limit=1)
        ret = "{}"
        if (rs['Count'] > 0):
            ret = rs['Items'][0]
        return ret

    def last(self, symbol):
        rs = self.__table.query(KeyConditionExpression=Key('symbol').eq(symbol),
                                     ScanIndexForward=False,
                                     Limit=1)
        timestamp = None
        if (rs['Count'] > 0):
            timestamp = rs['Items'][0]['timestamp']
        return timestamp

    def first(self, symbol):
        rs = self.__table.query(KeyConditionExpression=Key('symbol').eq(symbol),
                                ScanIndexForward=True,
                                Limit=1)
        timestamp = rs['Items'][0]['timestamp']
        return timestamp

    def delete(self, symbol,timestamp):
        self.__table.delete_item(
            Key={
                'symbol' : symbol,
                'timestamp': timestamp
            }
        )


if __name__ == "__main__":
    k = ohlc("Daily")
    #print k.json("IFCI.NS", '1485143000', '1486093500')
    #print k.json("IFCI.NS", starttime='1485143000')
    #print k.json("IFCI.NS", endtime='1486093500')
    #print k.df("IFCI.NS")
    #print k.np("IFCI.NS")
    #print k.last("INFY.NS")
    #print k.first("INFY.NS")
    #print k.get("INFY.NS", k.last("INFY.NS"))
    print k.get("CRAP", "1")
    print k.put("CRAP", "1","1","1","1","1","1","1","1")
    print k.get("CRAP", "1")
    print k.delete("CRAP","1")
    print k.get("CRAP", "1")