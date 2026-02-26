#!/usr/bin/env python3
"""BTC Halving Cycle Monitor - On-chain analysis and investment signal engine.

Usage:
    python btc_monitor.py              # Full analysis (all 4 modules)
    python btc_monitor.py countdown    # Halving countdown only
    python btc_monitor.py miner        # Miner pressure only
    python btc_monitor.py cycle        # Historical cycle comparison only
    python btc_monitor.py signal       # Investment signal only (runs all modules for scoring)
"""

import json
import ssl
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# Permissive SSL context for environments with outdated certificates
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

# ============================================================
# Constants
# ============================================================
HALVING_INTERVAL = 210_000
AVG_BLOCK_TIME_MIN = 10

HALVINGS = [
    {"num": 1, "block": 210_000,  "date": "2012-11-28", "reward_after": 25,
     "price": 12.35,   "peak": 1100,   "days_to_peak": 371},
    {"num": 2, "block": 420_000,  "date": "2016-07-09", "reward_after": 12.5,
     "price": 650,     "peak": 19800,  "days_to_peak": 525},
    {"num": 3, "block": 630_000,  "date": "2020-05-11", "reward_after": 6.25,
     "price": 8600,    "peak": 69000,  "days_to_peak": 546},
    {"num": 4, "block": 840_000,  "date": "2024-04-20", "reward_after": 3.125,
     "price": 64000,   "peak": None,   "days_to_peak": None},
]

CURRENT_HALVING = HALVINGS[-1]
NEXT_HALVING_BLOCK = 1_050_000
NEXT_REWARD = 1.5625
LAST_HALVING_DATE = datetime(2024, 4, 20, tzinfo=timezone.utc)

# Approximate % gain at N days post-halving for historical cycles
HISTORICAL_GAINS = {
    # days: [(cycle_label, gain%), ...]
    100:  [("2012", 130),  ("2016", 30),   ("2020", 40)],
    200:  [("2012", 250),  ("2016", 45),   ("2020", 80)],
    300:  [("2012", 3000), ("2016", 55),   ("2020", 250)],
    400:  [("2012", 8000), ("2016", 110),  ("2020", 500)],
    500:  [("2012", 7000), ("2016", 2000), ("2020", 650)],
    546:  [("2012", 5500), ("2016", 2500), ("2020", 702)],
}


# ============================================================
# HTTP helpers (stdlib only, no dependencies)
# ============================================================
def fetch_json(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BTC-Monitor/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  [API ERROR] {url}\n             {e}", file=sys.stderr)
        return None


def fetch_text(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BTC-Monitor/1.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
            return r.read().decode().strip()
    except Exception as e:
        print(f"  [API ERROR] {url}\n             {e}", file=sys.stderr)
        return None


def hr_fmt(value_h):
    """Format hash rate to human-readable EH/s."""
    return f"{value_h / 1e18:.2f} EH/s"


# ============================================================
# Module 1: Halving Countdown
# ============================================================
def halving_countdown():
    print("=" * 60)
    print("  MODULE 1: BTC HALVING COUNTDOWN")
    print("=" * 60)

    height_str = fetch_text("https://mempool.space/api/blocks/tip/height")
    if not height_str:
        print("  ERROR: Cannot fetch current block height from mempool.space")
        return None

    current_height = int(height_str)
    blocks_remaining = NEXT_HALVING_BLOCK - current_height
    blocks_since = current_height - CURRENT_HALVING["block"]
    cycle_progress = blocks_since / HALVING_INTERVAL * 100

    minutes_left = blocks_remaining * AVG_BLOCK_TIME_MIN
    est_date = datetime.now(timezone.utc) + timedelta(minutes=minutes_left)
    days_since = (datetime.now(timezone.utc) - LAST_HALVING_DATE).days
    days_remaining = int(minutes_left / 1440)

    print(f"""
  Current Block Height:    {current_height:,}
  Next Halving Block:      {NEXT_HALVING_BLOCK:,}
  Blocks Remaining:        {blocks_remaining:,}
  Estimated Halving Date:  {est_date.strftime('%Y-%m-%d')}
  Current Block Reward:    3.125 BTC
  Next Block Reward:       {NEXT_REWARD} BTC
  Cycle Progress:          {cycle_progress:.1f}%  (block {blocks_since:,} / {HALVING_INTERVAL:,})
  Days Since Last Halving: {days_since}
  Approx Days Remaining:   {days_remaining:,}
""")

    return {
        "current_height": current_height,
        "blocks_remaining": blocks_remaining,
        "estimated_date": est_date.strftime("%Y-%m-%d"),
        "cycle_progress": cycle_progress,
        "days_since_halving": days_since,
        "days_remaining": days_remaining,
    }


# ============================================================
# Module 2: Miner Pressure (Hash Ribbon + Difficulty + Revenue)
# ============================================================
def miner_pressure():
    print("=" * 60)
    print("  MODULE 2: MINER PRESSURE ANALYSIS")
    print("=" * 60)

    # --- Hash Rate Data (6 months for 60d MA) ---
    hr_data = fetch_json("https://mempool.space/api/v1/mining/hashrate/6m")
    if not hr_data or "hashrates" not in hr_data:
        print("  ERROR: Cannot fetch hash rate data from mempool.space")
        return None

    hashrates = sorted(hr_data["hashrates"], key=lambda x: x.get("timestamp", 0))
    raw_diffs = hr_data.get("difficulty", [])
    difficulties = sorted(
        [d for d in raw_diffs if isinstance(d, dict) and "timestamp" in d],
        key=lambda x: x["timestamp"]
    )

    hr_values = [h["avgHashrate"] for h in hashrates]
    current_hr = hr_values[-1] if hr_values else 0

    # --- Moving Averages ---
    def moving_avg(data, window):
        if len(data) < window:
            return sum(data) / len(data) if data else 0
        return sum(data[-window:]) / window

    ma_30 = moving_avg(hr_values, 30)
    ma_60 = moving_avg(hr_values, 60)

    # --- Hash Ribbon ---
    ribbon_signal = "neutral"
    if ma_30 > ma_60:
        ribbon_status = "RECOVERY (30d MA > 60d MA)"
        ribbon_signal = "bullish"
    else:
        ribbon_status = "CAPITULATION (30d MA < 60d MA)"
        ribbon_signal = "bearish"

    # Detect crossover
    if len(hr_values) >= 61:
        prev_ma30 = sum(hr_values[-31:-1]) / 30
        prev_ma60 = sum(hr_values[-61:-1]) / 60
        if prev_ma30 <= prev_ma60 and ma_30 > ma_60:
            ribbon_status += "  ** BUY SIGNAL (just crossed up) **"
            ribbon_signal = "strong_bullish"
        elif prev_ma30 >= prev_ma60 and ma_30 < ma_60:
            ribbon_status += "  ** WARNING (just crossed down) **"
            ribbon_signal = "strong_bearish"

    # --- Hash Rate Trend ---
    hr_7d = ((hr_values[-1] - hr_values[-7]) / hr_values[-7] * 100) if len(hr_values) >= 7 else 0
    hr_30d = ((hr_values[-1] - hr_values[-30]) / hr_values[-30] * 100) if len(hr_values) >= 30 else 0

    # --- Difficulty Adjustments ---
    diff_trend = "UNKNOWN"
    recent_adj = []
    if difficulties:
        # Filter valid entries with timestamp
        valid_diffs = [d for d in difficulties if isinstance(d, dict) and "timestamp" in d]
        if valid_diffs:
            last5 = valid_diffs[-5:]
            recent_adj = [
                {"date": datetime.fromtimestamp(d["timestamp"], tz=timezone.utc).strftime("%Y-%m-%d"),
                 "change": d.get("difficultyChange", d.get("change", 0))}
                for d in last5
            ]
            pos = sum(1 for a in recent_adj if a["change"] > 0)
            neg = sum(1 for a in recent_adj if a["change"] < 0)
            if pos > neg:
                diff_trend = "INCREASING (miners joining network)"
            elif neg > pos:
                diff_trend = "DECREASING (miners leaving network)"
            else:
                diff_trend = "STABLE"

    # --- Miner Revenue Proxy (reward * price / hashrate) ---
    price_data = fetch_json("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    btc_price = price_data.get("bitcoin", {}).get("usd", 0) if price_data else 0
    revenue_per_eh = (3.125 * 6 * 24 * btc_price) / (current_hr / 1e18) if current_hr > 0 and btc_price > 0 else 0

    # --- Pressure Score (-4 to +4) ---
    pressure_score = 0
    if ribbon_signal == "strong_bullish":
        pressure_score += 2
    elif ribbon_signal == "bullish":
        pressure_score += 1
    elif ribbon_signal == "strong_bearish":
        pressure_score -= 2
    else:
        pressure_score -= 1

    if hr_30d > 5:
        pressure_score += 1
    elif hr_30d < -5:
        pressure_score -= 1

    if diff_trend.startswith("INCREASING"):
        pressure_score += 1
    elif diff_trend.startswith("DECREASING"):
        pressure_score -= 1

    if pressure_score >= 2:
        pressure_level = "LOW - Healthy network, miners profitable"
    elif pressure_score >= 0:
        pressure_level = "MODERATE - Watch closely"
    elif pressure_score >= -2:
        pressure_level = "HIGH - Miners under stress"
    else:
        pressure_level = "EXTREME - Miner capitulation in progress"

    # --- Output ---
    print(f"""
  Hash Rate (current):     {hr_fmt(current_hr)}
  Hash Rate 30d MA:        {hr_fmt(ma_30)}
  Hash Rate 60d MA:        {hr_fmt(ma_60)}
  7-day Change:            {hr_7d:+.2f}%
  30-day Change:           {hr_30d:+.2f}%

  Hash Ribbon:             {ribbon_status}
  Difficulty Trend:        {diff_trend}""")

    if recent_adj:
        print("  Recent Difficulty Adjustments:")
        for a in recent_adj:
            print(f"    {a['date']}: {a['change']:+.2f}%")

    if revenue_per_eh > 0:
        print(f"\n  Est. Daily Revenue/EH:   ${revenue_per_eh:,.0f}")

    print(f"\n  >>> MINER PRESSURE:      {pressure_level} (score: {pressure_score})")
    print()

    return {
        "current_hr": current_hr,
        "ma_30": ma_30,
        "ma_60": ma_60,
        "hr_7d_change": hr_7d,
        "hr_30d_change": hr_30d,
        "ribbon_signal": ribbon_signal,
        "diff_trend": diff_trend,
        "pressure_score": pressure_score,
        "pressure_level": pressure_level,
        "btc_price": btc_price,
    }


# ============================================================
# Module 3: Historical Cycle Comparison
# ============================================================
def cycle_analysis(btc_price=0):
    print("=" * 60)
    print("  MODULE 3: HISTORICAL CYCLE COMPARISON")
    print("=" * 60)

    if btc_price <= 0:
        pd = fetch_json("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        btc_price = pd.get("bitcoin", {}).get("usd", 0) if pd else 0

    halving_price = CURRENT_HALVING["price"]
    days_since = (datetime.now(timezone.utc) - LAST_HALVING_DATE).days
    gain = ((btc_price - halving_price) / halving_price * 100) if btc_price > 0 else 0

    print(f"""
  Current BTC Price:       ${btc_price:,.0f}
  Price at 4th Halving:    ${halving_price:,}
  Gain Since Halving:      {gain:+.1f}%
  Days Since Halving:      {days_since}

  Historical Halving Cycles:
  {'Cycle':<14} {'Price@Halving':<16} {'Cycle Peak':<14} {'Peak Gain':<12} {'Days to Peak':<13}
  {'-'*14} {'-'*16} {'-'*14} {'-'*12} {'-'*13}""")

    for h in HALVINGS:
        peak_str = f"${h['peak']:,}" if h["peak"] else f"${btc_price:,.0f}*"
        gain_str = f"{(h['peak']/h['price']-1)*100:,.0f}%" if h["peak"] else f"{gain:+.1f}%*"
        dtp_str = str(h["days_to_peak"]) if h["days_to_peak"] else f"{days_since}*"
        print(f"  {h['num']}{'st' if h['num']==1 else 'nd' if h['num']==2 else 'rd' if h['num']==3 else 'th'} (Block {h['block']:,})"
              f"  ${h['price']:>10,}  {peak_str:>14}  {gain_str:>10}  {dtp_str:>10}")

    print("  (* = current cycle, in progress)")

    # Benchmark vs historical average at similar day count
    closest = min(HISTORICAL_GAINS.keys(), key=lambda d: abs(d - days_since))
    benchmarks = HISTORICAL_GAINS[closest]
    avg_gain = sum(g for _, g in benchmarks) / len(benchmarks)

    print(f"\n  Benchmark at ~Day {closest} post-halving:")
    for label, g in benchmarks:
        print(f"    {label} cycle: +{g:,}%")
    print(f"    Historical avg: +{avg_gain:,.0f}%")
    print(f"    Current cycle:  {gain:+.1f}%")

    if gain < avg_gain * 0.5:
        pace = "BEHIND historical average - potential catch-up upside"
    elif gain > avg_gain * 1.5:
        pace = "AHEAD of historical average - possible overextension"
    else:
        pace = "IN LINE with historical average"
    print(f"    Assessment:     {pace}")
    print()

    return {
        "btc_price": btc_price,
        "halving_price": halving_price,
        "gain_pct": gain,
        "days_since_halving": days_since,
        "pace": pace,
    }


# ============================================================
# Module 4: Investment Signal Engine (Balanced Strategy)
# ============================================================
def investment_signal(countdown=None, miner=None, cycle=None):
    print("=" * 60)
    print("  MODULE 4: INVESTMENT SIGNAL ENGINE (Balanced)")
    print("=" * 60)

    signals = []
    score = 0.0

    # S1: Hash Ribbon
    if miner:
        rs = miner["ribbon_signal"]
        if rs == "strong_bullish":
            signals.append(("Hash Ribbon", "BUY SIGNAL (crossover up)", 2))
            score += 2
        elif rs == "bullish":
            signals.append(("Hash Ribbon", "Bullish (recovery)", 1))
            score += 1
        elif rs == "strong_bearish":
            signals.append(("Hash Ribbon", "SELL SIGNAL (crossover down)", -2))
            score -= 2
        else:
            signals.append(("Hash Ribbon", "Bearish (capitulation)", -1))
            score -= 1

    # S2: Miner Health
    if miner:
        ps = miner["pressure_score"]
        if ps >= 2:
            signals.append(("Miner Health", "Healthy network", 1))
            score += 1
        elif ps <= -2:
            signals.append(("Miner Health", "Capitulation zone", -1))
            score -= 1
        else:
            signals.append(("Miner Health", "Moderate stress", 0))

    # S3: Cycle Position
    if countdown:
        d = countdown["days_since_halving"]
        if 100 <= d <= 500:
            signals.append(("Cycle Position", f"Day {d} - PRIME zone (100-500d)", 1.5))
            score += 1.5
        elif d < 100:
            signals.append(("Cycle Position", f"Day {d} - Early accumulation", 0.5))
            score += 0.5
        elif 500 < d <= 700:
            signals.append(("Cycle Position", f"Day {d} - Late cycle, caution", -0.5))
            score -= 0.5
        else:
            signals.append(("Cycle Position", f"Day {d} - Very late / pre-bear", -1.5))
            score -= 1.5

    # S4: Price vs Historical Pace
    if cycle:
        g = cycle["gain_pct"]
        if g < 50:
            signals.append(("Price vs History", f"{g:+.1f}% - Underperforming", 1))
            score += 1
        elif 50 <= g <= 300:
            signals.append(("Price vs History", f"{g:+.1f}% - Reasonable range", 0))
        elif 300 < g <= 600:
            signals.append(("Price vs History", f"{g:+.1f}% - Approaching peak zone", -0.5))
            score -= 0.5
        else:
            signals.append(("Price vs History", f"{g:+.1f}% - Overextended", -1.5))
            score -= 1.5

    # Display
    print(f"\n  {'Indicator':<20} {'Status':<40} {'Score':<6}")
    print(f"  {'-'*20} {'-'*40} {'-'*6}")
    for name, status, s in signals:
        print(f"  {name:<20} {status:<40} {s:+.1f}")

    print(f"\n  COMPOSITE SCORE:   {score:+.1f}  (range: -7 to +6.5)")

    # --- Generate Advice ---
    price = 0
    if cycle:
        price = cycle["btc_price"]
    elif miner:
        price = miner.get("btc_price", 0)

    divider = "─" * 54
    print(f"\n  {divider}")
    print("  INVESTMENT ADVICE")
    print(f"  {divider}")

    if score >= 3.5:
        outlook = "STRONGLY BULLISH"
        spot = "Aggressive accumulation. Allocate 70-80% of planned BTC position now."
        contract_dir = "LONG"
        leverage = "5-8x"
        sl_pct, tp_pct = 0.90, 1.35
        confidence = "HIGH"
    elif score >= 1.5:
        outlook = "BULLISH"
        spot = "Steady DCA. Build position with weekly/bi-weekly buys."
        contract_dir = "LONG"
        leverage = "3-5x"
        sl_pct, tp_pct = 0.92, 1.25
        confidence = "MEDIUM-HIGH"
    elif score >= 0:
        outlook = "NEUTRAL-BULLISH"
        spot = "Light DCA. Maintain cash reserves for potential dips."
        contract_dir = "Small LONG or AVOID"
        leverage = "2-3x"
        sl_pct, tp_pct = 0.95, 1.15
        confidence = "MEDIUM"
    elif score >= -1.5:
        outlook = "NEUTRAL-BEARISH"
        spot = "HOLD only. No new buys. Consider partial profit-taking."
        contract_dir = "AVOID or small SHORT"
        leverage = "2-3x"
        sl_pct, tp_pct = 1.05, 0.88
        confidence = "LOW"
    else:
        outlook = "BEARISH"
        spot = "Reduce exposure. Take profits. Wait for Hash Ribbon buy signal."
        contract_dir = "SHORT"
        leverage = "3-5x"
        sl_pct, tp_pct = 1.08, 0.80
        confidence = "MEDIUM (bearish)"

    sl_str = f"${price * sl_pct:,.0f} ({(sl_pct-1)*100:+.0f}%)" if price else f"{(sl_pct-1)*100:+.0f}% from entry"
    tp_str = f"${price * tp_pct:,.0f} ({(tp_pct-1)*100:+.0f}%)" if price else f"{(tp_pct-1)*100:+.0f}% from entry"

    print(f"""
  Outlook:             {outlook}
  Confidence:          {confidence}

  [SPOT / DCA]
    Advice:            {spot}

  [CONTRACT / FUTURES]
    Direction:         {contract_dir}
    Leverage:          {leverage}
    Stop Loss:         {sl_str}
    Take Profit:       {tp_str}

  {divider}
  RISK MANAGEMENT
  {divider}
  - Max contract position: 10-20% of total crypto portfolio
  - Hard leverage cap: 10x (balanced strategy)
  - Max risk per trade: 2% of portfolio value
  - Always use stop-loss orders
  - Split entries: don't go all-in at one price

  {divider}
  DISCLAIMER: This is NOT financial advice. Analysis is
  based solely on on-chain metrics and historical patterns.
  Past halving cycles do NOT guarantee future results.
  Always do your own research (DYOR).
  {divider}
""")

    return {"score": score, "outlook": outlook, "confidence": confidence}


# ============================================================
# Orchestration
# ============================================================
def full_analysis():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print()
    print("#" * 60)
    print(f"#{'BTC HALVING CYCLE MONITOR':^58}#")
    print(f"#{now:^58}#")
    print("#" * 60)
    print()

    cd = halving_countdown()
    mp = miner_pressure()
    btc_price = mp["btc_price"] if mp else 0
    ca = cycle_analysis(btc_price)
    investment_signal(cd, mp, ca)


def main():
    cmds = {
        "countdown": lambda: halving_countdown(),
        "miner":     lambda: miner_pressure(),
        "cycle":     lambda: cycle_analysis(),
        "signal":    full_analysis,
        "full":      full_analysis,
    }

    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "full"

    if cmd in ("-h", "--help", "help"):
        print(__doc__)
        return

    if cmd not in cmds:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(cmds.keys())}")
        sys.exit(1)

    cmds[cmd]()


if __name__ == "__main__":
    main()
