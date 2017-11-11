"""
Calculates the momentum score for a stock
"""
import json
import argparse
import boto3
import time


def main(args):

    #open json file and setup the data frame
    with open(args.filename[0]) as json_data:
        d = json.load(json_data)
        timestamp = d["chart"]["result"][0]["timestamp"]
        lowPrice = d['chart']['result'][0]['indicators']['quote'][0]['low']
        highPrice = d['chart']['result'][0]['indicators']['quote'][0]['high']
        closePrice = d['chart']['result'][0]['indicators']['quote'][0]['close']
        openPrice = d['chart']['result'][0]['indicators']['quote'][0]['open']
        adjustedClose = d['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
        unadjustedClose = d['chart']['result'][0]['indicators']['unadjclose'][0]['unadjclose']
        name = d["chart"]["result"][0]["meta"]["symbol"]
        volume = d['chart']['result'][0]['indicators']['quote'][0]['volume']

    dDbsession = boto3.Session(profile_name='personal', region_name = 'us-east-1')
    dynamodb = dDbsession.resource('dynamodb')
    table = dynamodb.Table(args.tableName[0])

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
        table.put_item(Item=item)
        print "Loaded :" , json.dumps(item)
        if (index % 10) == 0 :
            time.sleep(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload stock details to dynamoDb')
    parser.add_argument('filename', metavar='FILENAME.json', type=str, nargs=1,
                        help='the file containing the stock OHLC information in json')
    parser.add_argument('tableName', metavar='Table Name', type=str, nargs=1,
                        help='The table name to to add the OHLC information')
    args = parser.parse_args()
    main(args)
