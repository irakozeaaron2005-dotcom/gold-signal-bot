import telebot
import requests
import time
import threading
import statistics
from datetime import datetime

TOKEN = "8774207469:AAEjAL7CyT9c25cznEd7EoECWySJ-j-UQy8"
API_KEY = "89c3f7fe08da4f41a9877b0d05376fa9"

bot = telebot.TeleBot(TOKEN)

def get_candles():

    url = f"https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=1h&apikey={API_KEY}&outputsize=50"

    data = requests.get(url).json()

    candles = data["values"]

    closes = [float(c["close"]) for c in candles]

    highs = [float(c["high"]) for c in candles]

    lows = [float(c["low"]) for c in candles]

    return closes, highs, lows


def calculate_rsi(data, period=14):

    gains = []
    losses = []

    for i in range(1, period):

        change = data[i] - data[i-1]

        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))

    avg_gain = sum(gains)/period if gains else 0
    avg_loss = sum(losses)/period if losses else 0

    if avg_loss == 0:
        return 100

    rs = avg_gain/avg_loss

    return 100 - (100/(1+rs))


def session_filter():

    hour = datetime.utcnow().hour

    if 7 <= hour <= 16:
        return "London"

    if 13 <= hour <= 22:
        return "New York"

    return None


def detect_trend(closes):

    ma = statistics.mean(closes[-20:])

    if closes[-1] > ma:
        return "BULLISH", ma

    else:
        return "BEARISH", ma


def detect_liquidity(highs, lows):

    recent_high = max(highs[-20:])
    recent_low = min(lows[-20:])
    price = highs[-1]

    if price > recent_high:
        return "BUY"

    if price < recent_low:
        return "SELL"

    return None


def detect_volatility(closes):

    return max(closes[-10:]) - min(closes[-10:])


def generate_signal():

    session = session_filter()

    if session is None:
        return None

    closes, highs, lows = get_candles()

    price = closes[-1]

    rsi = calculate_rsi(closes)

    trend, ma = detect_trend(closes)

    liquidity = detect_liquidity(highs, lows)

    volatility = detect_volatility(closes)

    score = 0

    if trend:
        score += 25

    if liquidity:
        score += 25

    if 35 < rsi < 65:
        score += 20

    if volatility > 3:
        score += 20

    if session:
        score += 10

    if score < 70:
        return None


    if trend == "BULLISH":
        trade = "BUY"
        sl = price - 15
        tp = price + 45
    else:
        trade = "SELL"
        sl = price + 15
        tp = price - 45


    signal = f"""
📊 GOLD SIGNAL

Session: {session}

{trade} XAUUSD
Entry price: {round(price)}

SL: {round(sl)}
TP: {round(tp)}

RSI: {round(rsi)}
Trend MA: {round(ma)}

Liquidity: {liquidity}
Volatility: {round(volatility,2)}

AI Confidence: {score}%

Strategy: AI + SMC + Candle
Timeframe: 1H
"""

    return signal


@bot.message_handler(commands=['start'])
def start(message):

    chat_id = message.chat.id

    bot.reply_to(message,"Gold AI Bot Started ✅")

    def auto_signal():

        while True:

            signal = generate_signal()

            if signal:

                bot.send_message(chat_id, signal)

            time.sleep(3600)

    threading.Thread(target=auto_signal).start()


bot.infinity_polling()
