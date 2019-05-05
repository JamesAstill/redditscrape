from bs4 import BeautifulSoup
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()
#Set up the current subreddit name
current_reddit = 'redditsoccercity'
url = 'https://www.reddit.com/r/' + current_reddit + '/'

#Function to pool the subreddit for open threads
def getMatchesReddit():
	#Http request from url above
	response = http.request('GET', url)
	#Parse HTTP with html parser
	soup = BeautifulSoup(response.data, 'html.parser')
	#Links are located within anchor <a> tags
	out = soup.find_all("a")
	match_links = []
	#Iterate through all links to find those ending hhmm_gmt_matchname
	for link in out:
		temp = link.get('href')
		words = temp.split('/')
		if len(words) == 9:
			if re.match(r"[0-9]",words[7]):
				match_links.append(words[6]+"/"+words[7])
	return match_links

#Call the function to allow matches to be iterable
match_urls = getMatchesReddit()
user_menu = []
i=1
### USER MENU - Print available matches, listed 1 to N ###
for match in match_urls:
	url2 = url + 'comments/' + match
	user_menu.append(url2)
	print(str(i) + ". " + url)
	i=i+1
user_choice = input("Which match would you like links for?\n")
url_chosen = url + 'comments/' + match_urls[int(user_choice)-1]

#User choice is then pooled as previously, using HTML parser
response = http.request('GET', url_chosen)
soup = BeautifulSoup(response.data, 'html.parser')

matches = []
#Comments are stored within a quoute block which uses a paragraph tag <p>.
#These are then searched to see if they are like acestream://xxxxxxxxxxxx
for comment in soup.find_all('p'):
	temp = comment.find(string=re.compile("acestream"))
	matches.append(temp)

#Remove 'None' entries
initial = [i for i in matches if i is not None]

final = {}
for item in initial:
	new = item.split(' ')
	final[item] = new[0]

#Print dictionary name/value pairs to confirmm success
print(final)
