import os
import time
import datetime
import requests
import json 
import sqlite3
import Config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

start = datetime.datetime.now()

def genToken():
	driver = webdriver.Chrome(ChromeDriverManager().install())
	#driver = webdriver.Chrome(
	#executable_path=r'/chromedriver')
	driver.get(Config.LINK)
	access_token = ''
	while not access_token:
		page_url = driver.current_url

		if 'access_token' in page_url:
        		#token
                #token_start = page_url.index(TOKEN) + len(TOKEN)
                #access_token = page_url[token_start:token_start+ATOKEN_LEN]
			break

		else:
			time.sleep(1)

	print(access_token)

	# Для удобства сохраняем XPath формы авторизации
	#username = '//*[@id="login_submit"]/div/div/input[6]'
	#password = '//*[@id="login_submit"]/div/div/input[7]'
	#login = '//*[@id="install_allow"]'

	# Заполняем форму авторизации
	#driver.find_element_by_xpath(username).send_keys(vk['login'])
	#driver.find_element_by_xpath(password).send_keys(vk['password'])
	#driver.find_element_by_xpath(login).click()

	#print(driver.current_url)

	

def accessInit():
	access_token=Config.TOKEN
	URL = "https://api.vk.com/method/friends.getOnline?v=5.81&access_token=" + access_token
	return URL

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

def parsingLoop(URL, conn, cur):
	for j in range(100):
		r = requests.get(URL).json()
		now = datetime.datetime.now()
		lst = r["response"]
		for l in lst:
			cur.execute("""INSERT INTO 'online_requests' (request_time, usr_online) VALUES (?, ?);""", (now, l))
		print(now)
		conn.commit()
		time.sleep(2)
def Parse(URL):
	i = 0
	while True:
		i = i + 1
		conn, cur = sqlInit(i)
		parsingLoop(URL, conn, cur)

		cur.close()
		conn.close()
	
genToken()	
#URL = accessInit()
#Parse(URL)
