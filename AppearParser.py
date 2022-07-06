import os
import time
import datetime
import requests
import json 
import sqlite3
import Config

access_token=Config.TOKEN
expires_in=86400
user_id=344666363

URL = "https://api.vk.com/method/friends.getOnline?v=5.81&access_token=" + access_token

def sqlInit(i):
	conn = sqlite3.connect("requests/requests"+str(i)+".db",
                       detect_types=sqlite3.PARSE_DECLTYPES |
                       sqlite3.PARSE_COLNAMES) #connection sql
	cur = conn.cursor() #cursor for connection
	cur.execute("""CREATE TABLE IF NOT EXISTS online_requests(
   	id INTEGER PRIMARY KEY AUTOINCREMENT,
   	request_time TIMESTAMP,
   	usr_online INT);
	""")
	conn.commit()
	return(conn, cur)

def parsingLoop(conn, cur):
	for j in range(100):
		r = requests.get(URL).json()
		now = datetime.datetime.now()
		lst = r["response"]
		for l in lst:
			cur.execute("""INSERT INTO 'online_requests' (request_time, usr_online) VALUES (?, ?);""", (now, l))
		print(now)
		conn.commit()
		time.sleep(2)

i = 0
while True:
	i = i + 1
	conn, cur = sqlInit(i)
	parsingLoop(conn, cur)

	cur.close()
	conn.close()
