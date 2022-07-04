import os
import sqlite3

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
	
def resultsLoad(i):
	conn, cur = sqlInit(i)
	cur.execute("""SELECT * FROM online_requests """)
	all_results = cur.fetchall()
	sqlClose(conn, cur)
	return(all_results)
	
def fullBase():
	base = []
	for i in range(len(os.listdir("/home/antonio/OnlineRequests simp/requests"))-1):
		for result in resultsLoad(i + 1):
			base.append(result)
	print(base)
	
fullBase()
