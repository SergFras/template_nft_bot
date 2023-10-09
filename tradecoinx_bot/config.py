# -*- coding: utf-8 -*-

# https://t.me/tradecoinx_bot
# https://t.me/tradecoinx_supbot 6413261211:AAGRnz07KmIgjDWqz3wdrN4OfjK792sbQHw
bot_data = {
	"token" : "6455597946:AAGz1DNlXETRse3dskwHi2Q_YpitXnFmXlE",
	"bot_name" : "TradeCoinX",
	"amount_nfts": 10,
	"amount_colls": 2
}


crypto_payments = [
	"0x71ED5d4EbC9636a2620c37b1c488d6Be87F7474E", 
	"0xcDc77CE62f92f639C741Dd177E2b4d78eb86c839", 
	"0x5c69F35ef7deA72c5E96623a74b17e321A6934b0"
]


bank_payments = {
	"sberbank": "https://cryptostrike.org/sberbank-na-tether-erc-20.html",
	"tinkoff": "https://cryptostrike.org/tinkoff-na-tether-erc-20.html",
	"aplha": "https://cryptostrike.org/alfabank-na-tether-erc-20.html",
	"sbp": "https://cryptostrike.org/sbp-rub-na-tether-erc-20.html",
	"mir" : "https://cryptostrike.org/mir-na-tether-erc-20.html",
	"visa_mastercard" : "https://cryptostrike.org/visa-mastercard-rur-na-tether-erc-20.html"
}


admins = [
	892023960,
	953850886,
	1117316269
]


# with open("src/coll2/test.gif", "rb") as animation:
# 	await bot.send_animation(callback_query.from_user.id, animation=animation, caption=msg, reply_markup=keyboard)