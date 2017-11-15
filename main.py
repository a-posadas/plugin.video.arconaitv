import sys
import urllib
import urllib2
import urlparse
import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
from bs4 import BeautifulSoup
import jsbeautifier.unpackers.packer as packer
import os.path
import json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
arconaitv_url = "https://www.arconaitv.xyz/"
mode = args.get('mode', None)

IMAGES_PATH = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'images')
DESC_PATH = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'

def build_url(query):
	return base_url + '?' + urllib.urlencode(query)

def duf(d,e,f):
	g = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/")
	h = g[0:e]
	i = g[0:f]
	d = list(d)[::-1]
	j = 0
	for c,b in enumerate(d):
		if b in h:
			j = j + h.index(b)*e**c

	k = ""
	while j > 0:
		k = i[j%f] + k
		j = (j - (j%f))//f

	return int(k) or 0

def hunter(h,u,n,t,e,r):
	r = "";
	i = 0
	while i < len(h):
		j = 0
		s = ""
		while h[i] is not n[e]:
			s = ''.join([s,h[i]])
			i = i + 1

		while  j < len(n):
			s = s.replace(n[j],str(j))
			j = j + 1

		r = ''.join([r,''.join(map(chr, [duf(s,e,10) - t]))])
		i = i + 1
	return r

if mode is None:
	url = build_url({'mode': 'shows'})
	li = xbmcgui.ListItem("24/7 TV Shows")
	shows_img = os.path.join(IMAGES_PATH, 'tv.png')
	li.setArt({'thumb': shows_img, 'poster': shows_img})
	il={"plot": "24/7 Streams of Popular Television Shows" }
	li.setInfo(type='video', infoLabels=il)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

	url = build_url({'mode': 'cable'})
	li = xbmcgui.ListItem("Cable")
	cable_img = os.path.join(IMAGES_PATH, 'cable.jpg')
	li.setArt({'thumb': cable_img, 'poster': cable_img})
	il={"plot": "Cable Television Channels" }
	li.setInfo(type='video', infoLabels=il)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

	url = build_url({'mode': 'movies'})
	li = xbmcgui.ListItem("Movies")
	movies_img = os.path.join(IMAGES_PATH, 'movies.png')
	li.setArt({'thumb': movies_img, 'poster': movies_img})
	il={"plot": "24/7 Streams of Movies by Genre" }
	li.setInfo(type='video', infoLabels=il)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'shows':
	arconaitv_r = requests.get(arconaitv_url+"index.php")
	html_text = arconaitv_r.text.encode('ascii', 'ignore')
	soup = BeautifulSoup(html_text, 'html.parser')
	shows = soup.find("div", id="shows")
	boxes = shows.find_all("div", class_="box-content")

	desc_file = os.path.join(DESC_PATH, 'shows.json')
	with open(desc_file) as file:
		data = file.read()

	parsed = json.loads(data)
	listItemlist = []
	for box in boxes:
		if box.a == None:
			continue

		url = build_url({'mode': 'play', 'selection': box.a["href"]})
		title = box.a["title"]
		li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png')
		for show in parsed['shows']:
			if title == show['show']:
				il={"plot": show['description'],"plotoutline":show['description']}
		li.setInfo(type='video', infoLabels=il)
		listItemlist.append([url,li,False])

	listLength = len(listItemlist)
	xbmcplugin.addDirectoryItems(handle=addon_handle, items=listItemlist, totalItems=listLength)
	xbmcplugin.setContent(addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'cable':
	arconaitv_r = requests.get(arconaitv_url+"index.php")
        html_text = arconaitv_r.text.encode('ascii', 'ignore')
        soup = BeautifulSoup(html_text, 'html.parser')
        cable = soup.find("div", id="cable")
        boxes = cable.find_all("div", class_="box-content")

        desc_file = os.path.join(DESC_PATH, 'cable.json')
        with open(desc_file) as file:
                data = file.read()

        parsed = json.loads(data)
        listItemlist = []
        for box in boxes:
                if box.a == None:
                        continue

                url = build_url({'mode': 'play', 'selection': box.a["href"]})
                title = box.a["title"]
                li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png')
                for station in parsed['cable']:
                        if title == station['station']:
                                il={"plot": station['description'],"plotoutline":station['description']}
                li.setInfo(type='video', infoLabels=il)
                listItemlist.append([url,li,False])

        listLength = len(listItemlist)
        xbmcplugin.addDirectoryItems(handle=addon_handle, items=listItemlist, totalItems=listLength)
        xbmcplugin.setContent(addon_handle, 'tvshows')
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'movies':
	arconaitv_r = requests.get(arconaitv_url+"index.php")
	html_text = arconaitv_r.text.encode('ascii', 'ignore')
	soup = BeautifulSoup(html_text, 'html.parser')
	movies = soup.find("div", id="movies")
        boxes = movies.find_all("div", class_="box-content")

        desc_file = os.path.join(DESC_PATH, 'movies.json')
        with open(desc_file) as file:
                data = file.read()

        parsed = json.loads(data)
        listItemlist = []
        for box in boxes:
                if box.a == None:
                        continue

                url = build_url({'mode': 'play', 'selection': box.a["href"]})
                title = box.a["title"]
                li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png')
                for movie in parsed['movies']:
                        if title == movie['movie']:
                                il={"plot": movie['description'],"plotoutline":movie['description']}
                li.setInfo(type='video', infoLabels=il)
                listItemlist.append([url,li,False])

        listLength = len(listItemlist)
        xbmcplugin.addDirectoryItems(handle=addon_handle, items=listItemlist, totalItems=listLength)
        xbmcplugin.setContent(addon_handle, 'movies')
        xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'play':
	selection = args.get('selection',None)
	r = requests.get(arconaitv_url+selection[0])
	html_text = r.text.encode('ascii', 'ignore')
	soup = BeautifulSoup(html_text, 'html.parser')
	scripts = soup.find_all('script')
	for script in scripts:
		if script.string is not None:
			if "document.getElementsByTagName('video')[0].volume = 1.0;" in script.string:
				idx = script.string.index("var")
				code = script.string[idx:]
				params = code[code.index('return r}(')+10:code.rfind('))')]
				params = params.replace('"','')
				params = params.split(',')
				for idx,param in enumerate(params):
					if param.isdigit():
						params[idx] = int(param)
				code = hunter(*params)
	unpacked = packer.unpack(code)
	xbmc.log(msg=unpacked,level=xbmc.LOGNOTICE)
	video_location = unpacked[unpacked.rfind('http'):unpacked.rfind('m3u8')+4]
	xbmc.log(msg=video_location,level=xbmc.LOGNOTICE)
	xbmc.Player().play(item=video_location+'|User-Agent=%s' % urllib2.quote(USER_AGENT, safe=''))
