from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура админки
btn_load = KeyboardButton('Загрузить')
btn_change = KeyboardButton('Редактировать')
btn_delete = KeyboardButton('Удалить')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
    btn_load, btn_change).add(btn_delete)

# Выбор таблицы
books = KeyboardButton('Книги📚')
courses = KeyboardButton('Курсы🗂')
select_table = ReplyKeyboardMarkup(resize_keyboard=True).row(books, courses)


# Выбор таблицы для редактирования
btn1 = InlineKeyboardButton("Книги📚", callback_data="change_books")
btn2 = InlineKeyboardButton("Курсы🗂", callback_data="change_courses")
table_for_change = InlineKeyboardMarkup(row_width=3).row(btn1, btn2)


def get_delete_kb(row):
    kb = InlineKeyboardMarkup()\
        .add(InlineKeyboardButton(f"Удалить {row[1]}", callback_data=f"del {row[1]}"))
    return kb
