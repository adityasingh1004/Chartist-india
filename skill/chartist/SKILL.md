---
name: chartist-india
description: Chart and company analysis for Indian stocks (NSE/BSE), Nifty/Sensex indices, global commodities and US Treasury yields, using the open-source Chartist tool on the user's computer. Use for "analyse the chart of X", "what does the chart say about X", support/resistance, patterns, Fibonacci, or company information for an Indian listed company. Analysis only; never places orders and never gives investment advice.
---

# Chartist (India) skill

Chartist is a local, standard-library Python tool. This skill calls its command-line front end, which runs the same analysis as the web app.

## Setup (once)
1. The user clones the repository and has Python 3.10+.
2. From the repository root, the command is `python chartist/cli.py` (Windows: `py chartist\cli.py`).

## How to use it
- Chart read: `python chartist/cli.py <query>` where query is an NSE symbol (`RELIANCE`, `M&M`), a company name, an index (`"nifty bank"`, `sensex`), `SYMBOL.BO` for a BSE-only stock, or a Yahoo ticker (`BZ=F`, `^TNX`).
- Weekly read: add `--tf W`.
- Full detail for your own reasoning: add `--json` (verdict, trend, momentum, levels, patterns, Fibonacci, each signal's track record on that security).
- Company information: `--company` (NSE classification, listing, index memberships, surveillance, business profile).
- For the interactive chart, tell the user to run `run.bat` (Windows) or `./run.sh` and open http://127.0.0.1:8765.

## Rules when reporting results
1. Say it is an analysis tool and not an investment recommendation. Do not turn a reading into "buy" or "sell" advice, targets for the user to act on, or position sizes.
2. Quote the track record: each signal carries how it has behaved on that security before. When a signal "has worked AGAINST its usual meaning" or shows "too few cases", say so.
3. The `calibration` field gives the verdict's track record for this security's group (`group`, `readings`, `bull_minus_bear_x60`, `finding`). Unless `finding` is "separates", present the verdict as a description of the chart, not a forecast; even then it is a modest past edge on today's lists, not a prediction.
4. Prices come from Yahoo (unofficial, can lag). Give the data source and last bar date with any level you quote.
5. On a yield chart, "bullish" means yields rising (bond prices falling). Futures (`=F`) are front-month continuous series: roll-date jumps are not real gaps.
6. If the tool reports an error or too little history, report that plainly; do not fill gaps from memory.
