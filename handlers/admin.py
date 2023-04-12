from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from database import sqlite_db
from keyboards import admin_kb
from keyboards import kb_client
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
ID = os.getenv("ADMIN_ID")


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    select_table = State()


# Получаем ID текущего модератора
async def make_changes_command(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Режим админа активирован. Чтобы выйти /logout',
                               reply_markup=admin_kb.admin_kb)
        await message.delete()


# Начало диалога загрузки нового пункта меню
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ok')


# Ловим первый ответ и пишем в словарь
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('А теперь введи название')


# Ловим второй ответ
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')


# Ловим третий ответ и используем полученные данные
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Выберите куда сохранить', reply_markup=admin_kb.select_table)


# Сохраняем ответ
async def save_data(message: types.Message, state: FSMContext):
    await sqlite_db.sql_add_command(state, message.text)
    await state.finish()
    await message.reply('Сохранено', reply_markup=admin_kb.admin_kb)

# ******************************Команда Редактировать**********************************************


async def change_items(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите таблицу", reply_markup=admin_kb.select_table)


async def show_items(message: types.Message):
    pass

# ******************************Команда Удалить**********************************************


# Выбираем из какой таблицы удалить
async def delete_command(message: types.Message):
    if message.from_user.id == ID:
        await message.reply("Выберите таблицу", reply_markup=admin_kb.select_table)


tableName = None


# Выводим все данные из таблицы
async def delete_item(message: types.Message):
    global tableName
    tableName = message.text

    read = await sqlite_db.sql_read2(tableName)
    for row in read:
        await bot.send_photo(message.from_user.id, row[0], f'{row[1]}\nОписание: {row[2]}')
        await bot.send_message(message.from_user.id, text="^^^",
                               reply_markup=admin_kb.get_delete_kb(row))


# Удаляем данные
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(tableName, callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.',
                                show_alert=True)


# ******************************Команда выйти из режима админа**********************************************

async def logout(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы вышли из режима админа", reply_markup=kb_client)


# Регистрируем хэндлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'])
    dp.register_message_handler(
        cm_start, Text(equals='Загрузить', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True),
                                state="*")
    dp.register_message_handler(load_photo, content_types=[
                                'photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(
        load_description, state=FSMAdmin.description)
    dp.register_message_handler(save_data, state=FSMAdmin.select_table)
    dp.register_message_handler(
        change_items, Text(equals='Редактировать', ignore_case=True))
    dp.register_message_handler(delete_command, Text(
        equals='Удалить', ignore_case=True))
    dp.register_message_handler(
        delete_item, Text(equals='Книги📚', ignore_case=True))
    dp.register_message_handler(delete_item, Text(
        equals='Курсы🗂', ignore_case=True))
    dp.register_callback_query_handler(del_callback_run,
                                       lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(logout, commands='logout')
