"""
Calculates the momentum score for a stock
"""
import json
import numpy as np
import math
import talib
import argparse
import datetime
import ohlc

def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def calculate_momentum_score(close, volume, timestamp,enddate, numDays,period ):

    if (period > numDays):
        msg = "ROC timeperiod ({0}) > Lookback period ({1})".format(period, numDays)
        raise Exception(msg)
    score = 0
    taclose = np.array(close, dtype=float)
    tavolume = np.array(volume, dtype=float)
    tatimestamp = np.array(timestamp, dtype=int)
    maxIndex = find_nearest(tatimestamp, int(enddate.strftime('%s')))
    minIndex = max(maxIndex - numDays, 0)
    rocp = talib.ROCP(taclose, timeperiod=period)
    rocp = [0 if math.isnan(x) else x for x in rocp.tolist()]
    rocpv = talib.ROCP(tavolume, timeperiod=period)
    rocpv = [0 if math.isnan(x) else x for x in rocpv.tolist()]
    for index in range(minIndex, maxIndex):
        #score = score + (1 + rocp[index] * rocpv[index])
        #score = score + (1 + rocp[index])
        score  = score + (1 + rocp[index] * math.pow(1.5,rocpv[index]))
    return score

def main(args):

    o = ohlc.ohlc("Daily")
    #5 days added as the date we have may not match the date we have in the DB
    e = args.enddate + datetime.timedelta(days = 5 )
    #get more number of days so that we can have date for the ROC and also account for weekends
    s = e - datetime.timedelta(days=(args.numDays * 2 + 2* args.roc + 5) )
    n = o.np(args.symbol[0], endtime = e.strftime('%s'), starttime= s.strftime('%s'))

    print "Score = ", calculate_momentum_score(n['close'], n['volume'], n['timestamp'], args.enddate, args.numDays, args.roc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate momentum score for share.')
    parser.add_argument('symbol', metavar='SYMBOL', type=str, nargs=1,
                        help='The stock symbol for NSE eg INFY.NS')
    parser.add_argument('-e', "--enddate", required=True, help="The End Date - format YYYY-MM-DD", type=valid_date)
    parser.add_argument('-n', "--numDays", required=False,
                        help="The look back period to consider for calculating score. Default value is 120 days",
                        type=int, default=120)
    parser.add_argument('-r', "--roc", required=False, help="Time period for ROC. Default value is 10", type=int,
                        default=10)
    args = parser.parse_args()
    main(args)
