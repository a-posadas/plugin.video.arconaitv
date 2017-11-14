import requests
from bs4 import BeautifulSoup
import json

arconaitv_url = "https://www.arconaitv.xyz/"

arconaitv_r = requests.get(arconaitv_url+"index.php")
html_text = arconaitv_r.text.encode('ascii', 'ignore')
soup = BeautifulSoup(html_text, 'html.parser')
movies = soup.find("div", id="movies")
boxes = movies.find_all("div", class_="box-content")

movies_list = []

def myprint(d,title):
	for k, v in d.items():
		if isinstance(v, dict):
			myprint(v,title)
		elif k == 'extract':
			movie_dict = {'movie':title,'description':v}
			movies_list.append(movie_dict)

for box in boxes:
	if box.a == None:
		continue
	title = box.a["title"]
	wiki_r = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="+title)
	parsed = json.loads(wiki_r.text.encode('ascii', 'ignore'))
	myprint(parsed,title)

movies_dict = {'movies':movies_list}
movies_json = json.dumps(movies_dict)
with open("movies.json","w") as f: 
	f.write(movies_json) 

