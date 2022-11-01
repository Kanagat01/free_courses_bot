from aiogram import types, Dispatcher
from create_bot import dp

#@dp.message_handler()
async def filt(message: types.Message):
	list1 = message.text.split(' ')
	for x in list1:
		x = x.lower()
		a = open("cenz.txt", 'r', encoding = 'utf-8')
		b = a.read()
		b = b.split(', ')
		if x in b:
			await message.reply("Маты запрещены!")
			await message.delete()

def register_handlers_other(dp: Dispatcher):
	dp.register_message_handler(filt)
