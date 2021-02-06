#!/usr/bin/env python
#

# # import modules used here -- sys is a very standard one
# import sys, argparse, logging

# # Gather our code in a main() function
# def main(args, loglevel):
#   logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

#   # TODO Replace this with your actual code.
#   print ("Hello there.")
#   logging.info("You passed an argument.")
#   logging.debug("Your Argument: %s" % args.argument)

# # Standard boilerplate to call the main() function to begin
# # the program.
# if __name__ == '__main__':
#   parser = argparse.ArgumentParser(
#                                     description = "Does a thing to some stuff.",
#                                     epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
#                                     fromfile_prefix_chars = '@' )
#   # TODO Specify your real parameters here.
#   parser.add_argument(
#                       "argument",
#                       help = "pass ARG to the program",
#                       metavar = "ARG")
#   parser.add_argument(
#                       "-v",
#                       "--verbose",
#                       help="increase output verbosity",
#                       action="store_true")
#   args = parser.parse_args()

#   # Setup logging
#   if args.verbose:
#     loglevel = logging.DEBUG
#   else:
#     loglevel = logging.INFO

#   main(args, loglevel)


from rich.console import Console
from rich.table import Table
from rich import box

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
symbols = ["BBBY", "GME", "AAPL"]

# ex = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL,NFLX"
# fulldata = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols=BBBY,GME"


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


print("URL: ", "{}&fields={}&symbols={}".format(API_ENDPOINT, fieldParameters, symbolParameters))

r = requests.get("{}&fields={}&symbols={}".format(API_ENDPOINT, fieldParameters, symbolParameters))
# r.status_code

# print("r.json(): ", r.json())

# json = {'quoteResponse': {'result': [{'language': 'en-US', 'region': 'US', 'quoteType': 'EQUITY', 'quoteSourceName': 'Delayed Quote', 'triggerable': True, 'currency': 'USD', 'exchange': 'NMS', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'gmtOffSetMilliseconds': -18000000, 'market': 'us_market', 'esgPopulated': False, 'sharesOutstanding': 121215000, 'marketCap': 3217046272, 'sourceInterval': 15, 'exchangeDataDelayedBy': 0, 'tradeable': False, 'firstTradeDateMilliseconds': 707751000000, 'priceHint': 2, 'regularMarketChange': -0.4699993, 'regularMarketChangePercent': -1.7400937, 'regularMarketTime': 1612558801, 'regularMarketPrice': 26.54, 'regularMarketPreviousClose': 27.01, 'fullExchangeName': 'NasdaqGS', 'marketState': 'CLOSED', 'displayName': 'Bed Bath & Beyond', 'symbol': 'BBBY'}, {'language': 'en-US', 'region': 'US', 'quoteType': 'EQUITY', 'quoteSourceName': 'Delayed Quote', 'triggerable': True, 'currency': 'USD', 'exchange': 'NYQ', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'gmtOffSetMilliseconds': -18000000, 'market': 'us_market', 'esgPopulated': False, 'sharesOutstanding': 69747000, 'marketCap': 4447766016, 'sourceInterval': 15, 'exchangeDataDelayedBy': 0, 'tradeable': False, 'firstTradeDateMilliseconds': 1013610600000, 'priceHint': 2, 'regularMarketChange': 10.27, 'regularMarketChangePercent': 19.196262, 'regularMarketTime': 1612558802, 'regularMarketPrice': 63.77, 'regularMarketPreviousClose': 53.5, 'fullExchangeName': 'NYSE', 'marketState': 'CLOSED', 'displayName': 'GameStop', 'symbol': 'GME'}], 'error': None}}
# json = {'quoteResponse': {'result': [{'language': 'en-US', 'region': 'US', 'quoteType': 'EQUITY', 'quoteSourceName': 'Delayed Quote', 'triggerable': True, 'currency': 'USD', 'exchange': 'NMS', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'gmtOffSetMilliseconds': -18000000, 'market': 'us_market', 'esgPopulated': False, 'sharesOutstanding': 121215000, 'marketCap': 3217046272, 'sourceInterval': 15, 'exchangeDataDelayedBy': 0, 'tradeable': False, 'firstTradeDateMilliseconds': 707751000000, 'priceHint': 2, 'regularMarketChange': -0.4699993, 'regularMarketChangePercent': -1.7400937, 'regularMarketTime': 1612558801, 'regularMarketPrice': 26.54, 'regularMarketPreviousClose': 27.01, 'fullExchangeName': 'NasdaqGS', 'marketState': 'CLOSED', 'displayName': 'Bed Bath & Beyond', 'symbol': 'BBBY'}, {'language': 'en-US', 'region': 'US', 'quoteType': 'EQUITY', 'quoteSourceName': 'Delayed Quote', 'triggerable': True, 'currency': 'USD', 'exchange': 'NYQ', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'gmtOffSetMilliseconds': -18000000, 'market': 'us_market', 'esgPopulated': False, 'sharesOutstanding': 69747000, 'marketCap': 4447766016, 'sourceInterval': 15, 'exchangeDataDelayedBy': 0, 'tradeable': False, 'firstTradeDateMilliseconds': 1013610600000, 'priceHint': 2, 'regularMarketChange': 10.27, 'regularMarketChangePercent': 19.196262, 'regularMarketTime': 1612558802, 'regularMarketPrice': 63.77, 'regularMarketPreviousClose': 53.5, 'fullExchangeName': 'NYSE', 'marketState': 'CLOSED', 'displayName': 'GameStop', 'symbol': 'GME'}], 'error': None}}

quoteResponse = r.json()["quoteResponse"]
# quoteResponse = json["quoteResponse"]
error = quoteResponse["error"]
if error:
    print("WARNING ERROR!!!!")

results = quoteResponse["result"]
# print("results: ", results)




console = Console()

table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
table.add_column("Ticker", width=6)
table.add_column("Name")
table.add_column("Price", justify="right")
table.add_column("Percent", justify="right")
table.add_column("Change", justify="right")
table.add_column("Market Cap", justify="right")
table.add_column(":thumbs_up:/:thumbs_down:")


for result in results:
    # print("result: ", result)

    changePercent = result["regularMarketChangePercent"]
    change = result["regularMarketChange"]
    
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
    
    marketCap = millify(result["marketCap"])

    table.add_row(
        result["symbol"],
        str(result["displayName"]),
        str(result["regularMarketPrice"]),
        changePercentStr,
        changeStr,
        marketCap,
        emoji
    )

console.print(table)
