import os #um webook url aus github secrets zu laden
import requests #um webhook nachricht zu versenden
import yfinance as yf #für stock prices
from datetime import datetime, timedelta # für stock prices
import urllib.request

#####LOAD WEBHOOK URL############################################################
# os.getenv sucht im System nach einer Variable mit dem Namen 'MY_API_KEY'
WEBHOOK_URL = os.getenv('MY_DISCORD')

if WEBHOOK_URL is None:
    print("Fehler: API_KEY wurde nicht gefunden!")
else:
    print("Key erfolgreich geladen.")



###### My Stock Prices CODE  #####################################################
STOCKS = {
    "2B7K.DE": "MSCI World SRI",
    "IS3N.DE": "MSCI World EM",
    "BTC-EUR": "Bitcoin",
}

def get_period_start_price(hist, start_date):
    """Erster verfügbarer Kurs ab einem bestimmten Datum."""
    period_hist = hist[hist.index.date >= start_date]
    if not period_hist.empty:
        return period_hist["Open"].iloc[0]
    return None

def pct_change(old, new):
    if old is None:
        return "N/A"
    change = ((new - old) / old) * 100
    arrow = "▲" if change >= 0 else "▼"
    return f"{arrow} {change:+.2f}%"

def display_stock(symbol, own_name):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="380d")

    if hist.empty:
        print(f"\n{own_name} ({symbol}): Keine Daten verfügbar.")
        return

    hist.index = hist.index.tz_localize(None)

    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    current_price = hist["Close"].iloc[-1]
    week_start_price = get_period_start_price(hist, monday)
    month_start_price = get_period_start_price(hist, month_start)
    year_start_price = get_period_start_price(hist, year_start)
    lines = []
    lines.append(f"{own_name}  ({symbol})")
    lines.append(f"   »    currently:  {current_price:.2f} €")
    lines.append(f"   »    this week:     {pct_change(week_start_price, current_price)}")
    lines.append(f"   »    this month:    {pct_change(month_start_price, current_price)}")
    lines.append(f"   »    this year:     {pct_change(year_start_price, current_price)}")
    message = "\n".join(lines)
    print(message)
    return message


























message = "\n📈 My Stock Prices:::::::::::::::::::::::::::::::: \n"
for symbol, name in STOCKS.items():
    message += display_stock(symbol, name) +"\n\n"



payload = {
    "content": message
}

response = requests.post(WEBHOOK_URL, json=payload)

if response.status_code == 204:
    print("Nachricht erfolgreich gesendet!")
else:
    print(f"Fehler: {response.status_code} - {response.text}")
