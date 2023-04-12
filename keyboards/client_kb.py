from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("Книги📚")
b2 = KeyboardButton("Курсы🗂")

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.row(b1, b2)
