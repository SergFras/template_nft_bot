from aiogram import Bot, Dispatcher, executor, types
import random

from config import *
from modules.database import *



async def payment(bot, callback_query, link):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		key1 = types.InlineKeyboardButton("✅ Оплатил", callback_data='input_crypto_target_callback')
		keyboard = types.InlineKeyboardMarkup().add(key1)

		msg = f"💎 Вставьте этот кошелёк в поле перевода\n\n<code>{crypto_payments[random.randint(0, 2)]}</code>\n\n<b>Ссылка для оплаты:</b>\n{link}\n\n"\
			"⚠️ Уважаемый пользователь, обращаем ваше внимание, что все вводы меньше 1000 RUB | 400 UAH  | 10 USD зачисляться в сервис не будут, возмещение по данным транзакциям так же не предусмотрено."
	else:
		key1 = types.InlineKeyboardButton("✅ Paid", callback_data='input_crypto_target_callback')
		keyboard = types.InlineKeyboardMarkup().add(key1)

		msg = f"💎 Paste this wallet into the transfer field\n\n<code>{crypto_payments[random.randint(0, 2)]}</code>\n\n<b>Payment link:</b>\n{link}\n\n"\
			"⚠️ Dear user, please note that all inputs less than 1000 RUB | 400 UAH | 10 USD will not be credited to the service, compensation for these transactions is also not provided."


	await bot.send_message(callback_query.from_user.id, msg, reply_markup=keyboard)


async def colls_menu(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("Коллекция #1", callback_data='coll1_callback')
			],
			[
				types.InlineKeyboardButton("Коллекция #2", callback_data='coll2_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 На данный момент на маркетплейсе всего {bot_data['amount_colls']} коллекции"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("Collection #1", callback_data='coll1_callback')
			],
			[
				types.InlineKeyboardButton("Collection #2", callback_data='coll2_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 At the moment there are {bot_data['amount_colls']} collections on the marketplace"


	with open("src/nft.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def coll1_nfts(bot, callback_query):
	buttons = [
			[
				types.InlineKeyboardButton("CrazySkull #2937", callback_data='CrazySkull2937_callback')
			],
			[
				types.InlineKeyboardButton("Wu Tiger #1595", callback_data='WuTiger1595_callback')
			],
			[
				types.InlineKeyboardButton("Wu Tiger #1637", callback_data='WuTiger1637_callback')
			],
			[
				types.InlineKeyboardButton("CloneX #1578", callback_data='CloneX1578_callback')
			],
			[
				types.InlineKeyboardButton("Psychedelics Anonymous Genesis #2724", callback_data='PsychedelicsAnonymousGenesis2724_callback')
			]
		]

	keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

	if getUserStat(callback_query.from_user.id)[6] == "ru":
		msg = f"💠 На данный момент на маркетплейсе всего {bot_data['amount_colls']} коллекции."
	else:
		msg = f"💠 At the moment there are {bot_data['amount_colls']} collections on the marketplace."


	with open("src/nft.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def CrazySkull2937_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен CrazySkull 2937\n\n"\
			"🗂 Коллекция: <b>#1</b>\n"\
			"🔹 Блокчейн: <b>Ethereum</b>\n\n"\
			"💸 Цена: <b>18.35 USD</b> <i>(~1801,9 RUB | ~677,7 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token CrazySkull 2937\n\n"\
			"🗂 Collection: <b>#1</b>\n"\
			"🔹 Chain: <b>Ethereum</b>\n\n"\
			"💸 Price: <b>18.35 USD</b> <i>(~1801,9 RUB | ~677,7 UAH)</i>"


	with open("src/coll1/1.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def WuTiger1595_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен WuTiger 1595\n\n"\
			"🗂 Коллекция: <b>#1</b>\n"\
			"🔹 Блокчейн: <b>Ethereum</b>\n\n"\
			"💸 Цена: <b>21.51 USD</b> <i>(~2112,2 RUB | ~794,4 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token WuTiger 1595\n\n"\
			"🗂 Collection: <b>#1</b>\n"\
			"🔹 Chain: <b>Ethereum</b>\n\n"\
			"💸 Price: <b>21.51 USD</b> <i>(~2112,2 RUB | ~794,4 UAH)</i>"


	with open("src/coll1/2.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def WuTiger1637_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен WuTiger 1637\n\n"\
			"🗂 Коллекция: <b>#1</b>\n"\
			"🔹 Блокчейн: <b>Ethereum</b>\n\n"\
			"💸 Цена: <b>19.14 USD</b> <i>(~1879,47 RUB | ~706,87 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token WuTiger 1637\n\n"\
			"🗂 Collection: <b>#1</b>\n"\
			"🔹 Chain: <b>Ethereum</b>\n\n"\
			"💸 Price: <b>19.14 USD</b> <i>(~1879,47 RUB | ~706,87 UAH)</i>"


	with open("src/coll1/3.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def CloneX1578_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен CloneX 1578\n\n"\
			"🗂 Коллекция: <b>#1</b>\n"\
			"🔹 Блокчейн: <b>Bitcoin</b>\n\n"\
			"💸 Цена: <b>18.76 USD</b> <i>(~1842,16 RUB | ~692,84 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token CloneX 1578\n\n"\
			"🗂 Collection: <b>#1</b>\n"\
			"🔹 Chain: <b>Bitcoin</b>\n\n"\
			"💸 Price: <b>18.76 USD</b> <i>(~1842,16 RUB | ~692,84 UAH)</i>"


	with open("src/coll1/4.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def PsychedelicsAnonymousGenesis2724_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен Psychedelics Anonymous Genesis 2724\n\n"\
			"🗂 Коллекция: <b>#1</b>\n"\
			"🔹 Блокчейн: <b>Bitcoin</b>\n\n"\
			"💸 Цена: <b>19.54 USD</b> <i>(~1918,48 RUB | ~721,64 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token Psychedelics Anonymous Genesis 2724\n\n"\
			"🗂 Collection: <b>#1</b>\n"\
			"🔹 Chain: <b>Bitcoin</b>\n\n"\
			"💸 Price: <b>19.54 USD</b> <i>(~1918,48 RUB | ~721,64 UAH)</i>"


	with open("src/coll1/5.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def coll2_nfts(bot, callback_query):
	buttons = [
			[
				types.InlineKeyboardButton("rektguy #8221", callback_data='rektguy8221_callback')
			],
			[
				types.InlineKeyboardButton("Prime Ape Planet #622", callback_data='PrimeApePlanet622_callback')
			],
			[
				types.InlineKeyboardButton("Caked Apes #1306", callback_data='CakedApes1306_callback')
			],
			[
				types.InlineKeyboardButton("CloneX #19636", callback_data='CloneX19636_callback')
			],
			[
				types.InlineKeyboardButton("Aniki Rare #1751", callback_data='AnikiRare1751_callback')
			]
		]

	keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

	if getUserStat(callback_query.from_user.id)[6] == "ru":
		msg = f"💠 На данный момент на маркетплейсе всего {bot_data['amount_colls']} коллекции."
	else:
		msg = f"💠 At the moment there are {bot_data['amount_colls']} collections on the marketplace."


	with open("src/nft.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def rektguy8221_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен rektguy 8221\n\n"\
			"🗂 Коллекция: <b>#2</b>\n"\
			"🔹 Блокчейн: <b>Bitcoin</b>\n\n"\
			"💸 Цена: <b>24.13 USD</b> <i>(~2369,47 RUB | ~891,16 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token rektguy 8221\n\n"\
			"🗂 Collection: <b>#2</b>\n"\
			"🔹 Chain: <b>Bitcoin</b>\n\n"\
			"💸 Price: <b>24.13 USD</b> <i>(~2369,47 RUB | ~891,16 UAH)</i>"


	with open("src/coll2/1.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def PrimeApePlanet622_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен Prime Ape Planet 622\n\n"\
			"🗂 Коллекция: <b>#2</b>\n"\
			"🔹 Блокчейн: <b>Bitcoin</b>\n\n"\
			"💸 Цена: <b>22.41 USD</b> <i>(~2200,57 RUB | ~827,64 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token Prime Ape Planet 622\n\n"\
			"🗂 Collection: <b>#2</b>\n"\
			"🔹 Chain: <b>Bitcoin</b>\n\n"\
			"💸 Price: <b>22.41 USD</b> <i>(~2200,57 RUB | ~827,64 UAH)</i>"


	with open("src/coll2/2.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def CakedApes1306_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен Caked Apes 1306\n\n"\
			"🗂 Коллекция: <b>#2</b>\n"\
			"🔹 Блокчейн: <b>Ethereum</b>\n\n"\
			"💸 Цена: <b>21.78 USD</b> <i>(~2138,71 RUB | ~804,37 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token Caked Apes 1306\n\n"\
			"🗂 Collection: <b>#2</b>\n"\
			"🔹 Chain: <b>Ethereum</b>\n\n"\
			"💸 Price: <b>21.78 USD</b> <i>(~2138,71 RUB | ~804,37 UAH)</i>"


	with open("src/coll2/3.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def CloneX19636_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен CloneX 19636\n\n"\
			"🗂 Коллекция: <b>#2</b>\n"\
			"🔹 Блокчейн: <b>Ethereum</b>\n\n"\
			"💸 Цена: <b>23.95 USD</b> <i>(~2351,8 RUB | ~884,51 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token CloneX 19636\n\n"\
			"🗂 Collection: <b>#2</b>\n"\
			"🔹 Chain: <b>Ethereum</b>\n\n"\
			"💸 Price: <b>23.95 USD</b> <i>(~2351,8 RUB | ~884,51 UAH)</i>"


	with open("src/coll2/4.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)


async def AnikiRare1751_callback(bot, callback_query):
	if getUserStat(callback_query.from_user.id)[6] == "ru":
		buttons = [
			[
				types.InlineKeyboardButton("✅ Купить", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Обратно", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Токен Aniki Rare 1751\n\n"\
			"🗂 Коллекция: <b>#2</b>\n"\
			"🔹 Блокчейн: <b>Bitcoin</b>\n\n"\
			"💸 Цена: <b>32.28 USD</b> <i>(~3169,77 RUB | ~1192,15 UAH)</i>"
	else:
		buttons = [
			[
				types.InlineKeyboardButton("✅ Buy", callback_data='buy_nft_callback'),
				types.InlineKeyboardButton("↩️ Back", callback_data='back_nft_callback')
			]
		]

		keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

		msg = f"💠 Token Aniki Rare 1751\n\n"\
			"🗂 Collection: <b>#2</b>\n"\
			"🔹 Chain: <b>Bitcoin</b>\n\n"\
			"💸 Price: <b>32.28 USD</b> <i>(~3169,77 RUB | ~1192,15 UAH)</i>"


	with open("src/coll2/5.png", "rb") as photo:
		await bot.send_photo(callback_query.from_user.id, photo=photo, caption=msg, reply_markup=keyboard)