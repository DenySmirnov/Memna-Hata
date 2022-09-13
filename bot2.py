from ast import Try
import telebot
import sqlite3
import json
import conf
import idbot
from telebot import types
bot = idbot.key
con = sqlite3.connect("gameinfo.db", check_same_thread=False)
cur = con.cursor()

keyboard = types.InlineKeyboardMarkup()
url_button = types.InlineKeyboardButton(text="Приєднатися!", url='t.me/Memna_hata_bot?start='+str(conf.userClickID)) 
keyboard.add(url_button)

@bot.message_handler(commands=['newgame'])
def send_welcome(message):
    if conf.gameAlreadyStarted == True:
        bot.reply_to(message, "Гра вже запущена!")
    else:
        mesID = bot.send_message(message.chat.id, "Початок реєстрації!\nЩоб зайти натисніть 'Приєднатися!'", reply_markup=keyboard)
        conf.gameMessageID = mesID.id
        print(conf.gameMessageID)
        conf.gameAlreadyStarted = True
        conf.startPlayerID = message.from_user.id
        bot.delete_message(message.chat.id, conf.gameMessageID - 1)
    @bot.message_handler(commands=['crash'])
    def send_crash(message):
        if conf.gameMessageID != 0:
            if message.from_user.id == conf.startPlayerID:
                if conf.gameAlreadyStarted == True:
                    bot.reply_to(message, "Реєстрація була зупинена!")
                    bot.delete_message(message.chat.id, conf.gameMessageID)
                    conf.gameAlreadyStarted = False
                    conf.gameMessageID = 0
                    conf.startPlayerID = 0
                else:
                    bot.reply_to(message, "Гра не запущена\nНатисніть /start для запуску гри")
            else:
                bot.reply_to(message, "Ви не запускали гру, отже не можете і зупинити")
        else:
            bot.reply_to(message, "Гра не була запущена!\nЩоб запустити гру напишіть /start")
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query): #Ця хня по ідеї має хаписувати в Ліст гравців і заповнювати їх але я сам не їбу шо вона робе)))
    data = query.data
    js=json.loads(data)
    print(js)
    markup = telebot.types.InlineKeyboardMarkup()
    conf.userClickID = from_user.id
    conf.userClickName = from_user.username
    if conf.userClickName in conf.registredPlayers:
        bot.send_message(message.chat.id, "Ви вже зайшли в гру!")
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=conf.gameMessageID, text="Початок реєстрації!\nЩоб зайти натисніть 'Приєднатися!'\n\nЗареєстровані:\n" + conf.userClickName + '\n')
        conf.registredPlayers.append(conf.userClickID)
    bot.answer_callback_query(query.id, query_text, show_alert=False)
    bot.edit_message_reply_markup(query.message.chat.id,query.message.message_id,reply_markup=markup)

@bot.message_handler(commands=['help']) #Полезний Хелп знаю)
def send_welcome(message):
    bot.reply_to(message, "help")

@bot.message_handler(commands=['start'])
def register(message):
  user_username = str(message.chat.username) #Підтягую юзернейм 
  user_id = str(message.chat.id) #Підтягую айді
  check = cur.execute(f"SELECT id FROM player WHERE id = {user_id}") #Запрос ID
  if check.fetchone() == None: #Якщо ID не знайшло
    cur.execute(f"""
        INSERT INTO player VALUES
            ({user_id}, '{user_username}', 'false') 
    """) #Записати
    con.commit() 
    bot.reply_to(message, f"Вітаємо в нашому боті, @{user_username}, будьмо знайомі") 
  else: 
    bot.reply_to(message, f"З поверненням, @{user_username}") 

bot.infinity_polling()
