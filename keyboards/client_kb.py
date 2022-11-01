from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton("Книги📚")
b2 = KeyboardButton("Курсы🗂")
#b3 = KeyboardButton('Поделиться номером', request_contact = True)
#b4 = KeyboardButton('Отправить где я', request_location = True)

kb_client = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

kb_client.row(b1, b2)#.add(b3).insert(b4)