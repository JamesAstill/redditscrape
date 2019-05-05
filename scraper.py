from bs4 import BeautifulSoup
import re
import requests

#Set up the current subreddit name
current_reddit = 'redditsoccercity'
url = 'https://www.reddit.com/r/' + current_reddit + '/'

#Function to pool the subreddit for open threads
def getMatchesReddit():
	#Http request from url above
	response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).content
	#Parse HTTP with html parser
	soup = BeautifulSoup(response, 'html.parser')
	#Links are located within anchor <a> tags
	out = soup.find_all("a")
	match_links = {}
	#Iterate through all links to find those ending hhmm_gmt_matchname
	for link in out:
		temp = link.get('href')
		words = temp.split('/')
		if len(words) == 7:
			if re.match(r"[0-9]",words[5]): 
				if re.match(r"\[\d",link.get_text()):
					match_links[link.get_text()] = (words[4]+"/"+words[5])
	return match_links

#Call the function to allow matches to be iterable
match_urls = getMatchesReddit()
user_menu = []
i=1
### USER MENU - Print available matches, listed 1 to N ###
for key, value in match_urls.items():
	url2 = url + 'comments/' + match_urls[key]
	user_menu.append(url2)
	print(str(i) + ". " + key)
	i=i+1
user_choice = input("Which match would you like links for?\n")
url_chosen = url + 'comments/' + match_urls[int(user_choice)-1]

#User choice is then pooled as previously, using HTML parser
response = requests.get(url_chosen, headers={'User-agent': 'Mozilla/5.0'}).content
soup = BeautifulSoup(response, 'html.parser')

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
