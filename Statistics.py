import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

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
	
def sqlClose(conn, cur):
	cur.close()
	conn.close()
	
def resultsLoad(i, uid):
	conn, cur = sqlInit(i)
	formula = "SELECT * FROM online_requests WHERE usr_online == " + str(uid)
	cur.execute(formula)
	all_results = cur.fetchall()
	sqlClose(conn, cur)
	return(all_results)
	
def fullBase(uid):
	base = []
	x = []
	for i in range(len(os.listdir("/home/antonio/OnlineRequests simp/requests"))):
		for result in resultsLoad(i + 1, uid):
			base.append(result)
	return(base)

def comparator(base1, base2):
	full = 0
	common = 0
	t1 = []
	t2 = []
	for element in base1:
		t1.append(element[1])
	for element in base2:
		t2.append(element[1])
	for t in t1:
		if t in t2:
			common = common + 1
	full = len(t1) + len(t2) - common
	return(common / full)

def compCouple(id1, id2):
	base1 = fullBase(id1)#650125)
	base2 = fullBase(id2)#111402557)
return comparator(base1, base2)


