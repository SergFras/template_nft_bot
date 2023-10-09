# -*- coding: utf-8 -*-
import sqlite3 as sl
import datetime
import os.path


path = 'modules/users.db'


def createDB():
	if not(os.path.exists(path)):
		con = sl.connect(path)

		with con:
			con.execute("""
				CREATE TABLE USERS (
					uid INTEGER,
					first_name TEXT,
					last_name TEXT,
					username TEXT,
					input INTEGER,
					output INTEGER,
					language TEXT,
					currency TEXT
				);
			""")
		con.commit()
		con.close()


def regUser(uid, first_name, last_name, username):
	uregdate = str(datetime.date.today())
	con = sl.connect(path)
	cur = con.cursor()
	cur.execute('INSERT INTO USERS (uid, first_name, last_name, username, input, output, language, currency) values(?, ?, ?, ?, ?, ?, ?, ?);', (int(uid), str(first_name), str(last_name), f'@{username}', 0, 0, 'ru', 'RUB'))
	con.commit()
	con.close()


def getUserStat(uid):
	uid = int(uid)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.close()

		return user


def updateUinput(uid, uinput):
	uid = int(uid)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET input = ? WHERE uid = ?", (uinput, uid))
		con.commit()
		con.close()


def updateUoutput(uid, uoutput):
	uid = int(uid)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET output = ? WHERE uid = ?", (uoutput, uid))
		con.commit()
		con.close()


def updateUlang(uid, language):
	uid = int(uid)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET language = ? WHERE uid = ?", (language, uid))
		con.commit()
		con.close()


def updateUcurrency(uid, currency):
	uid = int(uid)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET currency = ? WHERE uid = ?", (currency, uid))
		con.commit()
		con.close()


def getAllStat():
	con = sl.connect(path)
	users = con.execute(f'SELECT * FROM USERS').fetchall()

	return users






