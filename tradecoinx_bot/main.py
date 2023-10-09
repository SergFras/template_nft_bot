# -*- coding: utf-8 -*-
import logging
import datetime
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled

from config import *
from modules.database import *
from nft_menu import *


def bot_start():
	logging.basicConfig(level=logging.INFO)
	storage = MemoryStorage()
	bot = Bot(token=bot_data["token"], parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
	dp = Dispatcher(bot, storage=storage)


	@dp.message_handler(commands=["start"])
	async def start_cmd(message: types.Message):
		if getUserStat(message.from_user.id) == None:
			regUser(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)

			if message.from_user.language_code == "ru":
				key1 = types.InlineKeyboardButton("✅ Принять правила", callback_data='lisence_callback')
				keyboard = types.InlineKeyboardMarkup().add(key1)

				msg = f"<b>👋 Привет, {message.from_user.first_name}!</b>\n\n"\
					f'<a href="https://telegra.ph/Polzovatelskoe-soglashenie-TradeCoinX-09-07">Политика и условия пользования данным ботом.</a>\n\n'\
					f"Спасибо за понимание, Ваш «{bot_data['bot_name']}»"
			else:
				key1 = types.InlineKeyboardButton("✅ Accept the rules", callback_data='lisence_callback')
				keyboard = types.InlineKeyboardMarkup().add(key1)

				msg = f"<b>👋 Hello, {message.from_user.first_name}!</b>\n\n"\
					f'<a href="https://telegra.ph/Polzovatelskoe-soglashenie-TradeCoinX-09-07">Policy and terms of use of this bot.</a>\n\n'\
					f"Thanks for your understanding, Your «{bot_data['bot_name']}»"

			await bot.send_message(message.from_user.id, msg, reply_markup=keyboard)
		else:
			if getUserStat(message.from_user.id)[6] == "ru":
				msg = f"<b>Приветствую, {message.from_user.first_name}!</b>\n\n"\
					"Это телеграм бот - торговая площадка для невзаимозаменяемых токенов (NFT). Покупайте, продавайте и открывайте для себя эксклюзивные цифровые предметы."
			else:
				msg = f"<b>Hello, {message.from_user.first_name}!</b>\n\n"\
					"This is a telegram bot - a trading platform for non-fungible tokens (NFT). Buy, sell and discover exclusive digital items."

			await bot.send_message(message.from_user.id, msg)


			if getUserStat(message.from_user.id)[6] == "ru":
				msg = f"<b>Используя сервисы проекта вы соглашаетесь с\nпользовательским соглашением\n"\
					f"Узнайте о других продуктах {bot_data['bot_name']}</b>"
			else:
				msg = f"<b>By using the project services you agree to the user agreement\n"\
					f"Learn about other products {bot_data['bot_name']}</b>"

			await bot.send_message(message.from_user.id, msg)


	@dp.message_handler(commands=["give"])
	async def give_cmd(message: types.Message):
		if (getUserStat(message.from_user.id) != None) and (message.from_user.id in admins):
			args = str(message.text).split()

			if len(args) != 3:
				await bot.send_message(message.from_user.id, f"Аргументы для команды указаны неверно! <code>/give id amount</code>")
			else:
				updateUinput(int(args[1]), int(args[2]))

				await bot.send_message(message.from_user.id, f"Реферальные деньги <i>({args[2]})</i> были успешно выданы пользователю <code>{args[1]}</code>\n\n<i>admin id: {message.from_user.id}</i>")


	@dp.message_handler()
	async def on_message_handler(message: types.Message):
		msg = message.text.lower()

		if (msg == "users") or (msg == "/users"):
			if message.from_user.id in admins:
				await bot.send_message(message.from_user.id, len(getAllStat()))

		if (msg == "личный кабинет 📁") or (msg == "personal account 📁"):
			await lk_menu(bot, message)

		if (msg == "тех. поддержка 🌐") or (msg == "tech. support 🌐"):
			await help_target(bot, message)

		if (msg == "инфо ℹ️") or (msg == "info ℹ️"):
			await info_target(bot, message)


	@dp.callback_query_handler(lambda c: c.data == 'lisence_callback')
	async def lisence_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

		key1 = types.InlineKeyboardButton("Русский 🇷🇺", callback_data='ru_callback')
		key2 = types.InlineKeyboardButton("English 🇬🇧", callback_data='en_callback')
		keyboard = types.InlineKeyboardMarkup().add(key1, key2)

		if callback_query.from_user.language_code == "ru":
			await bot.send_message(callback_query.from_user.id, "🌎 Выберите язык:", reply_markup=keyboard)
		else:
			await bot.send_message(callback_query.from_user.id, "🌎 Select language:", reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'ru_callback')
	async def ru_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

		updateUlang(callback_query.from_user.id, "ru")

		key1 = types.InlineKeyboardButton("RUB 🇷🇺", callback_data='ru_money_callback')
		key2 = types.InlineKeyboardButton("UAH 🇺🇦", callback_data='ua_money_callback')
		key3 = types.InlineKeyboardButton("USD 🇺🇸", callback_data='usa_money_callback')
		keyboard = types.InlineKeyboardMarkup().add(key1, key2, key3)

		await bot.send_message(callback_query.from_user.id, "💸 Выберите валюту:", reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'en_callback')
	async def en_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

		updateUlang(callback_query.from_user.id, "en")

		key1 = types.InlineKeyboardButton("RUB 🇷🇺", callback_data='ru_money_callback')
		key2 = types.InlineKeyboardButton("UAH 🇺🇦", callback_data='ua_money_callback')
		key3 = types.InlineKeyboardButton("USD 🇺🇸", callback_data='usa_money_callback')
		keyboard = types.InlineKeyboardMarkup().add(key1, key2, key3)

		await bot.send_message(callback_query.from_user.id, "💸 Select currency:", reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'ru_money_callback')
	async def ru_money_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

		updateUcurrency(callback_query.from_user.id, "RUB")

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			keyboard.row("Личный кабинет 📁")
			keyboard.row("Инфо ℹ️", "Тех. Поддержка 🌐")

			await bot.send_message(callback_query.from_user.id, "<b>Используй клавиатуру ниже для удобства!</b>", reply_markup=keyboard)
		else:
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			keyboard.row("Personal account 📁")
			keyboard.row("Info ℹ️", "Tech. support 🌐")

			await bot.send_message(callback_query.from_user.id, "<b>Use the keyboard below for convenience!</b>", reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'ua_money_callback')
	async def ua_money_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

		updateUcurrency(callback_query.from_user.id, "UAH")

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			keyboard.row("Личный кабинет 📁")
			keyboard.row("Инфо ℹ️", "Тех. Поддержка 🌐")

			await bot.send_message(callback_query.from_user.id, "<b>Используй клавиатуру ниже для удобства!</b>", reply_markup=keyboard)
		else:
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			keyboard.row("Personal account 📁")
			keyboard.row("Info ℹ️", "Tech. support 🌐")

			await bot.send_message(callback_query.from_user.id, "<b>Use the keyboard below for convenience!</b>", reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'usa_money_callback')
	async def usa_money_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

		updateUcurrency(callback_query.from_user.id, "USD")

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			keyboard.row("Личный кабинет 📁")
			keyboard.row("Инфо ℹ️", "Тех. Поддержка 🌐")

			await bot.send_message(callback_query.from_user.id, "<b>Используй клавиатуру ниже для удобства!</b>", reply_markup=keyboard)
		else:
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			keyboard.row("Personal account 📁")
			keyboard.row("Info ℹ️", "Tech. support 🌐")

			await bot.send_message(callback_query.from_user.id, "<b>Use the keyboard below for convenience!</b>", reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'input_callback')
	async def input_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			buttons = [
				[types.InlineKeyboardButton("🪙 Пополнить криптовалютой", callback_data='input_crypto_callback')],
				[types.InlineKeyboardButton("💸 Сбербанк", callback_data='input_sberbank_callback')],
				[types.InlineKeyboardButton("💸 Тинькофф", callback_data='input_tinkoff_callback')],
				[types.InlineKeyboardButton("💸 Альфа Банк", callback_data='input_aplha_callback')],
				[types.InlineKeyboardButton("💸 СБП", callback_data='input_sbp_callback')],
				[types.InlineKeyboardButton("💸 Visa/Mastercard", callback_data='input_visa_mastercard_callback')]
			]

			keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

			msg = "<b>💎 Пополнение</b>"
		else:
			buttons = [
				[types.InlineKeyboardButton("🪙 Top up with cryptocurrency", callback_data='input_crypto_callback')],
				[types.InlineKeyboardButton("💸 Sberbank", callback_data='input_sberbank_callback')],
				[types.InlineKeyboardButton("💸 Tinkoff", callback_data='input_tinkoff_callback')],
				[types.InlineKeyboardButton("💸 Aplha Bank", callback_data='input_aplha_callback')],
				[types.InlineKeyboardButton("💸 SBP", callback_data='input_sbp_callback')],
				[types.InlineKeyboardButton("💸 Visa/Mastercard", callback_data='input_visa_mastercard_callback')]
			]

			keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

			msg = "<b>💎 Replenishment</b>"


		with open("src/input.png", "rb") as photo:
			await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'input_crypto_callback')
	async def input_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			key1 = types.InlineKeyboardButton("✅ Оплатил", callback_data='input_crypto_target_callback')
			keyboard = types.InlineKeyboardMarkup().add(key1)

			msg = f"💎 Сделайте перевод на этот кошелёк в <b>USDT</b>\n\n<code>{crypto_payments[random.randint(0, 2)]}</code>\n\n"\
				"⚠️ Уважаемый пользователь, обращаем ваше внимание, что все вводы меньше 1000 RUB | 400 UAH  | 10 USD зачисляться в сервис не будут, возмещение по данным транзакциям так же не предусмотрено."
		else:
			key1 = types.InlineKeyboardButton("✅ Paid", callback_data='input_crypto_target_callback')
			keyboard = types.InlineKeyboardMarkup().add(key1)

			msg = f"💎 Make a transfer to this wallet in <b>USDT</b>\n\n<code>{crypto_payments[random.randint(0, 2)]}</code>\n\n"\
				"⚠️ Dear user, please note that all inputs less than 1000 RUB | 400 UAH | 10 USD will not be credited to the service, compensation for these transactions is also not provided."


		await bot.send_message(callback_query.from_user.id, msg, reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'input_sberbank_callback')
	async def input_sberbank_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await payment(bot, callback_query, bank_payments["sberbank"])


	@dp.callback_query_handler(lambda c: c.data == 'input_tinkoff_callback')
	async def input_tinkoff_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await payment(bot, callback_query, bank_payments["tinkoff"])


	@dp.callback_query_handler(lambda c: c.data == 'input_aplha_callback')
	async def input_aplha_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await payment(bot, callback_query, bank_payments["aplha"])


	@dp.callback_query_handler(lambda c: c.data == 'input_sbp_callback')
	async def input_sbp_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await payment(bot, callback_query, bank_payments["sbp"])


	@dp.callback_query_handler(lambda c: c.data == 'input_visa_mastercard_callback')
	async def input_visa_mastercard_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await payment(bot, callback_query, bank_payments["visa_mastercard"])


	@dp.callback_query_handler(lambda c: c.data == 'input_crypto_target_callback')
	async def input_crypto_target_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			msg = f"💎 <b>Стандартное ожидание подтверждения транзакции варьируется от 15 до 60 минут.</b>\n\n"\
				"⚠️ Не паникуйте, если средства не пришли в течение часа – при высокой загрузке блокчейна операция может занимать даже два часа."
		else:
			msg = f"💎 <b>The standard waiting time for transaction confirmation varies from 15 to 60 minutes.</b>\n\n"\
				"⚠️ Don’t panic if the funds haven’t arrived within an hour – when the blockchain is busy, the transaction can even take two hours."


		await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'output_callback')
	async def output_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			key1 = types.InlineKeyboardButton("Поддержка 👩‍💻", url='https://t.me/tradecoinx_supbot')
			keyboard = types.InlineKeyboardMarkup().add(key1)

			if (int(getUserStat(callback_query.from_user.id)[4]) <= 1700):
				msg = f"❌ Минимальный вывод 30 USD | 3000 RUB | 1100 UAH"
			elif int(getUserStat(callback_query.from_user.id)[4]) > 3000:
				msg = f"❌ Для вывода необходимо пройти верификацию.\n\nДля этого необходимо написать в поддержку."
			else:
				msg = f"❌ Ваш баланс: <b>{getUserStat(callback_query.from_user.id)[4]} {getUserStat(callback_query.from_user.id)[7]}</b>\n\nВам нечего выводить."
		else:
			key1 = types.InlineKeyboardButton("Support 👩‍💻", url='https://t.me/tradecoinx_supbot')
			keyboard = types.InlineKeyboardMarkup().add(key1)

			if (int(getUserStat(callback_query.from_user.id)[4]) <= 1700):
				msg = f"❌ Minimum withdrawal 30 USD | 3000 RUB | 1100 UAH"
			elif int(getUserStat(callback_query.from_user.id)[4]) > 3000:
				msg = f"❌ To withdraw, you need to pass verification.\n\nTo do this, you need to write to support."
			else:
				msg = f"❌ Your balance: <b>{getUserStat(callback_query.from_user.id)[4]} {getUserStat(callback_query.from_user.id)[7]}</b>\n\nYou have nothing to output."


		with open("src/output.png", "rb") as photo:
			await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'get_lisence_callback')
	async def get_lisence_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			key1 = types.InlineKeyboardButton("Поддержка 👩‍💻", url='https://t.me/tradecoinx_supbot')
			keyboard = types.InlineKeyboardMarkup().add(key1)

			msg = "🔹 <b>Ваш аккаунт не верифицирован.</b>\n\n"\
				"Получить статус <i>«Верифицирован»</i> можно написав фразу <i>«Верификация»</i> в общий чат технической поддержки.\n\n"\
				"Для перехода в общий чат поддержки понадобится перейти в раздел <i>«Тех. Поддержка»</i>, либо воспользоваться кнопкой ниже.\n\n"
		else:
			key1 = types.InlineKeyboardButton("Support 👩‍💻", url='https://t.me/tradecoinx_supbot')
			keyboard = types.InlineKeyboardMarkup().add(key1)

			msg = "🔹 <b>Your account has not been verified.</b>\n\n"\
				"You can get the status <i>«Verified»</i> by writing the phrase <i>«Verification»</i> to the general technical support chat.\n\n"\
				"To go to the general support chat, you will need to go to the <i>«Tech. Support»</i>, or use the button below.\n\n"


		with open("src/help.png", "rb") as photo:
			await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'options_callback')
	async def options_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			key1 = types.InlineKeyboardButton("🌎 Язык и валюта 💸", callback_data='lisence_callback')
			keyboard = types.InlineKeyboardMarkup().add(key1)

			msg = "<b>⚙ Настройки</b>"
		else:
			key1 = types.InlineKeyboardButton("🌎 Language and currency 💸", callback_data='lisence_callback')
			keyboard = types.InlineKeyboardMarkup().add(key1)

			msg = "<b>⚙ Options</b>"


		with open("src/options.png", "rb") as photo:
			await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'nft_callback')
	async def nft_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await colls_menu(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'coll1_callback')
	async def coll1_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await coll1_nfts(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'coll2_callback')
	async def coll2_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await coll2_nfts(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'CrazySkull2937_callback')
	async def CrazySkull2937_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await CrazySkull2937_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'WuTiger1595_callback')
	async def WuTiger1595_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await WuTiger1595_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'WuTiger1637_callback')
	async def WuTiger1637_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await WuTiger1637_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'CloneX1578_callback')
	async def CloneX1578_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await CloneX1578_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'PsychedelicsAnonymousGenesis2724_callback')
	async def PsychedelicsAnonymousGenesis2724_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await PsychedelicsAnonymousGenesis2724_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'rektguy8221_callback')
	async def rektguy8221_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await rektguy8221_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'PrimeApePlanet622_callback')
	async def PrimeApePlanet622_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await PrimeApePlanet622_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'CakedApes1306_callback')
	async def CakedApes1306_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await CakedApes1306_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'CloneX19636_callback')
	async def CloneX19636_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await CloneX19636_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'AnikiRare1751_callback')
	async def AnikiRare1751_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await AnikiRare1751_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'back_nft_callback')
	async def back_nft_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await colls_menu(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'buy_on_signal_callback')
	async def buy_on_signal_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			msg = "<b>⚙ Данная функция разрабатывается и в скором времени будет добавлена.</b>"
		else:
			msg = "<b>⚙ This feature is under development and will be added soon.</b>"


		with open("src/soon.png", "rb") as photo:
			await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg)


	@dp.callback_query_handler(lambda c: c.data == 'help_callback')
	async def help_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await help_target(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'my_nft_callback')
	async def my_nft_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if callback_query.from_user.id not in admins:
			if getUserStat(callback_query.from_user.id)[6] == "ru":
				msg = f"❌ У вас нет приобретённых NFT."
			else:
				msg = f"❌ You do not have purchased NFTs."

			await bot.send_message(callback_query.from_user.id, msg)
		else:
			buttons = [
				[
					types.InlineKeyboardButton("🌃 Набор #1", callback_data='nabor1_callback')
				],
				[
					types.InlineKeyboardButton("🌃 Набор #2", callback_data='nabor1_callback')
				]
			]

			keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

			msg = f"🌌 <b>Ваши NFT:</b>\n\n"

			await bot.send_message(callback_query.from_user.id, msg, reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'nabor1_callback')
	async def my_nft_admin_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await admin_nfts(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'back_nft_admin_callback')
	async def back_nft_admin_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		await admin_nfts(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'inBetweeners3706_callback')
	async def inBetweeners3706_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await inBetweeners3706_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'CyberBandit4883_callback')
	async def CyberBandit4883_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await CyberBandit4883_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'SamuraiSaga1517_callback')
	async def SamuraiSaga1517_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		try:
			await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
		except:
			await lk_menu(bot, callback_query)


		await SamuraiSaga1517_callback(bot, callback_query)


	@dp.callback_query_handler(lambda c: c.data == 'buy_nft_callback')
	async def buy_nft_callback_cmd(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)

		if getUserStat(callback_query.from_user.id)[6] == "ru":
			if (int(getUserStat(callback_query.from_user.id)[4]) == 0):
				msg = f"❌ Ваш баланс: <b>{getUserStat(callback_query.from_user.id)[4]} {getUserStat(callback_query.from_user.id)[7]}</b>\n\nВы не можете преобрести."
			else:
				msg = f"❌ Ваш баланс: <b>{getUserStat(callback_query.from_user.id)[4]} {getUserStat(callback_query.from_user.id)[7]}</b>\n\nНедостаточно средств."

		else:
			if (int(getUserStat(callback_query.from_user.id)[4]) == 0):
				msg = f"❌ Your balance: <b>{getUserStat(callback_query.from_user.id)[4]} {getUserStat(callback_query.from_user.id)[7]}</b>\n\nYou cannot purchase."
			else:
				msg = f"❌ Your balance: <b>{getUserStat(callback_query.from_user.id)[4]} {getUserStat(callback_query.from_user.id)[7]}</b>\n\nInsufficient funds."

		await bot.send_message(callback_query.from_user.id, msg)




	executor.start_polling(dp, skip_updates=True)


async def info_target(bot, message):
	if getUserStat(message.from_user.id)[6] == "ru":
		key1 = types.InlineKeyboardButton("Поддержка 👩‍💻", url='https://t.me/tradecoinx_supbot')
		keyboard = types.InlineKeyboardMarkup().add(key1)

		msg = "🔹 <b>О Сервисе</b>\n\n"\
			f"<b>{bot_data['bot_name']} — торговая площадка для невзаимозаменяемых токенов (NFT). Покупайте, продавайте и открывайте для себя эксклюзивные цифровые предметы.</b>\n\n"\
			"<b>Покупайте, продавайте и зарабатывайте вместе с нами!</b>"
	else:
		key1 = types.InlineKeyboardButton("Support 👩‍💻", url='https://t.me/tradecoinx_supbot')
		keyboard = types.InlineKeyboardMarkup().add(key1)

		msg = "🔹 <b>About the Service</b>\n\n"\
			f"<b>{bot_data['bot_name']} — marketplace for non-fungible tokens (NFTs). Buy, sell and discover exclusive digital items.</b>\n\n"\
			"<b>Buy, sell and earn with us!</b>"


	with open("src/info.png", "rb") as photo:
		await bot.send_photo(message.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def help_target(bot, message):
	if getUserStat(message.from_user.id)[6] == "ru":
		key1 = types.InlineKeyboardButton("Поддержка 👩‍💻", url='https://t.me/tradecoinx_supbot')
		keyboard = types.InlineKeyboardMarkup().add(key1)

		msg = "<b>Правила обращения в Техническую Поддержку:</b>\n\n"\
			"🔹1. <b>Представьтесь, изложите проблему своими словами</b> - мы постараемся Вам помочь.\n\n"\
			"🔹2. <b>Напишите свой ID</b> - нам это нужно, чтобы увидеть Ваш профиль, и узнать актуальность Вашей проблемы.\n\n"\
			"🔹3. <b>Будьте вежливы</b>, наши консультанты не роботы, мы постараемся помочь Вам, и сделать все возможное, чтобы сберечь Ваше время и обеспечить максимальную оперативность в работе.\n\n"\
			"<i>Напишите нам, ответ Поддержки, не заставит Вас долго ждать!</i>"
	else:
		key1 = types.InlineKeyboardButton("Support 👩‍💻", url='https://t.me/tradecoinx_supbot')
		keyboard = types.InlineKeyboardMarkup().add(key1)

		msg = "<b>Rules for contacting Technical Support:</b>\n\n"\
			"🔹1. <b>Introduce yourself, state the problem in your own words</b> - we will try to help you.\n\n"\
			"🔹2. <b>Write your ID</b> - we need it to see your profile and find out the relevance of your problem.\n\n"\
			"🔹3. <b>Be polite</b>, our consultants are not robots, we will try to help you and do everything possible to save your time and ensure maximum efficiency in work.\n\n"\
			"<i>Write to us, the Support response will not keep you waiting long!</i>"


	with open("src/help.png", "rb") as photo:
		await bot.send_photo(message.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def lk_menu(bot, message):
	if getUserStat(message.from_user.id)[6] == "ru":
		if message.from_user.id not in admins:
			buttons = [
				[
					types.InlineKeyboardButton("📥 Пополнить", callback_data='input_callback'),
					types.InlineKeyboardButton("📤 Вывести", callback_data='output_callback')
				],
				[
					types.InlineKeyboardButton("🎆 NFT", callback_data='nft_callback'),
					types.InlineKeyboardButton("🌌 Мои NFT", callback_data='my_nft_callback')
				],
				[
					types.InlineKeyboardButton("📈 Торговля по сигналам", callback_data='buy_on_signal_callback')
				],
				[
					types.InlineKeyboardButton("📝 Верификация", callback_data='get_lisence_callback')
				],
				[
					types.InlineKeyboardButton("⚙️ Настройки", callback_data='options_callback'),
					types.InlineKeyboardButton("🌐 Тех. Поддержка", callback_data='help_callback')
				]
			]

			keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

			msg = "<b>Личный кабинет</b>\n\n"\
				f"Баланс: <b>{getUserStat(message.from_user.id)[4]} {getUserStat(message.from_user.id)[7]}</b>\n"\
				f"На выводе: <b>{getUserStat(message.from_user.id)[5]} {getUserStat(message.from_user.id)[7]}</b>\n\n"\
				f"Верификация: <b>⚠️ Не верифицирован</b>\n"\
				f"Ваш ID: <code>{message.from_user.id}</code>\n\n"\
				f"Дата и время: {str(datetime.datetime.now())[:-10]}"
		else:
			buttons = [
				[
					types.InlineKeyboardButton("📥 Пополнить", callback_data='input_callback'),
					types.InlineKeyboardButton("📤 Вывести", callback_data='output_callback')
				],
				[
					types.InlineKeyboardButton("🎆 NFT", callback_data='nft_callback'),
					types.InlineKeyboardButton("🌌 Мои NFT", callback_data='my_nft_callback')
				],
				[
					types.InlineKeyboardButton("📈 Торговля по сигналам", callback_data='buy_on_signal_callback')
				],
				[
					types.InlineKeyboardButton("⚙️ Настройки", callback_data='options_callback'),
					types.InlineKeyboardButton("🌐 Тех. Поддержка", callback_data='help_callback')
				]
			]

			keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

			msg = "<b>Личный кабинет</b>\n\n"\
				f"Баланс: <b>{getUserStat(message.from_user.id)[4]} {getUserStat(message.from_user.id)[7]}</b>\n"\
				f"На выводе: <b>{getUserStat(message.from_user.id)[5]} {getUserStat(message.from_user.id)[7]}</b>\n\n"\
				f"Верификация: <b>✅ Верифицирован</b>\n"\
				f"Ваш ID: <code>1247312279</code>\n\n"\
				f"Дата и время: {str(datetime.datetime.now())[:-10]}"
	else:
		if message.from_user.id not in admins:
			buttons = [
				[
					types.InlineKeyboardButton("📥 Top up", callback_data='input_callback'),
					types.InlineKeyboardButton("📤 Withdraw", callback_data='output_callback')
				],
				[
					types.InlineKeyboardButton("🎆 NFT", callback_data='nft_callback'),
					types.InlineKeyboardButton("🌌 My NFT", callback_data='my_nft_callback')
				],
				[
					types.InlineKeyboardButton("📈 Signal trading", callback_data='buy_on_signal_callback')
				],
				[
					types.InlineKeyboardButton("📝 Verification", callback_data='get_lisence_callback')
				],
				[
					types.InlineKeyboardButton("⚙️ Options", callback_data='options_callback'),
					types.InlineKeyboardButton("🌐 Tech. Support", callback_data='help_callback')
				]
			]

			keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

			msg = "<b>Personal account</b>\n\n"\
				f"Balance: <b>{getUserStat(message.from_user.id)[4]} {getUserStat(message.from_user.id)[7]}</b>\n"\
				f"On the output: <b>{getUserStat(message.from_user.id)[5]} {getUserStat(message.from_user.id)[7]}</b>\n\n"\
				f"Verification: <b>⚠️ Not verified</b>\n"\
				f"Your ID: <code>{message.from_user.id}</code>\n\n"\
				f"Date and time: {str(datetime.datetime.now())[:-10]}"
		else:
			buttons = [
				[
					types.InlineKeyboardButton("📥 Top up", callback_data='input_callback'),
					types.InlineKeyboardButton("📤 Withdraw", callback_data='output_callback')
				],
				[
					types.InlineKeyboardButton("🎆 NFT", callback_data='nft_callback'),
					types.InlineKeyboardButton("🌌 My NFT", callback_data='my_nft_callback')
				],
				[
					types.InlineKeyboardButton("📈 Signal trading", callback_data='buy_on_signal_callback')
				],
				[
					types.InlineKeyboardButton("⚙️ Options", callback_data='options_callback'),
					types.InlineKeyboardButton("🌐 Tech. Support", callback_data='help_callback')
				]
			]

			keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

			msg = "<b>Personal account</b>\n\n"\
				f"Balance: <b>{getUserStat(message.from_user.id)[4]} {getUserStat(message.from_user.id)[7]}</b>\n"\
				f"On the output: <b>{getUserStat(message.from_user.id)[5]} {getUserStat(message.from_user.id)[7]}</b>\n\n"\
				f"Verification: <b>✅ Verified</b>\n"\
				f"Your ID: <code>1247312279</code>\n\n"\
				f"Date and time: {str(datetime.datetime.now())[:-10]}"


	with open("src/lk.png", "rb") as photo:
		await bot.send_photo(message.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)




if __name__ == '__main__':
	try:
		print(f"\nBot has been started! {str(datetime.datetime.now())[:-10]}\n\n")
		bot_start()
	except:
		print(f"\nBot has been started! {str(datetime.datetime.now())[:-10]}\n\n")
		bot_start()