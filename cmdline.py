#!/usr/bin/env python

from rich.console import Console
from rich.table import Table
from rich import box

import sys, argparse, logging

import requests
import json
import math


millnames = ['', ' thousand',' m',' b',' t']

def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


API_ENDPOINT="https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com"
fields = ["symbol", "marketState", "regularMarketPrice", "regularMarketChange", "regularMarketChangePercent", "displayName", "marketCap"]
# symbols = ["BBBY", "GME", "AAPL"]

# ex = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL,NFLX"
# fulldata = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols=BBBY,GME"


def apiCall(symbols):
    fieldParameters = ""
    for i in range(0, len(fields)):
        fieldParameters += fields[i]
        if i != len(fields) - 1:
            fieldParameters += ","

    symbolParameters = ""
    for i in range(0, len(symbols)):
        symbolParameters += symbols[i]
        if i != len(symbols) - 1:
            symbolParameters += ","


    # print("URL: ", "{}&fields={}&symbols={}".format(API_ENDPOINT, fieldParameters, symbolParameters))

    r = requests.get("{}&fields={}&symbols={}".format(API_ENDPOINT, fieldParameters, symbolParameters))
    # r.status_code

    quoteResponse = r.json()["quoteResponse"]
    # quoteResponse = json["quoteResponse"]
    error = quoteResponse["error"]
    if error:
        logging.error("WARNING ERROR!!!!")

    results = quoteResponse["result"]
    # print("results: ", results)
    return results



def createTable(data):
    console = Console()

    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Ticker", width=10)
    table.add_column("Name")
    table.add_column("Price", justify="right")
    table.add_column("Percent", justify="right")
    table.add_column("Change", justify="right")
    table.add_column("Market Cap", justify="right")
    table.add_column(":thumbs_up:/:thumbs_down:")


    for ticker in data:
        # print("ticker: ", ticker)

        changePercent = ticker["regularMarketChangePercent"]
        change = ticker["regularMarketChange"]
        
        changePercentStr = "{:.2f}".format(changePercent)
        changeStr = "{:.2f}".format(change)
        if changePercent > 0:
            changePercentStr = "[green3]{}%[green3]".format(changePercentStr)
            changeStr = "[green3]{}[green3]".format(changeStr)
        elif changePercent < 0:
            changePercentStr = "[red1]{}%[red1]".format(changePercentStr.replace("-", ""))
            changeStr = "[red1]{}[red1]".format(changeStr.replace("-", ""))
        
        emoji = ""
        if changePercent > 10:
            emoji = ":rocket:"
        elif changePercent < -10:
            emoji = ":pile_of_poo:"
        else:
            emoji = ":neutral_face:"
        
        marketCap = millify(ticker["marketCap"])

        # logging.debug("ticker: %s" % ticker)

        displayNameStr = ticker["symbol"]
        if "displayName" in ticker:
            displayNameStr = str(ticker["displayName"])

        table.add_row(
            ticker["symbol"],
            displayNameStr,
            str(ticker["regularMarketPrice"]),
            changePercentStr,
            changeStr,
            marketCap,
            emoji
        )

    console.print(table)

# Gather our code in a main() function
def main(args):
    logging.debug("Your Argument: %s" % args)

    watchlist = (args.watchlist).split(",")
    logging.debug("watchlist: %s" % watchlist)

    # interval = (args.interval)

    data = apiCall(watchlist)
    # logging.debug("data: %s" % data)
    createTable(data)





# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                    description = "Tracks stocks using yahoo finance api.",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )
    # TODO Specify your real parameters here.
    parser.add_argument(
            "-w"
            "--watchlist",
            dest="watchlist",
            action="store",
            help = "pass watchlist to the program. Comma separated", 
            default="GME")
    # parser.add_argument(
    #         "-i",
    #         "--interval",
    #         help="refresh interval in seconds",
    #         action="store", 
    #         type=int,
    #         default=None)
    parser.add_argument(
            "-v",
            "--verbose",
            help="increase output verbosity",
            action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    main(args)
