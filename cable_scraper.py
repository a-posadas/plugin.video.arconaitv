import requests
from bs4 import BeautifulSoup
import json

arconaitv_url = "https://www.arconaitv.xyz/"

arconaitv_r = requests.get(arconaitv_url+"index.php")
html_text = arconaitv_r.text.encode('ascii', 'ignore')
soup = BeautifulSoup(html_text, 'html.parser')
cable = soup.find("div", id="cable")
boxes = cable.find_all("div", class_="box-content")

cable_list = []

def myprint(d,title):
	for k, v in d.items():
		if isinstance(v, dict):
			myprint(v,title)
		elif k == 'extract':
			cable_dict = {'station':title,'description':v}
			cable_list.append(cable_dict)

for box in boxes:
	if box.a == None:
		continue
	title = box.a["title"]
	wiki_r = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="+title)
	parsed = json.loads(wiki_r.text.encode('ascii', 'ignore'))
	myprint(parsed,title)

cable_dict = {'cable':cable_list}
cable_json = json.dumps(cable_dict)
with open("cable.json","w") as f: 
	f.write(cable_json) 

