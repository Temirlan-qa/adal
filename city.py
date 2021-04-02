import telebot
import config
from telebot import types
from string import Template
bot = telebot.TeleBot(config.token)
user_dict = {}

class User:
	def __init__(self, SET):
		self.SET = SET
		keys = ['fullname', 'phone', 'adress',]
		for key in keys:
			self.key = None

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	itembtn1 = types.KeyboardButton('/Заказ')
	itembtn2 = types.KeyboardButton('/FAQ')
	itembtn3 = types.KeyboardButton('/Menu')
	markup.add(itembtn1, itembtn2, itembtn3)
	bot.send_message(message.chat.id, "Сәлеметсізбе "+str(message.from_user.first_name)+',Adal chicken-ге қош келдіңіз',reply_markup=markup)
@bot.message_handler(commands=['Menu'])
def send_about(message):
		bot.send_photo(message.chat.id, open("Сет.png",'rb'), timeout=1000)
		bot.send_photo(message.chat.id, open("menu.png",'rb'), timeout=1000)
		bot.send_message(message.chat.id,'Заказ жасау ушин "Заказ" деген жерди басыныз')
@bot.message_handler(commands=['FAQ'])
def send_about(message):
		markup = types.InlineKeyboardMarkup()
		btn_my_site= types.InlineKeyboardButton(text='Наша инста', url='https://www.instagram.com/pasha.taraz/')
		markup.add(btn_my_site)
		bot.send_message(message.chat.id, "Нажми на кнопку и перейди на нашу инсту.", reply_markup = markup)
@bot.message_handler(commands=["Заказ"])
def user_reg(message):
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		#set
		itembtn1 = types.KeyboardButton('MAX🍗')
		itembtn2 = types.KeyboardButton('Kids🍗')
		itembtn3 = types.KeyboardButton('Star🍗')
		itembtn4 = types.KeyboardButton('Mix🍗')
		itembtn5 = types.KeyboardButton('Duel🍗')
		#Курочка
		itembtn6 = types.KeyboardButton('Курочка 7(1190)')
		itembtn7 = types.KeyboardButton('Курочка 14(2190)')
		#Крылышки
		itembtn8 = types.KeyboardButton('Крылышки 8(1090)')
		itembtn9 = types.KeyboardButton('Крылышки 16(1990)')
		itembtn10 = types.KeyboardButton('Крылышки 32(3790)')
		#Стрипсы
		itembtn11 = types.KeyboardButton('Стрипсы 7(690)')
		itembtn12 = types.KeyboardButton('Стрипсы 15(1390)')
		#ножки
		itembtn13 = types.KeyboardButton('ножки 4(1190)')
		itembtn14 = types.KeyboardButton('ножки 8(2390)')
		itembtn15 = types.KeyboardButton('ножки 16(4590)')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11, itembtn12, itembtn13, itembtn14, itembtn15)
		msg = bot.send_message(message.chat.id, 'выберите:', reply_markup=markup)
		bot.register_next_step_handler(msg, process_city_step)
def process_city_step(message):
	chat_id = message.chat.id
	user_dict[chat_id] = User(message.text)

	# удалить старую клавиатуру
	markup = types.ReplyKeyboardRemove(selective=False)

	msg = bot.send_message(chat_id, 'Напишите адрес доставки:', reply_markup=markup)
	bot.register_next_step_handler(msg, adress)
def adress(message):

	chat_id = message.chat.id
	user = user_dict[chat_id]
	user.adress = message.text

	msg = bot.send_message(chat_id, 'Номер телефона:')
	bot.register_next_step_handler(msg, process_phone_step)
def process_phone_step(message):
	try:
		int(message.text)
		chat_id = message.chat.id
		user = user_dict[chat_id]
		user.phone = message.text

		msg = bot.send_message(chat_id, 'Ваше имя:')
		bot.register_next_step_handler(msg, process_carDate_step)
	except Exception as e:
		msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
		bot.register_next_step_handler(msg, process_phone_step)
def process_carDate_step(message):

	chat_id = message.chat.id
	user = user_dict[chat_id]
	user.fullname = message.text

		# ваша заявка "Имя пользователя"
	bot.send_message(chat_id, getRegData(user, 'Спасибо, Ваш заказ принят! Ожидайте звонка менеджера! Адал Чикен!.\n Ваша заявка:', message.from_user.first_name ), parse_mode="Markdown")
		# отправить в группу
	bot.send_message(config.chat_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")
def getRegData(user, title, name):
	t = Template('$title *$name* \n заказ: *$userSET* \n имя: *$fullname* \n Телефон: *$phone* \n Адрес: *$adress*')

	return t.substitute({
		'title': title,
		'name': name,
		'userSET': user.SET,
		'fullname': user.fullname,
		'phone': user.phone,
		'adress': user.adress,
	})

@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, 'Помощь - /help')

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




bot.polling(none_stop=True)