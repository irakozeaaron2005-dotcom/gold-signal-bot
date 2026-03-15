import telebot

TOKEN = "8774207469:AAEjAL7CyT9c25cznEd7EoECWySJ-j-UQy8"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Gold Signal Bot is running 🚀")

bot.infinity_polling()
