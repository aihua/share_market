

class backtest(object):
    def __init__(self, init,candleProcessor):
        self.__init = init
        self.__candleProcessor = candleProcessor

    def run(self):
        # call the init and hold the parameters

        return


def init():
    return

def processor():
    return


def main(args):

    #initialize
    b = backtest(init, processor)

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
