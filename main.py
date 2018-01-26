from __future__ import unicode_literals # turns everything to unicode
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
from lib.aadecode import aadecode

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

def getShowInfo(title):
	desc_file = os.path.join(DESC_PATH, 'shows.json')
	with open(desc_file) as file:
		data = file.read()
	parsed = json.loads(data)

	for show in parsed['shows']:
		if title == show['title']:
			return show

	return {'title':title,'description':'New Show!','poster':'DefaultVideo.png'} # Should Never Get Here

def getCableInfo(title):
	desc_file = os.path.join(DESC_PATH, 'cable.json')
	with open(desc_file) as file:
		data = file.read()

	parsed = json.loads(data)

	for cable in parsed['cable']:
		if title == cable['station']:
			return cable

	return {'title':title,'description':'New Channel!','logo':'DefaultVideo.png'} # Should Never Get Here

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
	# Put in a try statement to check that the html code is what we expect it to be.
	try:
		shows = soup.find("div", id="shows")
		boxes = shows.find_all("div", class_="box-content")
	except AttributeError:
		xbmcgui.Dialog().ok("Sorry","The website has changed or we are downloading from wrong website.")
		return

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
	# Put in try statement to check that html code is what we expect it to be. 
	try:
		cable = soup.find("div", id="cable")
		boxes = cable.find_all("div", class_="box-content")
	except AttributeError:
		xbmcgui.Dialog().ok("Sorry","The website has changed or we are downloading from wrong website.")
		return

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
	try:
		movies = soup.find("div", id="movies")
		boxes = movies.find_all("div", class_="box-content")
	except AttributeError:
		xbmcgui.Dialog().ok("Sorry","The website has changed or we are downloading from wrong website.")
		return

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
				# Here is the call to the first part of the deobfuscation i.e. getting packed code
				code = aadecode(code)
				code = code.aadecode()
				if not code.replace(' ', '').startswith('eval(function(p,a,c,k,e,'):
					code = 'fail'
				break
			else:
				code = 'fail'
		else:
			code = 'fail'
	#The second part of deobfuscation occurs here. Using module jsbeautifier. 
	if code != 'fail':
		unpacked = packer.unpack(code)
		video_location = unpacked[unpacked.rfind('http'):unpacked.rfind('m3u8')+4]
		play_item = xbmcgui.ListItem(path=video_location+'|User-Agent=%s' % urllib2.quote(USER_AGENT, safe=''))
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	else:
		xbmcgui.Dialog().ok('Sorry','Could not deobfuscate the code.')

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
