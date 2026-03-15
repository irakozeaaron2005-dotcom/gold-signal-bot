import telebot
import random
import time
import threading

TOKEN = "8774207469:AAEjAL7CyT9c25cznEd7EoECWySJ-j-UQy8"

bot = telebot.TeleBot(TOKEN)

def generate_signal():
    trade = random.choice(["BUY", "SELL"])
    entry = random.randint(2300, 2400)
    sl = entry - 10
    tp = entry + 10

    signal = f"""
📊 XAUUSD SIGNAL

{trade} XAUUSD
Entry price: {entry}
SL: {sl}
TP: {tp}
"""
    return signal

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Gold Signal Bot is running 🚀")

@bot.message_handler(commands=['signal'])
def signal(message):
    bot.reply_to(message, generate_signal())

def auto_signal():
    while True:
        signal = generate_signal()
        chat_id = YOUR_CHAT_ID
        bot.send_message(chat_id, signal)
        time.sleep(300)

threading.Thread(target=auto_signal).start()

bot.infinity_polling()
