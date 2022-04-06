from telebot import TeleBot
import tool
bot = TeleBot(tool.CONFIG_ENV.get("BOT_KEY"))
b = tool.Bot(bot)


@bot.message_handler(commands=['start'])
def start_h(msg):
    b.start(msg)

@bot.message_handler(func= lambda msg: True)
def start_h(msg):
    b.message(msg)


if __name__ == "__main__":
    bot.infinity_polling()