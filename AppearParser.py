import threading
import time
import datetime
import requests
import json 
import sqlite3
import Config
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

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
		lst = r["response"]
		for l in lst:
			cur.execute("""INSERT INTO 'online_requests' (request_time, usr_online) VALUES (?, ?);
			""", (now, l))
		conn.commit()
		time.sleep(2)

def timeLines():
	conn, cur = sqlInit()
	cur.execute("SELECT * FROM online_requests ORDER BY usr_online;")
	all_results = cur.fetchall()
	gx = []
	gy = []
	gn = []
	x = []
	y = []
	i = 0
	uId = 0
	ax1.clear()
	for result in all_results:
		if result[2] != uId:
			gx.append(x)
			gy.append(y)
			gn.append("№ " + str(i) + " " + str(uId))
			uId = result[2]
			i = i + 1
			x = []
			y = []
		else:
			x.append(result[1])
			y.append(i)
	return(gx, gy, gn)

def animate(j):
	gx, gy, gn = timeLines()
	matrixLoop(gx, gy, gn)
	for num in range(len(gn)):
		ax1.plot(gx[num], gy[num], label=gn[num])
		ax1.legend()

def monitorLoop():
	while True:
		ani = animation.FuncAnimation(fig, animate, interval=1000)
		plt.show()
		
def coatingTime(gx1, gy1, gx2, gy2):
	l = 0
	e = 0
	for g in gx1:
		if g in gx2:
			l = l + 1
			e = e + 1
		else:
			l = l + 1
	for g in gx2:
		if g in gx1:
			pass
		else:
			l = l + 1
	if l > 0:
		return(e/l)
	else:
		return(100)

def matrixLoop(gx, gy, gn):
	for n in gn:
		print(n, "\n")
	matr = np.zeros((len(gn), len(gn)))
	for num in range(len(gn)):
		for num2 in range(num):
			matr[num][num2] = coatingTime(gx[num], gy[num], gx[num2], gy[num2])
	print(matr)

ford = threading.Thread(name='foreground', target=parsingLoop)
back = threading.Thread(name='background', target=monitorLoop)
#back2 = threading.Thread(name='background', target=matrixLoop)

ford.start()
back.start()
#back2.start()

conn, cur = sqlInit()

cur.close()
conn.close()
