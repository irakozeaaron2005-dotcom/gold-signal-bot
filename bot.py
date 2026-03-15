import telebot

TOKEN = "8774207469:AAEjAL7CyT9c25cznEd7EoECWySJ-j-UQy8"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Gold Signal Bot is running 🚀")

@bot.message_handler(commands=['signal'])
def signal(message):
    bot.reply_to(message, "📊 XAUUSD SIGNAL\nBUY 🟢\nTP: 10 pips\nSL: 5 pips")

bot.infinity_polling()
