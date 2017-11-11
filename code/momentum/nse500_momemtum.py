"""
Calculates the momentum score for a stock
"""
import argparse
import datetime
import csv
import pandas as pd
import logging
import sys
sys.path.append("../common")
import ohlc
import momentum as m

def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def calculate_momentum_score(symbols, enddate, numDays, roc) :
    df = pd.DataFrame(columns=('symbol', 'score'))
    for sym in symbols:
        o = ohlc.ohlc("Daily")
        e = enddate + datetime.timedelta(days=7)
        s = e - datetime.timedelta(days=(numDays * 2 + 2 * roc + 5))
        print "processing sym=", sym, " e = ", e, "s = ", s
        n = o.np(sym, endtime=e.strftime('%s'), starttime=s.strftime('%s'))
        if (len(n['close']) == 0):
            continue
        score = m.calculate_momentum_score(n['close'], n['volume'], n['timestamp'], args.enddate,
                                               args.numDays, args.roc)
        df = df.append([{'symbol': sym, 'score': score}])
    df = df.sort_values('score', ascending=False)
    return df

def main(args):
    symbols = []
    with open(args.filename[0]) as file_obj:
        reader = csv.DictReader(file_obj, delimiter=',')
        for line in reader:
            symbols.append(line['Symbol'] + ".NS")

    df = calculate_momentum_score(symbols, args.enddate, args.numDays, args.roc)
    df.to_csv("momentum.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate momentum score for share.')
    parser.add_argument('filename', metavar='FILENAME.csv', type=str, nargs=1,
                        help='the file containing the stocks to consider')
    parser.add_argument('-s', "--startdate", required=False, help="The Start Date - format YYYY-MM-DD", type=valid_date)
    parser.add_argument('-e', "--enddate", required=True, help="The End Date - format YYYY-MM-DD", type=valid_date)
    parser.add_argument('-n', "--numDays", required=False,
                        help="The look back period to consider for calculating score. Default value is 120 days",
                        type=int, default=120)
    parser.add_argument('-r', "--roc", required=False, help="Time period for ROC. Default value is 10", type=int,
                        default=10)
    args = parser.parse_args()
    main(args)
