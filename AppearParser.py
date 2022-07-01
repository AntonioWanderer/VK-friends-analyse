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

conn = sqlite3.connect('requests.db',
                       detect_types=sqlite3.PARSE_DECLTYPES |
                       sqlite3.PARSE_COLNAMES) #connection sql
cur = conn.cursor() #cursor for connection
#SQL REQUEST TEMPLATE:
#cur.execute(""" """)
#conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS online_requests(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   request_time TIMESTAMP,
   usr_online INT);
""")
conn.commit()

for n in range(10):
	r = requests.get(URL).json()#["response"]["items"]
	now = datetime.datetime.now()
	with open("friends.json", "w") as f:
		f.write(json.dumps(r))

	f.close()

	lst = r["response"]
	for l in lst:
		cur.execute("""INSERT INTO 'online_requests' (request_time, usr_online) VALUES (?, ?);
		""", (now, l))
	conn.commit()
	print("Done")
	time.sleep(10)

cur.execute("SELECT * FROM online_requests;")
all_results = cur.fetchall()
for result in all_results:
	print(result)

cur.close()
conn.close()
