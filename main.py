import telebot
import config
from telebot import types # кнопки
from string import Template
bot = telebot.TeleBot(config.token)
user_dict = {}

class User:
	def __init__(self, SET):
		self.SET = SET
		keys = ['fullname', 'phone', 'adress','second_phone','append','k']
		for key in keys:
			self.key = None
# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	itembtn1 = types.KeyboardButton('/Заказ')
	itembtn2 = types.KeyboardButton('/SMM')
	itembtn3 = types.KeyboardButton('/Menu')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.send_message(message.chat.id, "Здравствуйте "+str(message.from_user.first_name)+',Добро пожаловать в Adal chicken',reply_markup=markup)
@bot.message_handler(commands=['Menu'])
def send_about(message):
		bot.send_photo(message.chat.id, open("Сет.png",'rb'), timeout=1000)
		bot.send_photo(message.chat.id, open("menu.png",'rb'), timeout=1000)
		bot.send_photo(message.chat.id, open("dop.png",'rb'), timeout=1000)
		bot.send_photo(message.chat.id, open("drinks.png",'rb'), timeout=1000)
		bot.send_message(message.chat.id,"Чтобы заказать нажмите на кнопку '/Заказ'")
@bot.message_handler(commands=['SMM'])
def send_about(message):
		markup = types.InlineKeyboardMarkup()
		btn_my_site= types.InlineKeyboardButton(text='Наша инста', url='https://www.instagram.com/pasha.taraz/')
		btn_my_2= types.InlineKeyboardButton(text='Наш вацап', url='wa.me/77071887071')
		markup.add(btn_my_site,btn_my_2)
		bot.send_message(message.chat.id, "Нажми на кнопку и перейди на нашу инсту.", reply_markup = markup)
@bot.message_handler(commands=["Заказ"])
def user_reg(message):
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		#set
		itembtn1 = types.KeyboardButton('MAX🍗')
		itembtn2 = types.KeyboardButton('Mix🍗')
		itembtn3 = types.KeyboardButton('Star🍗')
		itembtn4 = types.KeyboardButton('Kids🍗')
		itembtn5 = types.KeyboardButton('Duel🍗')
		#Курочка
		itembtn6 = types.KeyboardButton('Курочка 7(1190₸)')
		itembtn7 = types.KeyboardButton('Курочка 14(2190₸)')
		#Крылышки
		itembtn8 = types.KeyboardButton('Крылышки 8(1090₸)')
		itembtn9 = types.KeyboardButton('Крылышки 16(1990₸)')
		itembtn10 = types.KeyboardButton('Крылышки 32(3790₸)')
		#Стрипсы
		itembtn11 = types.KeyboardButton('Стрипсы 7(690₸)')
		itembtn12 = types.KeyboardButton('Стрипсы 15(1390₸)')
		#ножки
		itembtn13 = types.KeyboardButton('ножки 4(1190₸)')
		itembtn14 = types.KeyboardButton('ножки 8(2390₸)')
		itembtn15 = types.KeyboardButton('ножки 16(4590₸)')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11, itembtn12, itembtn13, itembtn14, itembtn15)
		msg = bot.send_message(message.chat.id, 'выберите:', reply_markup=markup)
		bot.register_next_step_handler(msg, process_city_step)
def process_city_step(message):
	chat_id = message.chat.id
	user_dict[chat_id] = User(message.text)

	# удалить старую клавиатуру
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	itembtn1 = types.KeyboardButton('1')
	itembtn2 = types.KeyboardButton('2')
	itembtn3 = types.KeyboardButton('3')
	itembtn4 = types.KeyboardButton('4')
	markup.add(itembtn1,itembtn2,itembtn3,itembtn4)
	msg = bot.send_message(chat_id, 'Напишите количество:', reply_markup=markup)
	bot.register_next_step_handler(msg, k)
def k(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user.k = message.text
	markup = types.ReplyKeyboardRemove(selective=False)
	msg = bot.send_message(chat_id, 'Напишите адрес доставки:', reply_markup=markup)
	bot.register_next_step_handler(msg, adress)
def adress(message):
	try:
		chat_id = message.chat.id
		user = user_dict[chat_id]
		user.adress = message.text
		msg = bot.send_message(chat_id, 'Номер телефона:')
		bot.register_next_step_handler(msg, process_phone_step)
	except Exception as e:
		msg = bot.reply_to(message, 'КАТЕ !!!')
		bot.register_next_step_handler(msg, adress)
def process_phone_step(message):
	try:
		int(message.text)
		chat_id = message.chat.id
		user = user_dict[chat_id]
		user.phone = message.text

		msg = bot.send_message(chat_id, '2 Номер телефона:')
		bot.register_next_step_handler(msg, process_2phone_step)
	except Exception as e:
		msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
		bot.register_next_step_handler(msg, process_phone_step)
def process_2phone_step(message):
	try:
		int(message.text)
		chat_id = message.chat.id
		user = user_dict[chat_id]
		user.second_phone = message.text
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		itembtn1 = types.KeyboardButton('Фри 200гр')
		itembtn2 = types.KeyboardButton('Фри 300гр')
		itembtn3 = types.KeyboardButton('Фри 400гр')
		itembtn4 = types.KeyboardButton('Соус 30гр')
		itembtn5 = types.KeyboardButton('Соус 50гр')
		itembtn6 = types.KeyboardButton('не нужно')
		markup.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6)
		msg = bot.send_message(chat_id, 'Доп. меню:',reply_markup=markup)
		bot.register_next_step_handler(msg, append)
	except Exception as e:
		msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
		bot.register_next_step_handler(msg, process_2phone_step)
def append(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user.append= message.text
	msg = bot.send_message(chat_id, 'Ваше имя:')
	bot.register_next_step_handler(msg, process_yes)
def process_yes(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user.fullname= message.text

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	itembtn1 = types.KeyboardButton('Да')
	itembtn2 = types.KeyboardButton('Нет')
	markup.add(itembtn1, itembtn2)
	msg=bot.send_message(message.chat.id, "Предоставленные данные правильные:", reply_markup=markup)
	bot.register_next_step_handler(msg, group)
@bot.message_handler(content_types = ['text'])
def group(message):
	if message.text == 'Да':
		msg=bot.send_message(message.chat.id, 'ещё раз нажмите')
		bot.register_next_step_handler(msg, process_carDate_step)
	elif message.text == 'Нет':
		msg=bot.send_message(message.chat.id,"ещё раз нажмите")
		bot.register_next_step_handler(msg, user_reg)
def process_carDate_step(message):
	chat_id = message.chat.id
	user = user_dict[chat_id]
	user.yes = message.text
	markup = types.ReplyKeyboardRemove(selective=False)
		# ваша заявка "Имя пользователя"
	bot.send_message(message.chat.id, getRegData(user, 'Спасибо, Ваш заказ принят! Ожидайте звонка менеджера!.\n Ваша заявка:', message.from_user.first_name ), parse_mode="Markdown")
	bot.send_message(message.chat.id, 'Курьер приедет через 30 мин.\n/start', reply_markup=markup)
		# отправить в группу
	bot.send_message(config.chat_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")
# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
	t = Template('$title *$name* \n заказ: *$userSET* \n количество:*$k* \n доп. меню: *$append* \n имя: *$fullname* \n телефон: *$phone* \n 2 телефон: *$second_phone* \n адрес: *$adress*')

	return t.substitute({
		'title': title,
		'name': name,
		'userSET': user.SET,
		'fullname': user.fullname,
		'phone': user.phone,
		'adress': user.adress,
		'second_phone': user.second_phone,
		'append': user.append,
		'k': user.k,
	})
# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
	bot.send_message(message.chat.id, 'Помощь - /help')
	bot.send_message(message.chat.id, 'Старт - /start')
	bot.send_message(message.chat.id, 'Меню - /Menu')
	bot.send_message(message.chat.id, 'SMM - /smm')
# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)
# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
if __name__ == '__main__':
	bot.polling(none_stop=True)