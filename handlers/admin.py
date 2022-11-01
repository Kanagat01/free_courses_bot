from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from database import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
	photo = State()
	name = State()
	description = State() 
	select_table = State()

#Получаем ID текущего модератора
async def make_changes_command(message: types.Message):
	global ID
	ID = message.from_user.id
	await bot.send_message(message.from_user.id, 'Режим админа активирован', 
		reply_markup = admin_kb.button_case_admin)
	await message.delete()

#Начало диалога загрузки нового пункта меню
#@dp.message_handler(commands = 'Загрузить', state = None)
async def cm_start(message: types.Message):
	if message.from_user.id == ID:
		await FSMAdmin.photo.set()
		await message.reply('Загрузи фото')


#Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
	if message.from_user.id == ID:
		current_state = await state.get_state()
		if current_state is None:
			return
		await state.finish()
		await message.reply('Ok')


#Ловим первый ответ и пишем в словарь
#@dp.message_handler(content_types = ['photo'], state = FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['photo'] = message.photo[0].file_id
		await FSMAdmin.next()
		await message.reply('А теперь введи название')

#Ловим второй ответ
#@dp.message_handler(state = FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['name'] = message.text
		await FSMAdmin.next()
		await message.reply('Введи описание')

#Ловим третий ответ и используем полученные данные	
#@dp.message_handler(state = FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
	if message.from_user.id == ID:
		async with state.proxy() as data:
			data['description'] = message.text
	await FSMAdmin.next()
	await message.reply('Выбери куда сохранить', reply_markup = admin_kb.button_case_admin2)

#Выбираем куда сохранить
async def select_table(message: types.Message, state: FSMContext):
	await sqlite_db.sql_add_command(state, message.text)
	await state.finish()	

#******************************Команда удалить**********************************************

tableName = None

#Выбираем из какой таблицы удалить
async def delete_command(message: types.Message):
	if message.from_user.id == ID:
		await message.reply("Выберите таблицу (courses или books)")


#Выводим все данные из таблицы		
async def delete_item(message: types.Message):
	global tableName
	tableName = message.text

	read = await sqlite_db.sql_read2(tableName)
	for ret in read:
		await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}')
		await bot.send_message(message.from_user.id, text="^^^", reply_markup = \
				InlineKeyboardMarkup().add(InlineKeyboardButton(f"Удалить {ret[1]}", \
				callback_data = f"del {ret[1]}")))


#Удаляем данные
async def del_callback_run(callback_query: types.CallbackQuery):
	await sqlite_db.sql_delete_command(tableName, callback_query.data.replace("del ", ""))
	await callback_query.answer(text = f'{callback_query.data.replace("del ", "")} удалена.',
		show_alert = True)


#Регистрируем хэндлеры
def register_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(cm_start, commands = ['Загрузить'], state = None)
	dp.register_message_handler(cancel_handler, commands = 'Отмена', state = "*")
	dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), 
		state = "*")
	dp.register_message_handler(load_photo, content_types = ['photo'], state = FSMAdmin.photo)
	dp.register_message_handler(load_name, state = FSMAdmin.name)
	dp.register_message_handler(load_description, state = FSMAdmin.description)
	dp.register_message_handler(select_table, state = FSMAdmin.select_table)
	dp.register_message_handler(make_changes_command, commands = ['moderator'], 
		is_chat_admin = True)
	dp.register_callback_query_handler(del_callback_run, 
		lambda x: x.data and x.data.startswith('del '))
	dp.register_message_handler(delete_command, commands='Удалить')
	dp.register_message_handler(delete_item, Text(equals='books', ignore_case=True))
	dp.register_message_handler(delete_item, Text(equals='courses', ignore_case=True))


