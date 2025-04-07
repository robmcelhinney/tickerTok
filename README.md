# TickerTok

Deprecated as yahoo finance api no longer available

Simple command line portfolio tracker

## Description

Python script that returns table with stocks/cryptos

## Getting Started


### Executing program


```sh
> python3 tickerTok.py -f ticker.yaml 
> python3 tickerTok.py -w ETH-USD,XM,AAPL
```

To auto update use `watch`
```sh
> watch -t -c python3 tickerTok.py -f ticker.yaml
```
```sh
> watch -t -c python3 tickerTok.py -f holdings.yaml
```

## Help

Any advise for common problems or issues.
```
> python3 tickerTok.py -h
```

## License

This project is licensed under the GNU Lesser General Public License v3.0


## Acknowledgments

Using the Yahoo Finance API
