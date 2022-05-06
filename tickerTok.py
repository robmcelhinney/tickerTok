#!/usr/bin/env python

from rich.console import Console
from rich.table import Table
from rich import box
import sys, argparse, logging
import requests
import math
import time
import yaml


millnames = ['', ' thousand',' m',' b',' t']

def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


API_ENDPOINT="https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com"
fields = ["symbol", "marketState", "regularMarketPrice", "regularMarketChange", "regularMarketChangePercent", "displayName", "marketCap"]

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

    # Get a copy of the default headers that requests would use
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-agent': 'Mozilla/5.0',
            'From': 'yahoofinanceapi@example.com'  # This is another valid field
        }
    )

    url = "{}&fields={}&symbols={}".format(API_ENDPOINT, fieldParameters, symbolParameters)
    logging.debug("url: {}".format(url))
    r = requests.get(url, headers=headers)
    logging.debug("status_code: {}".format(r.status_code))

    quoteResponse = r.json()["quoteResponse"]
    error = quoteResponse["error"]
    if error:
        logging.error("WARNING ERROR!!!!")

    results = quoteResponse["result"]
    return results


def createTable(data, holdings=None):
    console = Console()

    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Ticker", width=10)
    table.add_column("Name")
    table.add_column("Price", justify="right")
    table.add_column("Percent", justify="right")
    table.add_column("Change", justify="right")
    table.add_column("Market Cap", justify="right")
    if holdings:
        table.add_column("Holdings", justify="right")
    table.add_column(":thumbs_up:/:thumbs_down:")

    totalHoldings = 0
    totalChange = 0
    totalChangePercent = 0

    for ticker in data:
        changePercent = ticker["regularMarketChangePercent"]
        change = ticker["regularMarketChange"]
        
        changePercentStr = "{:.2f}".format(changePercent)
        changeStr = "{:,.2f}".format(change)
        if changePercent > 0:
            changePercentStr = "[green3]{}%[green3]".format(changePercentStr)
            changeStr = "[green3]{}[green3]".format(changeStr)
        elif changePercent < 0:
            changePercentStr = "[red1]{}%[red1]".format(changePercentStr.replace("-", ""))
            changeStr = "[red1]{}[red1]".format(changeStr.replace("-", ""))
        
        if changePercent > 10:
            emoji = ":rocket:"
        elif changePercent < -10:
            emoji = ":pile_of_poo:"
        else:
            emoji = ":neutral_face:"
        
        marketCap = millify(ticker["marketCap"])

        logging.debug("ticker: {}".format(ticker))
        displayNameStr = ticker["symbol"]
        if "displayName" in ticker:
            displayNameStr = str(ticker["displayName"])
    
        if holdings:
            logging.debug("holdings: {}".format(holdings))
            holding = float(holdings[ticker["symbol"]])
            holdingValue = holding * float(ticker["regularMarketPrice"])
            totalHoldings += holdingValue
            logging.debug("holdingValue: {}".format(holdingValue))
            holdingRow = "{:,.2f}".format(holdingValue)

            table.add_row(
                ticker["symbol"],
                displayNameStr,
                "{:.2f}".format(ticker["regularMarketPrice"]),
                changePercentStr,
                changeStr,
                marketCap,
                holdingRow,
                emoji,
            )

            totalChange += change * holding
            totalChangePercent = (totalChange / (totalHoldings - totalChange)) * 100

            if totalChange >= 0:
                console.print("Daily Change: [green3]~${:.2f}[green3]".format(totalChange))
                console.print("Daily % Change: [green3]~{:.2f}%[green3]".format(totalChangePercent))
            else:
                console.print("Daily Change: [red1]~${:.2f}[red1]".format(totalChange))
                console.print("Daily % Change: [red1]~{:.2f}%[red1]".format(totalChangePercent))
            console.print("Daily Change Percent: ~${:.2f}".format(totalChangePercent))
            console.print("Total Holdings: [bold dodger_blue1]~${:.2f}[bold dodger_blue1]".format(totalHoldings))
        else:
            table.add_row(
                ticker["symbol"],
                displayNameStr,
                "{:.2f}".format(ticker["regularMarketPrice"]),
                changePercentStr,
                changeStr,
                marketCap,
                emoji,
            )
    console.print(table)

def refreshDataTable(watchlist, holdings):
    data = apiCall(watchlist)
    logging.debug("data: {}".format(data))
    createTable(data, holdings)

# Gather our code in a main() function
def main(args):
    logging.debug("Your Argument: {}".format(args))

    if not args.watchlist and not args.file:
        logging.error("Must give watchlists as parameter or file")
        sys.exit()

    watchlist = []
    if args.watchlist:
        watchlist = (args.watchlist).split(",")
        logging.debug("watchlist: {}".format(watchlist))

    holdings = None
    file = (args.file)
    if file:
        try:
            yamlFile = open(file)
            yamlFile = yaml.load(yamlFile, Loader=yaml.FullLoader)
            if "watchlist" in yamlFile:
                yamlWatchlist = yamlFile["watchlist"]
                watchlist = list(set(watchlist + yamlWatchlist))
            elif "holdings" in yamlFile:
                holdings = yamlFile["holdings"]
                watchlist = set(holdings.keys())
        except IOError as err:
            logging.error("Could not open file {}. Error: {}".format(file, err))
            sys.exit()
        except yaml.YAMLError as err:
            logging.error("Could not load yaml from file {}. Error: {}".format(file, err))
            sys.exit()

    watchlist = sorted(watchlist)

    if (args.interval):
        while True:
            data = apiCall(watchlist)
            logging.debug("data: {}".format(data))
            print(chr(27) + "[2J")
            createTable(data, holdings)
            time.sleep(args.interval)
    refreshDataTable(watchlist, holdings)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description = "Tracks stocks using yahoo finance api.",
            epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
            fromfile_prefix_chars = '@' )
    parser.add_argument(
            "-w"
            "--watchlist",
            dest="watchlist",
            action="store",
            help = "pass watchlist to the program. Comma separated", 
            default=None)
    parser.add_argument(
            "-f",
            "--file",
            dest="file",
            action="store",
            help="file storing watchlist (yaml)", 
            default=None)
    parser.add_argument(
            "-i",
            "--interval",
            dest="interval",
            action="store",
            type=int,
            help="interval to refresh table", 
            default=None)
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
