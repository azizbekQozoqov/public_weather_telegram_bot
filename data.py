import os
import json
import secrets
from telebot.types import Message
from telebot import TeleBot

class Data:
    def __init__(self) -> None:
        self.root = './data/'
        self.ext = ".json"
        self.initial = {"id":0, "region":"", "command":''}
        self.response = {"status":0, "which":'', 'data':[]}
    
    def _all(self, as_json=False):
        all_paths = []
        for f in os.scandir(self.root):
            if f.is_file:
                all_paths.append(f.path)
        if not as_json:
            return all_paths
        else:
            data = []
            for i in all_paths:
                with open(i, 'r') as f:
                    data.append(json.loads(f.read()))
            return data
    
    
    def is_exists(self, msg):
        data = Data()._all(as_json=True)
        for i in data:
            if i["id"] == msg.from_user.id:
                return True
        return False
    
    
    def create_and_get(self, msg: Message):
        data =  Data()
        if not data.is_exists(msg):
            filename = self.root+str(msg.from_user.id)+self.ext
            d = self.initial
            d['id'] = msg.from_user.id
            with open(filename, 'w') as f:
                f.write(json.dumps(d))
            res = self.response
            res['status'] = 200
            res['which'] = 'ok'
            res['data'] = {"path":filename}
            return res
        else:
            res = self.response
            res['status'] = 400
            res['which'] = 'exists_err'
            return res
    
    
    def region(self, msg):
        if not os.path.exists(self.root+str(msg.from_user.id)+self.ext):
            res = self.response
            res['status'] = 400
            res['which'] = 'exists_err'
            return res
        else:
            with open(self.root+str(msg.from_user.id)+self.ext, 'r') as f:
                data = json.loads(f.read())
            return data['region']
    
    
    def set_region(self, msg):
        with open(self.root+str(msg.from_user.id)+self.ext, 'r') as f:
            data = json.loads(f.read())
        data['region'] = msg.text
        with open(self.root+str(msg.from_user.id)+self.ext, 'w') as f:
            f.write(json.dumps(data))
    
    
    def set_command(self, msg: Message, which: str):
        with open(self.root+str(msg.from_user.id)+self.ext, 'r') as f:
            data = json.loads(f.read())
        data['command'] = which
        with open(self.root+str(msg.from_user.id)+self.ext, 'w') as f:
            f.write(json.dumps(data))
    
    
    def handle(self, msg:Message, bot:TeleBot, keyboards):
        d = Data()
        with open(self.root+str(msg.from_user.id)+self.ext, 'r') as f:
            data = json.loads(f.read())
        if data['command'] == "s_reg":
            d.set_region(msg)
            d.clear_commands(msg)
            bot.send_message(msg.from_user.id, "<b>✅ Mintaqa muvoffaqiyatli saqlandi.</b>", parse_mode="HTML", reply_markup=keyboards.Reply(['☀ Bugungi', '⚙️ Sozlamalar', '🧑‍💻 Admin/Boshqa']).get())
    
    
    def clear_commands(self, msg:Message):
        with open(self.root+str(msg.from_user.id)+self.ext, 'r') as f:
            data = json.loads(f.read())
        data['command'] = ''
        with open(self.root+str(msg.from_user.id)+self.ext, 'w') as f:
            f.write(json.dumps(data))