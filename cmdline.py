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




API_ENDPOINT="https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com"
fields = ["symbol", "marketState", "regularMarketPrice", "regularMarketChange", "regularMarketChangePercent", "displayName"]
symbols = ["BBBY", "GME"]

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

# r = requests.get("{}&fields={}&symbols={}".format(API_ENDPOINT, fieldParameters, symbolParameters))
# r.status_code

# r.text
# # print("r.text: ", r.text)
# print("r.json(): ", r.json())

json = {'quoteResponse': {'result': [{'language': 'en-US', 'region': 'US', 'quoteType': 'EQUITY', 'quoteSourceName': 'Delayed Quote', 'triggerable': True, 'exchange': 'NMS', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'gmtOffSetMilliseconds': -18000000, 'market': 'us_market', 'esgPopulated': False, 'sourceInterval': 15, 'exchangeDataDelayedBy': 0, 'tradeable': False, 'firstTradeDateMilliseconds': 707751000000, 'priceHint': 2, 'regularMarketChange': -0.4699993, 'regularMarketChangePercent': -1.7400937, 'regularMarketTime': 1612558801, 'regularMarketPrice': 26.54, 'regularMarketPreviousClose': 27.01, 'fullExchangeName': 'NasdaqGS', 'marketState': 'CLOSED', 'symbol': 'BBBY'}, {'language': 'en-US', 'region': 'US', 'quoteType': 'EQUITY', 'quoteSourceName': 'Delayed Quote', 'triggerable': True, 'exchange': 'NYQ', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'gmtOffSetMilliseconds': -18000000, 'market': 'us_market', 'esgPopulated': False, 'sourceInterval': 15, 'exchangeDataDelayedBy': 0, 'tradeable': False, 'firstTradeDateMilliseconds': 1013610600000, 'priceHint': 2, 'regularMarketChange': 10.27, 'regularMarketChangePercent': 19.196262, 'regularMarketTime': 1612558802, 'regularMarketPrice': 63.77, 'regularMarketPreviousClose': 53.5, 'fullExchangeName': 'NYSE', 'marketState': 'CLOSED', 'symbol': 'GME'}], 'error': None}}

quoteResponse = json["quoteResponse"]
error = quoteResponse["error"]
if error:
    print("WARNING ERROR!!!!")

results = quoteResponse["result"]
print("results: ", results)




console = Console()

table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
table.add_column("Ticker", style="dim", width=12)
table.add_column("Name")
table.add_column("Price", justify="right")
table.add_column("Percent", justify="right")
table.add_column("Market Cap", justify="right")
table.add_column("Sentiment")



# table.add_row(
#     "BBBY", 
#     "Bed Bath & Beyond", 
#     "26.54", 
#     "[red]1.74%[red]", 
#     "3.22B",
#     ":smiley:"
# )

# table.add_row(
#     "GME",
#     "Gamestop",
#     "63.77",
#     "[green]19.2%[green]",
#     "4.55B",
#     ":clown_face:"
# )

for result in results:
    print("result: ", result)

    changePercent = result["regularMarketChangePercent"]
    change = result["regularMarketChange"]
    
    changePercentStr = changePercent
    if changePercent > 0:
        changePercentStr = "[green]{}[green]".format(changePercent)
    elif changePercent < 0:
        changePercentStr = "[red]{}[red]".format(changePercent)
    
    table.add_row(
        result["symbol"],
        result["displayName"],
        result["regularMarketPrice"],
        changePercent,
        result["marketCap"],
        ":clown_face:"
    )

console.print(table)
