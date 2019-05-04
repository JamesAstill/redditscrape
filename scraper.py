from bs4 import BeautifulSoup
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()

def getMatchesReddit():
	url = 'https://www.reddit.com/r/redditsoccercity/'
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data, 'html.parser')
	out = soup.find_all("a")
	match_links = []
	for link in out:
		temp = link.get('href')
		words = temp.split('/')
		if len(words) == 9:
			if re.match(r"[0-9]",words[7]):
				match_links.append(words[6]+"/"+words[7])
			else:
				continue
		else:
			continue
	return match_links
match_urls = getMatchesReddit()
user_menu = []
i=1
for match in match_urls:
	url = 'https://www.reddit.com/r/redditsoccercity/comments/' + match
	user_menu.append(url)
	print(str(i)+". "+url)
	i=i+1

user_choice = input("Which match would you like links for?\n")

url_chosen = 'https://www.reddit.com/r/redditsoccercity/comments/' + match_urls[int(user_choice)-1]
response = http.request('GET', url_chosen)

soup = BeautifulSoup(response.data, 'html.parser')

matches = []
for comment in soup.find_all('p'):
	temp = comment.find(string=re.compile("acestream"))
	matches.append(temp)

initial = [i for i in matches if i is not None]


final = {}
for item in initial:
	new = item.split(' ')
	final[item] = new[0]


print(final)
