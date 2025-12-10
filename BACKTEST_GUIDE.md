# Backtest Guide - Jan 2024 to Dec 2024

This document explains how to run a backtest for the period January 2024 to December 2024 using the Blueprint Trader AI system.

## Prerequisites

To run backtests, you need:
1. OANDA API credentials (for fetching historical data)
2. Python 3.11+ installed
3. Required dependencies (pandas, numpy, requests, python-dotenv)

## OANDA API Setup

### Getting OANDA Credentials

1. Sign up for an OANDA practice account at [OANDA](https://www.oanda.com/)
2. Navigate to your account settings
3. Generate an API access token
4. Note your Account ID

### Setting Credentials

**Option 1: Environment Variables (Recommended for local development)**
```bash
export OANDA_API_KEY="your_api_key_here"
export OANDA_ACCOUNT_ID="your_account_id_here"
```

**Option 2: GitHub Secrets (For CI/CD)**
1. Go to your repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `OANDA_API_KEY`: Your OANDA API key
   - `OANDA_ACCOUNT_ID`: Your OANDA account ID

## Running the Backtest

### Method 1: Command Line (Local)

```bash
# Install dependencies
pip install pandas numpy requests python-dotenv

# Set credentials
export OANDA_API_KEY="your_api_key"
export OANDA_ACCOUNT_ID="your_account_id"

# Run the backtest
python run_backtest_2024.py
```

### Method 2: GitHub Actions

1. Ensure OANDA credentials are configured as GitHub Secrets
2. Go to Actions tab in your repository
3. Select "Run Backtest" workflow
4. Click "Run workflow"
5. Optionally specify a custom period or asset
6. Download results from the workflow artifacts

### Method 3: Discord Bot (If configured)

```
/backtest "Jan 2024 - Dec 2024"
```

For a specific asset:
```
/backtest "Jan 2024 - Dec 2024" EUR_USD
```

## Output

The backtest generates a JSON file `backtest_results_2024.json` containing:

- **Summary Statistics**
  - Total trades across all assets
  - Overall win rate
  - Total R-multiple
  - Net return percentage
  - Exit breakdown (TP1/TP2/TP3/SL hits)

- **Per-Asset Results**
  - Trade count
  - Win rate
  - Total R
  - Return percentage
  - Maximum drawdown

## Understanding the Results

### Key Metrics

| Metric | Description |
|--------|-------------|
| Total Trades | Number of trades executed during the period |
| Win Rate | Percentage of profitable trades |
| Total R | Sum of all R-multiples (risk units) |
| Avg R/Trade | Average profit per trade in R-multiples |
| Net Return | Percentage return on account |
| Max Drawdown | Largest peak-to-trough decline |

### Exit Types

- **TP1+Trail**: Price hit TP1, stop moved to breakeven, then stopped out
- **TP2**: Full TP2 hit
- **TP3**: Full TP3 hit (best outcome)
- **SL**: Stop loss hit (1R loss)

## Configured Assets

The backtest covers the following assets:

**Forex Pairs:**
EUR_USD, GBP_USD, USD_JPY, USD_CHF, USD_CAD, AUD_USD, NZD_USD,
EUR_GBP, EUR_JPY, EUR_CHF, EUR_AUD, EUR_CAD, EUR_NZD,
GBP_JPY, GBP_CHF, GBP_AUD, GBP_CAD, GBP_NZD,
AUD_JPY, AUD_CHF, AUD_CAD, AUD_NZD,
NZD_JPY, NZD_CHF, NZD_CAD, CAD_JPY, CAD_CHF, CHF_JPY

**Metals:**
XAU_USD (Gold), XAG_USD (Silver)

**Indices:**
SPX500_USD (S&P 500), NAS100_USD (NASDAQ 100)

**Crypto:**
BTC_USD (Bitcoin), ETH_USD (Ethereum)

## Strategy Parameters

The backtest uses the Blueprint confluence-based strategy with:
- Minimum 4/7 confluence (standard mode)
- Multi-timeframe analysis (Monthly, Weekly, Daily, H4)
- Risk per trade: 1% of account
- Partial profit taking (TP1, TP2, TP3)
- Trailing stop after TP1

## Troubleshooting

### "OANDA API not configured"
Ensure environment variables are set correctly:
```bash
echo $OANDA_API_KEY
echo $OANDA_ACCOUNT_ID
```

### "Network error"
Check your internet connection and verify the OANDA API URL is accessible:
```bash
curl -I https://api-fxpractice.oanda.com
```

### "No trades found"
This could mean:
- The strategy didn't generate signals in the period
- Data is not available for some assets
- The period format is incorrect (use "Jan 2024 - Dec 2024" format)

## Sample Results

When the backtest completes successfully, you'll see output like:

```
======================================================================
BLUEPRINT TRADER AI - BACKTEST
======================================================================
Period: Jan 2024 - Dec 2024
Account Size: $10,000
Risk per Trade: 1.0%
Signal Mode: standard
======================================================================

Testing 34 assets...

[ 1/34] EUR_USD... 12 trades, 58.3% WR, +4.50R
[ 2/34] GBP_USD... 8 trades, 62.5% WR, +3.20R
...

======================================================================
SUMMARY
======================================================================
...
```
