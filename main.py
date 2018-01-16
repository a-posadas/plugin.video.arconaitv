from __future__ import unicode_literals
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
import re

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

#1
ff9f03c9ff9fff89 = "undefined"
#2
o=ff9fff70ff9f=_=3
#3
c=ff9f0398ff9f=ff9fff70ff9f-ff9fff70ff9f
#4
ff9f0414ff9f = ff9f0398ff9f = o^_^o/ o^_^o
#5
ff9f0414ff9f={'ff9f0398ff9f': '_' ,
				'ff9f03c9ff9fff89' : (str(ff9f03c9ff9fff89==3) + '_')[ff9f0398ff9f] ,
				'ff9fff70ff9fff89' : (str(ff9f03c9ff9fff89) + '_')[o^_^o - ff9f0398ff9f] ,
				'ff9f0414ff9fff89': (str(ff9fff70ff9f==3) +'_')[ff9fff70ff9f] }
#6
ff9f0414ff9f [ff9f0398ff9f] =(str(ff9f03c9ff9fff89==3) +'_') [c^_^o];
#7
ff9f0414ff9f ['c'] = "[object Object]" [ ff9fff70ff9f+ff9fff70ff9f-ff9f0398ff9f ]
#8
ff9f0414ff9f ['o'] = "[object Object]"[ff9f0398ff9f]
#9
ff9foff9f = ff9f0414ff9f['c'] + ff9f0414ff9f['o'] + (ff9f03c9ff9fff89 + '_')[ff9f0398ff9f] + (str(ff9f03c9ff9fff89==3) + '_')[ff9fff70ff9f] + "[object Object]"[ff9fff70ff9f+ff9fff70ff9f] + (str(ff9fff70ff9f==3) + '_')[ff9f0398ff9f] + (str(ff9fff70ff9f==3) + '_')[ff9fff70ff9f - ff9f0398ff9f] + ff9f0414ff9f['c'] + "[object Object]"[ff9fff70ff9f+ff9fff70ff9f] + ff9f0414ff9f['o'] + (str(ff9fff70ff9f==3) + '_')[ff9f0398ff9f]
#10
ff9f0414ff9f['_'] = 'Function'
#11
ff9f03b5ff9f = (str(ff9fff70ff9f==3)+'_')[ff9f0398ff9f] + ff9f0414ff9f['ff9f0414ff9fff89'] + '[object Object]'[ff9fff70ff9f + ff9fff70ff9f] + (str(ff9fff70ff9f==3)+'_')[o^_^o - ff9f0398ff9f] + (str(ff9fff70ff9f==3)+'_')[ff9f0398ff9f] + (ff9f03c9ff9fff89+'_')[ff9f0398ff9f]
#12
ff9fff70ff9f = ff9fff70ff9f + ff9f0398ff9f
#13
ff9f0414ff9f['ff9f03b5ff9f']='\\\\';
#14
ff9f0414ff9f['ff9f0398ff9fff89']=('[object Object]' + str(ff9fff70ff9f))[o^_^o -(ff9f0398ff9f)]
#15
off9fff70ff9fo=(ff9f03c9ff9fff89+'_')[c^_^o];
#16
ff9f0414ff9f['ff9foff9f']='\\"'

def aadecode(code):
	js_list = code.split(';')
	code = js_list[-3]
	code = code.encode('unicode_escape')
	code = code.replace('\\u','')
	code = code[45:-7]

	code = code.replace('[','["')
	code = code.replace(']','"]')
	p = re.compile('\/\*.+?\*\/|\/\/.*(?=[\n\r])')
	code = p.sub('',code)

	code_list = code.split('+')

	idx = 0
	eval_this = code_list[idx]
	complete = str(iseval(eval_this))
	complete = ''
	while idx < len(code_list)-1:
		if iseval(eval_this):
			complete = complete + str(eval(eval_this))
			idx = idx + 1
			eval_this = str(code_list[idx])
		else:
			eval_this = eval_this + '+' + str(code_list[idx+1])
			idx = idx + 1

	complete = complete.replace('return\\"','')
	complete = complete.replace('\\\\','\\')
	complete = complete.decode('unicode_escape')
	return complete

def iseval(character):
	try:
		eval(character)
		return True
	except:
		return False

def getShowInfo(title):
	desc_file = os.path.join(DESC_PATH, 'shows.json')
	with open(desc_file) as file:
		data = file.read()

	parsed = json.loads(data)

	for show in parsed['shows']:
		if title == show['title']:
			return show

	return {'title':title+' wtf','description':'wtf','poster':'DefaultVideo.png'} # Should Never Get Here

def getCableInfo(title):
	desc_file = os.path.join(DESC_PATH, 'cable.json')
	with open(desc_file) as file:
		data = file.read()

	parsed = json.loads(data)

	for cable in parsed['cable']:
		if title == cable['station']:
			return cable

	return {'title':title+' wtf','description':'wtf','logo':'DefaultVideo.png'} # Should Never Get Here

def list_categories():
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

def list_shows():
	arconaitv_r = requests.get(arconaitv_url+"index.php")
	html_text = arconaitv_r.text.encode('ascii', 'ignore')
	soup = BeautifulSoup(html_text, 'html.parser')
	shows = soup.find("div", id="shows")
	boxes = shows.find_all("div", class_="box-content")

	listItemlist = []
	for box in boxes:
		if box.a == None:
			continue

		url = build_url({'mode': 'play', 'selection': box.a["href"]})
		title = box.a["title"].strip()
		showInfo = getShowInfo(title)
		li = xbmcgui.ListItem(showInfo['title'], iconImage=showInfo['poster'])
		il={"Title": title,"mediatype":"video","plot": showInfo['description'],"plotoutline": showInfo['description']}
		li.setProperty('IsPlayable', 'true')
		li.setInfo(type='video', infoLabels=il)
		li.setArt({ 'poster': showInfo['poster'], 'banner' : showInfo['poster'] })
		listItemlist.append([url,li,False])

	listLength = len(listItemlist)
	xbmcplugin.addDirectoryItems(handle=addon_handle, items=listItemlist, totalItems=listLength)
	xbmcplugin.setContent(addon_handle, 'tvshows')
	xbmcplugin.endOfDirectory(addon_handle)

def list_cable():
	arconaitv_r = requests.get(arconaitv_url+"index.php")
        html_text = arconaitv_r.text.encode('ascii', 'ignore')
        soup = BeautifulSoup(html_text, 'html.parser')
        cable = soup.find("div", id="cable")
        boxes = cable.find_all("div", class_="box-content")

        listItemlist = []
        for box in boxes:
                if box.a == None:
                        continue

                url = build_url({'mode': 'play', 'selection': box.a["href"]})
                title = box.a["title"].strip()
		cableInfo = getCableInfo(title)
                li = xbmcgui.ListItem(title, iconImage=cableInfo['logo'])
		il={"Title": title,"mediatype":"video","plot": cableInfo['description'],"plotoutline": cableInfo['description']}
		li.setProperty('IsPlayable', 'true')
                li.setInfo(type='video', infoLabels=il)
                listItemlist.append([url,li,False])

        listLength = len(listItemlist)
        xbmcplugin.addDirectoryItems(handle=addon_handle, items=listItemlist, totalItems=listLength)
        xbmcplugin.setContent(addon_handle, 'tvshows')
        xbmcplugin.endOfDirectory(addon_handle)

def list_movies():
	arconaitv_r = requests.get(arconaitv_url+"index.php")
	html_text = arconaitv_r.text.encode('ascii','ignore')
	soup = BeautifulSoup(html_text, 'html.parser')
	movies = soup.find("div", id="movies")
        boxes = movies.find_all("div", class_="box-content")

        listItemlist = []
        for box in boxes:
                if box.a == None:
                        continue

                url = build_url({'mode': 'play', 'selection': box.a["href"]})
                title = box.a["title"]
                li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png')
		il={"Title": title,"mediatype":"video"}
		li.setProperty('IsPlayable', 'True')
		li.setProperty('mimetype', 'application/x-mpegURL') 
                li.setInfo(type='video', infoLabels=il)
                listItemlist.append([url,li,False])

        listLength = len(listItemlist)
        xbmcplugin.addDirectoryItems(handle=addon_handle, items=listItemlist, totalItems=listLength)
        xbmcplugin.setContent(addon_handle, 'movies')
        xbmcplugin.endOfDirectory(addon_handle)


def play_video(selection):
	r = requests.get(arconaitv_url+selection)
	html_text = r.text
	soup = BeautifulSoup(html_text, 'html.parser')
	scripts = soup.find_all('script')
	for script in scripts:
		if script.string is not None:
			if "document.getElementsByTagName('video')[0].volume = 1.0;" in script.string:
				code = script.string
				code = aadecode(code)

				xbmc.log(code, xbmc.LOGNOTICE)
	unpacked = packer.unpack(code)
	video_location = unpacked[unpacked.rfind('http'):unpacked.rfind('m3u8')+4]
	play_item = xbmcgui.ListItem(path=video_location+'|User-Agent=%s' % urllib2.quote(USER_AGENT, safe=''))
	xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def router(params):
	if params:
		if params['mode'][0] == 'shows':
			list_shows()
		elif params['mode'][0] == 'cable':
			list_cable()
		elif params['mode'][0] == 'movies':
			list_movies()
		elif params['mode'][0] == 'play':
			play_video(params['selection'][0])
	else:
		list_categories()

if __name__ == '__main__':
	router(args)
