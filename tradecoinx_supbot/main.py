# -*- coding: utf-8 -*-
import logging
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled

from config import *
from modules.database import *


def bot_start():
	logging.basicConfig(level=logging.INFO)
	storage = MemoryStorage()
	bot = Bot(token=bot_data["token"], parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
	dp = Dispatcher(bot, storage=storage)


	@dp.message_handler(commands=["start"])
	async def start_cmd(message: types.Message):
		if message.from_user.language_code == "ru":
			msg = f"<b>Вас приветствует служба поддержки.</b>\n\n"\
				"⚠️ Для того, чтобы наши менеджеры быстро устранили вашу проблему, Вам следует совершить следующие действия:\n\n"\
				"1️⃣  Идентифицируйте Вашу личность, сообщите пользовательский ID, представтесь.\n"\
				"2️⃣  Опишите вашу проблему как можно конкретнее.\n"\
				"3️⃣  Приложите скриншоты, которые связаны с вашей проблемой.\n\n"\
				"После того, как Вы создали заявку, ожидайте менеджера, который подключится к вашему чату и поможет Вам устранить проблему.\n\n"\
				"⌛️ Среднее время ожидания ответа от поддержки ≈ 12 рабочих часов.\n\n"\
				"С уважением, техническая поддержка."
		else:
			msg = f"<b>Welcome to the support team.</b>\n\n"\
				"⚠️ In order for our managers to quickly resolve your problem, you should take the following actions:\n\n"\
				"1️⃣  Identify your identity, provide your user ID, introduce yourself.\n"\
				"2️⃣  Describe your problem as specifically as possible.\n"\
				"3️⃣  Attach screenshots that are related to your problem.\n\n"\
				"After you have created a request, wait for a manager who will connect to your chat and help you fix the problem.\n\n"\
				"⌛️ The average waiting time for a response from support is ≈ 12 business hours.\n\n"\
				"Best regards, technical support."

		with open("src/help.png", "rb") as photo:
			await bot.send_photo(message.from_user.id, photo=photo, caption=msg)


	@dp.message_handler()
	async def on_message_handler(message: types.Message):
		msg = message.text

		if len(msg) > 20:
			await bot.send_message(log_chat_id, f"{msg}\n\nID: {message.from_user.id}\nUsername: @{message.from_user.username}")
		else:
			if message.from_user.language_code == "ru":
				msg = "❌ <b>Слишком короткое сообщение!</b>"
			else:
				msg = "❌ <b>Too short message!</b>"

			await bot.send_message(message.from_user.id, msg)


	@dp.message_handler(content_types=["photo"])
	async def get_photo(message):
		file_id = message.photo[-1].file_id

		msg = f"ID: {message.from_user.id}\n"\
			f"Username: @{message.from_user.username}"

		await bot.send_photo(log_chat_id, file_id, msg)




	executor.start_polling(dp, skip_updates=True)




if __name__ == '__main__':
	try:
		print(f"\nBot has been started! {str(datetime.datetime.now())[:-10]}\n\n")
		bot_start()
	except:
		print(f"\nBot has been started! {str(datetime.datetime.now())[:-10]}\n\n")
		bot_start()