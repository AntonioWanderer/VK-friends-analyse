import threading
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

def sqlInit():
	conn = sqlite3.connect('requests.db',
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

def parsingLoop():
	while True:
		conn, cur = sqlInit()
		r = requests.get(URL).json()#["response"]["items"]
		now = datetime.datetime.now()
		with open("friends.json", "a") as f:
			f.write(json.dumps(r))

		f.close()

		lst = r["response"]
		for l in lst:
			cur.execute("""INSERT INTO 'online_requests' (request_time, usr_online) VALUES (?, ?);
			""", (now, l))
		conn.commit()
		print("Done")
		time.sleep(2)
		
def marking():
	while True:
		print("hi")
		time.sleep(2)


#parsingLoop(cur)


ford = threading.Thread(name='foreground', target=marking)
back = threading.Thread(name='background', target=parsingLoop)

ford.start()
back.start()

conn, cur = sqlInit()
cur.execute("SELECT * FROM online_requests;")
all_results = cur.fetchall()
for result in all_results:
	print(result)

cur.close()
conn.close()
