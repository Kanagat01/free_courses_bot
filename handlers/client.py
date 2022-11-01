from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from database import sqlite_db

#@dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
	await bot.send_message(message.from_user.id, 
		"Вас приветствует бот с бесплатными курсами по программированию!",
		reply_markup = kb_client)

async def command_courses(message: types.Message):
	await bot.send_message(message.from_user.id,
		"Здесь вы можете посмотреть список доступных курсов")
	await sqlite_db.sql_read(message, "courses")

async def command_books(message: types.Message):
	await bot.send_message(message.from_user.id,
		"Здесь вы можете найти и скачать книги по программированию", 
		#reply_markup = types.ReplyKeyboardRemove()
		)
	await sqlite_db.sql_read(message, "books")


#@dp.message_handler(lambda message: 'кана' in message.text)
async def kana(message: types.Message):
	await message.reply('Красавчик ко Кана')

def register_handlers_client(dp: Dispatcher):
	dp.register_message_handler(command_start, commands = ["start", "help"])
	dp.register_message_handler(command_courses, lambda message: "Курсы🗂" in message.text)
	dp.register_message_handler(command_books, lambda message: "Книги📚" in message.text)
	dp.register_message_handler(kana, lambda message: "Кана" in message.text)



