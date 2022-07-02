import threading
import time
import datetime
import requests
import json 
import sqlite3
import Config
import matplotlib.pyplot as plt
import matplotlib.animation as animation

access_token=Config.TOKEN
expires_in=86400
user_id=344666363

URL = "https://api.vk.com/method/friends.getOnline?v=5.81&access_token=" + access_token

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

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
		r = requests.get(URL).json()
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

def animate(j):
	conn, cur = sqlInit()
	cur.execute("SELECT * FROM online_requests ORDER BY usr_online;")
	all_results = cur.fetchall()
	x = []
	y = []
	i = 0
	uId = 0
	ax1.clear()
	for result in all_results:
		if result[2] != uId:
			ax1.plot(x, y, label="№ " + str(i) + " " + str(uId))
			ax1.legend()
			uId = result[2]
			i = i + 1
			x = []
			y = []
		else:
			x.append(result[1])
			y.append(i)

def marking():
	while True:
		ani = animation.FuncAnimation(fig, animate, interval=1000)
		plt.show()


ford = threading.Thread(name='foreground', target=marking)
back = threading.Thread(name='background', target=parsingLoop)

ford.start()
back.start()

conn, cur = sqlInit()

cur.close()
conn.close()
