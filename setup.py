import telebot
from telebot import types
from telebot.types import Message
import main_processor

TOKEN = '709074122:AAGUUFDahapsjQDWx1jSJ3kqnoB_sibyFsI'

bot = telebot.TeleBot(TOKEN)

USER = set()
USE_PICS = False
SEND_WORDS = False
WAITING_WORDS = False
CURRENT_WORD = None


@bot.message_handler(commands=['start'])
def send_start(message: Message):
	bot.reply_to(message, "This is test bot.")


@bot.message_handler(commands=['help'])
def send_help(message: Message):
	bot.send_message(message.chat.id, "Try to figure out by yourself!")


@bot.message_handler(commands=['add_words'])
def send_adding_words(message: Message):
	global WAITING_WORDS
	bot.send_message(message.chat.id, "Send words in format:\nword1 - translation1\nword2 - translation2\n")
	WAITING_WORDS = True


@bot.message_handler(commands=['learning'])
def handle_learning_start(message: Message):
	global SEND_WORDS
	global CURRENT_WORD

	SEND_WORDS = True
	bot.send_message(message.chat.id, "Sending words started!")
	db = main_processor.init_db()
	CURRENT_WORD = main_processor.get_word(db)
	bot.send_message(message.chat.id, CURRENT_WORD[2])


@bot.message_handler(commands=['stop'])
def handle_learning_stop(message: Message):
	global SEND_WORDS
	SEND_WORDS = False
	bot.send_message(message.chat.id, "Sending words stopped!")


@bot.message_handler(commands=['using_pics'])
def handle_using_pics(message: Message):
	bot.send_message(message.chat.id, "Try to figure out by yourself!")


@bot.message_handler(content_types=['text'])
def message_handler(message: Message):
	USER.add(message)
	global WAITING_WORDS
	global CURRENT_WORD

	if WAITING_WORDS:
		db = main_processor.init_db()
		main_processor.add_words(db, message.text.split('\n'))
		WAITING_WORDS = False
	if SEND_WORDS:
		answer = 'You are correct! {} - {}' if message.text.strip() == CURRENT_WORD[3] else 'You are wrong! {} - {}'
		bot.send_message(message.chat.id, answer.format(CURRENT_WORD[2], CURRENT_WORD[3]))
		db = main_processor.init_db()
		CURRENT_WORD = main_processor.get_word(db)

		bot.send_message(message.chat.id, CURRENT_WORD[2])


# @bot.edited_message_handler(content_types=['text'], func=lambda message: True)
# @bot.message_handler(content_types=['text'], func=lambda message: True)
# def reply_message(message: Message):
# 	if message.from_user.id not in USER:
# 		bot.send_message(message.chat.id, 'Hi, this is your first message! How are you?')
# 		USER.add(message.from_user.id)
# 	else:
# 		bot.send_message(message.chat.id, 'What has changed since the previous time?')


# @bot.inline_handler(lambda query: len(query.query) > 0)
# def query_text(query):
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(types.InlineKeyboardButton(text="Like", callback_data="data"))
#     results = []
#     single_msg = types.InlineQueryResultArticle(
#         id="1", title="Press me",
#         input_message_content=types.InputTextMessageContent(message_text="Inline message"),
#         reply_markup=keyboard
#     )
#     results.append(single_msg)
#     bot.answer_inline_query(query.id, results)


bot.polling(timeout=60)