
import requests
from bs4 import BeautifulSoup
import re

def initial_request():
	token = ""
	session_id = ""

	url = "http://192.168.1.14:/index/login.php"

	# - make request to get login page HTML
	r = requests.get(url)

	session_id = re.match("PHPSESSID=(.*?);", r.headers["set-cookie"])
	session_id = session_id.group(1)

	cookie = {"PHPSESSID" : session_id}

	soup = BeautifulSoup(r.text, "html.parser")

	token = soup.find("input", {"name": "user_token"})["value"]

	

	data = {"username": "admin", "password": "password", "Login": "Login", "user_token": token}
	html = requests.post(url, data, cookies = cookie)

	print(html.content)

initial_request()


