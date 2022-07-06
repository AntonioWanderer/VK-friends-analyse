import Config
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
	
def idList():
	ids = []
	for i in range(len(os.listdir("/home/antonio/OnlineRequests simp/requests"))):
		conn, cur = sqlInit(i)
		formula = "SELECT * FROM online_requests"
		cur.execute(formula)
		all_results = cur.fetchall()
		sqlClose(conn, cur)
		for result in all_results:
			thisId = result[2]
			if not thisId in ids:
				ids.append(thisId)
	return(sorted(ids))
	
def resultsLoad(i, uid):
	conn, cur = sqlInit(i)
	formula = "SELECT * FROM online_requests WHERE usr_online == " + str(uid)
	cur.execute(formula)
	all_results = cur.fetchall()
	sqlClose(conn, cur)
	return(all_results)
	
def fullBase(uid):
	base = []
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
	return(common)

def compCouple(id1, id2):
	base1 = fullBase(id1)
	base2 = fullBase(id2)
	return comparator(base1, base2)

def compAndDescribeAll():
	ids = Config.IDGLOB
	leng = len(ids)
	matrix = np.zeros((leng, leng))
	flatten = []
	#ids = idList()
	i = 0
	for i1 in range(leng):
		for i2 in range(i1 + 1):
			z = compCouple(ids[i1], ids[i2])/30
			print(ids[i1], ids[i2])
			matrix[i1][i2] = z
			matrix[i2][i1] = z
			if z != 1:
				flatten.append(z)
			i = i + 1
			#print("progress ", int(100 * i * 2 / ((leng) * (leng + 1))), "%")
	return(matrix, flatten)
	
matrix, flatten = compAndDescribeAll()
print(matrix)
