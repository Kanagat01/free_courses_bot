import sqlite3 as sq
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp, bot

def sql_start():
	global base, cur
	base = sq.connect('courses_bot.db')
	cur = base.cursor()
	if base:
		print('База данных успешно подключена!')
	base.execute('''CREATE TABLE IF NOT EXISTS books(
					img TEXT, 
					name TEXT PRIMARY KEY, 
					description TEXT)''')

	base.execute('''CREATE TABLE IF NOT EXISTS courses(
					img TEXT, 
					name TEXT PRIMARY KEY, 
					description TEXT)''')
	base.commit()


async def sql_add_command(state, tableName):
	async with state.proxy() as data:
		cur.execute(f'INSERT INTO {tableName} VALUES (?, ?, ?)', tuple(data.values()))
		base.commit()

async def sql_read(message, tableName):
	for ret in cur.execute(f"SELECT * FROM {tableName}").fetchall():
		await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}')

async def sql_read2(tableName):
	return cur.execute(f"SELECT * FROM {tableName}").fetchall()

async def sql_delete_command(tableName, data):
	cur.execute(f"DELETE FROM {tableName} WHERE name == ?", (data,))
	base.commit()

