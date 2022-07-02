import os
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

track = []
print("Hom many peoples you would like to track?")
quant = int(input())
for q in range(quant):
	print("\n User id = ")
	track.append(int(input()))

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

if os.path.isfile("requests.db"):
	os.remove("requests.db")

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
		time.sleep(10)

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
			gn.append(uId)
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
		time.sleep(30)
		
def coatingTime(gx1, gx2):
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
		return(0)

def matrixLoop(gx, gy, gn):
	matr = np.zeros((len(gn), len(gn)))
	for num in range(len(gn)):
		for num2 in range(num):
			matr[num][num2] = coatingTime(gx[num], gx[num2])
	print(matr)
	print("\n\n")
	for n in track:
		print(n, "\n")
	matr2 = np.zeros((quant, quant))
	for i in range(quant):
		for j in range(quant):
			if (track[i] in gn) & (track[j] in gn):
				n1 = gn.index(track[i])
				n2 = gn.index(track[j])
				matr2[i][j] = matr[n1][n2]
				matr2[j][i] = matr[n2][n1]
	print(matr2)
	with open("Matrix.txt", "w") as f:
		for n in gn:
			f.write(str(n) +  "\n")
		for i in range(len(gn)):
			for j in range(len(gn)):
				s = str(int(matr[i][j] * 100))
				f.write(str(gn[i]) + "-")
				f.write(str(gn[j]) + "-")
				f.write(s)
				if len(s) == 1:
					f.write("   ")
				elif len(s) == 2:
					f.write("  ")
				elif len(s) == 3:
					f.write(" ")
			f.write("\n")
		f.close()

ford = threading.Thread(name='foreground', target=parsingLoop)
back = threading.Thread(name='background', target=monitorLoop)

ford.start()
back.start()

conn, cur = sqlInit()

cur.close()
conn.close()
