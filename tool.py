import dotenv
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from data import Data
import requests


CONFIG_ENV = dotenv.dotenv_values(".env")
CONFIG = []

class KeyBoards:
    class Inline:
        pass
    class Reply:
        def __init__(self, texts: list, which: str = "main_menu") -> None:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            if which.lower() == 'main_menu':
                markup.row(texts[0], texts[1])
                markup.add(texts[2])
            self.markup = markup
        def get(self):
            return self.markup
    class Admin:
        def __init__(self) -> None:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🕹 Kanal", url="https://t.me/Algorithmg"))
            markup.add(InlineKeyboardButton("🔴 Instagram", url="https://instagram.com/azizbekdeveloper"))
            markup.add(InlineKeyboardButton("🌐 WEB", url="https://www.azizbekdev"))
            self.markup = markup
        def get(self):
            return self.markup
    class Settings:
        def __init__(self) -> None:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KeyboardButton(text="🗺 Mintaqani O'zgartirish"))
            self.markup = markup
        def get(self):
            return self.markup
class Bot:
    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
    def start(self, msg: Message) -> None:
        data = Data()
        if not data.is_exists(msg):
            data.create_and_get(msg)
            self.bot.reply_to(msg, "<b>Ro'yxatdan muvoffaqiyatli o'tdingiz!</b>", parse_mode="HTML")
        markup = KeyBoards.Reply(['☀ Bugungi', '⚙️ Sozlamalar', '🧑‍💻 Admin/Boshqa'])
        start_msg = f'''<b>👋 Assalomu alaykum. Men sizga 15 kungacha bo'lgan muddatdagi ☀ ob havo ma'lumotini topishga yordam beraman. Tanlang👇</b>'''
        self.bot.send_message(msg.from_user.id, start_msg, reply_markup=markup.get(), parse_mode='HTML')
    
    def help(self, msg: Message):
        pass

    def message(self, msg: Message):
        if msg.text == '🧑‍💻 Admin/Boshqa':
            self.bot.send_message(msg.from_user.id, f'''<b>🕹 @Algorithmg - Yangiliklardan doim xabardor bo'ling!\n\nwww.azizbekdev.com</b>''', reply_markup=KeyBoards.Admin().get(), parse_mode="HTML")
        
        elif msg.text == "☀ Bugungi":
            data  = Data()
            weather = Weather(data.region(msg))
            
            if data.region(msg):
                data = weather.get_current()
                if not data['error']:
                    self.bot.send_photo(msg.from_user.id, data['img'], caption=data['text'], parse_mode="HTML")
                else:
                    self.bot.send_message(msg.from_user.id, data['text'], parse_mode='HTML')
            
            else:
                self.bot.reply_to(msg, "<b>⚠ Siz hali mintaqa tanlamagansiz. Iltimos mintaqa nomini kiriting!\n\n Masalan: \n<i>Samarkand\nTashkent\nLondon</i></b>", parse_mode="HTML")
                data.set_command(msg, 's_reg')
        
        elif msg.text == "⚙️ Sozlamalar":
            self.bot.send_message(msg.from_user.id, "<b>Tanlang 👇!</b>", parse_mode="HTML", reply_markup=KeyBoards.Settings().get())
        
        elif msg.text == "🗺 Mintaqani O'zgartirish":
            data = Data()
            self.bot.reply_to(msg, "<b>🗺 Iltimos mintaqa nomini kiriting!</b>", parse_mode="HTML")
            data.set_command(msg, 's_reg')
        else:
            data = Data()
            data.handle(msg, self.bot, KeyBoards)

class Weather:
    def __init__(self, region: str) -> None:
        self.url_now = "https://api.weatherapi.com/v1/current.json?key={key}&q={region}&aqi=no"
        self.url_7 = "https://api.weatherapi.com/v1/forecast.json?key={key}&q={region}&days=7"
        self.url_15 = "https://api.weatherapi.com/v1/forecast.json?key={key}&q={region}&days=15"
        self.region = region
    
    def get_current(self):
        data = requests.get(self.url_now.format(key=CONFIG_ENV.get("API_KEY"), region=self.region)).json()
        if not data.get("error"):
            img_icon = requests.get('http://'+data['current']['condition']['icon'].replace('//', '')).content
            loc = f'''🌏 - {data['location']['region']}/{data['location']['country']}'''
            cel =f'''🌡 - {data['current']['temp_c']} °C'''
            wind = f'''🌬 - {data['current']['wind_mph']} MPH'''
            return {"text":f"<b>{loc}\n{cel}\n{wind}</b>", "img":img_icon, "error":False}
        else:
            return {"error":True, 'text':"<b>Mintaqa nomi xato kiritilgan iltimos SOZLAMALAR bo'limiga o'ting va mintaqa nomi to'g'ri kiritilganini tekshiring!</b>"}
    def get_7(self):
        pass

    def get_15(self):
        pass