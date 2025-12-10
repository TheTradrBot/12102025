#!/usr/bin/env python3
"""
Backtest script for Jan 2024 - Dec 2024.
Uses OANDA API for historical data.

Usage:
    # Set environment variables first:
    export OANDA_API_KEY="your_api_key"
    export OANDA_ACCOUNT_ID="your_account_id"
    
    # Then run:
    python run_backtest_2024.py

Or run via GitHub Actions with secrets configured.
"""

import os
import sys
import json
from datetime import datetime


def check_credentials():
    """Check if OANDA API credentials are configured."""
    api_key = os.getenv("OANDA_API_KEY")
    account_id = os.getenv("OANDA_ACCOUNT_ID")
    
    if not api_key or not account_id:
        print("=" * 70)
        print("OANDA API CREDENTIALS REQUIRED")
        print("=" * 70)
        print()
        print("Please set the following environment variables:")
        print("  export OANDA_API_KEY='your_api_key'")
        print("  export OANDA_ACCOUNT_ID='your_account_id'")
        print()
        print("Or configure them as GitHub Secrets and run via GitHub Actions.")
        print("=" * 70)
        return False
    
    return True


if not check_credentials():
    sys.exit(1)

# Import after setting env vars
from backtest import run_backtest
from config import (
    FOREX_PAIRS,
    METALS,
    INDICES,
    CRYPTO_ASSETS,
    ACCOUNT_SIZE,
    RISK_PER_TRADE_PCT,
    SIGNAL_MODE,
)


def run_full_backtest():
    """Run backtest for all assets for Jan 2024 - Dec 2024."""
    period = "Jan 2024 - Dec 2024"
    
    print("=" * 70)
    print("BLUEPRINT TRADER AI - BACKTEST")
    print("=" * 70)
    print(f"Period: {period}")
    print(f"Account Size: ${ACCOUNT_SIZE:,.0f}")
    print(f"Risk per Trade: {RISK_PER_TRADE_PCT*100:.1f}%")
    print(f"Signal Mode: {SIGNAL_MODE}")
    print("=" * 70)
    print()
    
    all_assets = FOREX_PAIRS + METALS + INDICES + CRYPTO_ASSETS
    
    all_results = []
    total_trades_all = 0
    total_wins_all = 0
    total_r_all = 0.0
    
    print(f"Testing {len(all_assets)} assets...\n")
    
    for i, asset in enumerate(all_assets, 1):
        print(f"[{i:2d}/{len(all_assets)}] {asset}...", end=" ", flush=True)
        try:
            result = run_backtest(asset, period)
            
            total_trades = result.get('total_trades', 0)
            if total_trades > 0:
                win_rate = result.get('win_rate', 0)
                net_return_pct = result.get('net_return_pct', 0)
                trades = result.get('trades', [])
                total_r = sum(t.get('rr', 0) for t in trades) if trades else 0
                
                all_results.append({
                    'asset': asset,
                    'trades': total_trades,
                    'win_rate': win_rate,
                    'total_r': total_r,
                    'return_pct': net_return_pct,
                    'max_dd_pct': result.get('max_drawdown_pct', 0),
                    'tp1_hits': result.get('tp1_trail_hits', 0),
                    'tp2_hits': result.get('tp2_hits', 0),
                    'tp3_hits': result.get('tp3_hits', 0),
                    'sl_hits': result.get('sl_hits', 0),
                    'full_result': result,
                })
                
                total_trades_all += total_trades
                total_wins_all += sum(1 for t in trades if t.get('rr', 0) > 0)
                total_r_all += total_r
                
                print(f"{total_trades} trades, {win_rate:.1f}% WR, {total_r:+.2f}R")
            else:
                print("No trades")
        except Exception as e:
            print(f"ERROR: {e}")
            continue
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if not all_results:
        print("No trades found in the specified period.")
        return {}
    
    # Sort by total R
    all_results.sort(key=lambda x: x['total_r'], reverse=True)
    
    # Calculate combined metrics
    avg_win_rate = (total_wins_all / total_trades_all * 100) if total_trades_all > 0 else 0
    avg_r = total_r_all / total_trades_all if total_trades_all > 0 else 0
    total_return_pct = total_r_all * RISK_PER_TRADE_PCT * 100
    total_profit_usd = ACCOUNT_SIZE * (total_return_pct / 100)
    
    print(f"\nPeriod: {period}")
    print(f"Assets with Trades: {len(all_results)}")
    print(f"\nCombined Performance:")
    print(f"  Total Trades: {total_trades_all}")
    print(f"  Win Rate: {avg_win_rate:.1f}%")
    print(f"  Total R: {total_r_all:+.2f}R")
    print(f"  Avg R/Trade: {avg_r:+.2f}R")
    print(f"  Net Return: {total_return_pct:+.1f}% (${total_profit_usd:+,.2f})")
    
    # Exit breakdown
    total_tp1 = sum(r['tp1_hits'] for r in all_results)
    total_tp2 = sum(r['tp2_hits'] for r in all_results)
    total_tp3 = sum(r['tp3_hits'] for r in all_results)
    total_sl = sum(r['sl_hits'] for r in all_results)
    
    print(f"\nExit Breakdown:")
    print(f"  TP1+Trail: {total_tp1} ({total_tp1/total_trades_all*100:.1f}%)")
    print(f"  TP2: {total_tp2} ({total_tp2/total_trades_all*100:.1f}%)")
    print(f"  TP3: {total_tp3} ({total_tp3/total_trades_all*100:.1f}%)")
    print(f"  SL: {total_sl} ({total_sl/total_trades_all*100:.1f}%)")
    
    print(f"\nTop 10 Performers:")
    for i, res in enumerate(all_results[:10], 1):
        print(f"  {i:2d}. {res['asset']:<12} {res['trades']:3d} trades, {res['win_rate']:.1f}% WR, {res['total_r']:+.2f}R ({res['return_pct']:+.1f}%)")
    
    # Save results to JSON file
    output_data = {
        'period': period,
        'generated_at': datetime.now().isoformat(),
        'account_size': ACCOUNT_SIZE,
        'risk_per_trade_pct': RISK_PER_TRADE_PCT * 100,
        'signal_mode': SIGNAL_MODE,
        'summary': {
            'total_assets_tested': len(FOREX_PAIRS + METALS + INDICES + CRYPTO_ASSETS),
            'assets_with_trades': len(all_results),
            'total_trades': total_trades_all,
            'win_rate': avg_win_rate,
            'total_r': total_r_all,
            'avg_r_per_trade': avg_r,
            'net_return_pct': total_return_pct,
            'net_profit_usd': total_profit_usd,
            'exit_breakdown': {
                'tp1_trail': total_tp1,
                'tp2': total_tp2,
                'tp3': total_tp3,
                'sl': total_sl,
            }
        },
        'by_asset': [
            {
                'asset': r['asset'],
                'trades': r['trades'],
                'win_rate': r['win_rate'],
                'total_r': r['total_r'],
                'return_pct': r['return_pct'],
                'max_dd_pct': r['max_dd_pct'],
            }
            for r in all_results
        ]
    }
    
    with open('backtest_results_2024.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nResults saved to: backtest_results_2024.json")
    print("=" * 70)
    
    return output_data


if __name__ == "__main__":
    run_full_backtest()
