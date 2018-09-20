import telebot
from telebot import apihelper
import time
from time import sleep
import logging
from telebot import types

list_products = ['Список товаров:', 'Кофеварка рожковая - 2000 рублей', 'Кофеварка капсульная - 1000 рублей', 
                    'Кофеварка гейзерная - 800 рублей', 'Турка(300мл) - 350 рублей',
    				'Кофе молотый(250г) - 500 рублей', '6. Кофе молотый(500г) - 950 рублей',
        	    	'Кофе в зернах(1000г) - 1300 рублей', '8. Кофе в зернах(3000г) - 3000 рублей',
        	    	'Набор топпингов(упаковка/6 шт,500мл) - 1800 рублей', 'Фильтры для кофеварки(упаковка/100 шт) - 100 рублей']
sum = 0
zakaz = []

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

apihelper.proxy = {'https': 'socks5://userproxy:password@ams3.proxy.veesecurity.com:443'}

bot = telebot.TeleBot("698272339:AAHCibs9b1dWO88v41ZtvJGPB0hHnxpBj3M")



@bot.message_handler(commands=["start"])
def start(message):
	bot.send_message(message.chat.id, "Здравствуйте, добро пожаловать в наш магазин Coffetime!\nЗдесь вы можете найти все для приготовления идеального кофе")
	markup = types.ReplyKeyboardMarkup()
	markup.row('Да', 'Нет')
	bot.send_message(message.chat.id, "Желаете что-нибудь заказать?",reply_markup = markup)

@bot.message_handler(content_types=['text'])
def check_answer(message):
	if message.text == "Да":
		order(message)

	elif message.text == "Нет":
		no(message)

def order(message):
		markup = types.ReplyKeyboardMarkup()
		markup.row('Кофеварка рожковая - 2000 рублей')
		markup.row('Кофеварка капсульная - 1000 рублей')
		markup.row('Кофеварка гейзерная - 800 рублей')
		markup.row('Турка(300мл) - 350 рублей')
		markup.row('Кофе молотый(250г) - 500 рублей')
		markup.row('Кофе молотый(500г) - 950 рублей')
		markup.row('Кофе в зернах(1000г) - 1300 рублей')
		markup.row('Кофе в зернах(3000г) - 3000 рублей')
		markup.row('Набор топпингов(упаковка/6 шт,500мл) - 1800 рублей')
		markup.row('Фильтры для кофеварки(упаковка/100 шт) - 100 рублей')
		mess = bot.send_message(message.chat.id,"Выберите товар из списка", reply_markup = markup)
		bot.register_next_step_handler(mess, next_step)

def next_step(message):
	if message.text in list_products:
		markup = types.ReplyKeyboardMarkup()
		markup.row('1','2','3','4','5','6','7','8')
		mess = bot.send_message(message.chat.id,"Какое количесвто данного товра Вы хотите заказать?", reply_markup = markup)
		zakaz.append(message.text)
		bot.register_next_step_handler(mess, next_step1)
	else:
		bot.send_message(message.chat.id, "Всего Вам доброго")

def next_step1(message):
	a = zakaz.pop()
	zakaz.append(a+" - "+message.text+"шт.")
	global sum
	sum += int(message.text)*int(a.split('- ')[1].split(' ')[0]) 
	markup = types.ReplyKeyboardMarkup()
	markup.row('Да', 'Нет')
	mess = bot.send_message(message.chat.id, "Хотите заказать что-нибудь еще?",reply_markup = markup)
	bot.register_next_step_handler(mess, next_step2)

def next_step2(message):
	if message.text == "Да":
		order(message)

	elif message.text == "Нет":
		no1(message)

def no1(message):
	markup = types.ReplyKeyboardMarkup()
	markup.row('Да', 'Нет')
	mess = bot.send_message(message.chat.id, "Хотите изменить Ваш заказ?",reply_markup = markup)
	bot.register_next_step_handler(mess, next_step3)

def next_step3(message):
	if message.text == "Да":
		markup = types.ReplyKeyboardMarkup()
		markup.row('Вид', 'Количество')
		mess = bot.send_message(message.chat.id, "Что Вы хотите изменить в заказе?",reply_markup = markup)
		bot.register_next_step_handler(mess, change)

	elif message.text == "Нет":
		no2(message)

def change(message):
	if message.text == "Вид":
		markup = types.ReplyKeyboardMarkup()
		for i in zakaz:
			markup.row(i)
		mess = bot.send_message(message.chat.id, "Выберете товар который Вы хотите заменить",reply_markup = markup)
		bot.register_next_step_handler(mess, change1)
	elif message.text == "Количество":
		bot.send_message(message.chat.id, zakaz)

def change1(message):
	zakaz.index(message.text)='HERE'
	for i in list_products:
			markup.row(i)
	mess = bot.send_message(message.chat.id, "Выберете товар на который Вы хотите заменить",reply_markup = markup)

def no2(message):
	pass



def no(message):
	bot.send_message(message.chat.id, "Всего Вам доброго")




if __name__ == '__main__':
	bot.polling(none_stop=True, timeout=123)
