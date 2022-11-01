from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Клавиатура админки
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')

books = KeyboardButton('books')
courses = KeyboardButton('courses')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard = True).add(button_load)\
					.add(button_delete)
					