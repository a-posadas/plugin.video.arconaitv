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

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

arconaitv_url = "https://www.arconaitv.xyz/"
mode = args.get('mode', None)

IMAGES_PATH = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'images')
DESC_PATH = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'

vars_list = {};

def evalxor(str):
	vars = str.split('^')
	index = 0
	value = vars_list[vars[index].strip()]
	while index < len(vars)-1:
		value = value^vars_list[vars[index+1].strip()]
		index=index+1
	return value

def aadecode(objscode):
	# The basic method for deobfuscating aaencoded javascript is outlined here:
	# https://stackoverflow.com/questions/8883999/how-do-these-javascript-obfuscators-generate-actual-working-code#answer-8885873
	# These are the variables 1 - 16 as on the link. I also make them into dictionary entries to avoid using eval
	#1
	ff9f03c9ff9fff89='undefined'
	vars_list.update({'ff9f03c9ff9fff89':'undefined'})
	#2
	o=ff9fff70ff9f=_=3
	vars_list.update({'o':o})
	vars_list.update({'ff9fff70ff9f':ff9fff70ff9f})
	vars_list.update({'_':_})
	#3
	c=ff9f0398ff9f=ff9fff70ff9f-ff9fff70ff9f
	vars_list.update({'ff9f0398ff9f':ff9f0398ff9f})
	vars_list.update({'c':c})
	#4
	ff9f0414ff9f = ff9f0398ff9f = o^_^o/ o^_^o
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	vars_list.update({'ff9f0398ff9f':ff9f0398ff9f})
	#5
	ff9f0414ff9f={'ff9f0398ff9f': '_' ,
					'ff9f03c9ff9fff89' : (str(ff9f03c9ff9fff89==3) + '_')[ff9f0398ff9f] ,
					'ff9fff70ff9fff89' : (str(ff9f03c9ff9fff89) + '_')[o^_^o - ff9f0398ff9f] ,
					'ff9f0414ff9fff89': (str(ff9fff70ff9f==3) +'_')[ff9fff70ff9f] }
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#6
	ff9f0414ff9f [ff9f0398ff9f] = (str(ff9f03c9ff9fff89==3) +'_') [c^_^o];
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#7
	ff9f0414ff9f ['c'] = "[object Object]" [ ff9fff70ff9f+ff9fff70ff9f-ff9f0398ff9f ]
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#8
	ff9f0414ff9f ['o'] = "[object Object]" [ff9f0398ff9f];
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#9
	ff9foff9f=ff9f0414ff9f ['c'] + ff9f0414ff9f ['o'] + (ff9f03c9ff9fff89 +'_')[ff9f0398ff9f] + (str(ff9f03c9ff9fff89==3) +'_')[ff9fff70ff9f] + "[object Object]"[ff9fff70ff9f+ff9fff70ff9f] + (str(ff9fff70ff9f==3) +'_')[ff9f0398ff9f] + (str(ff9fff70ff9f==3) +'_')[ff9fff70ff9f - ff9f0398ff9f] + ff9f0414ff9f ['c'] + "[object Object]" [ff9fff70ff9f+ff9fff70ff9f] + ff9f0414ff9f ['o'] + (str(ff9fff70ff9f==3) +'_')[ff9f0398ff9f]
	vars_list.update({'ff9foff9f':ff9foff9f})
	#10
	ff9f0414ff9f['_'] = 'Function'
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#11
	ff9f03b5ff9f = (str(ff9fff70ff9f==3)+'_')[ff9f0398ff9f] + ff9f0414ff9f['ff9f0414ff9fff89'] + '[object Object]'[ff9fff70ff9f + ff9fff70ff9f] + (str(ff9fff70ff9f==3)+'_')[o^_^o - ff9f0398ff9f] + (str(ff9fff70ff9f==3)+'_')[ff9f0398ff9f] + (ff9f03c9ff9fff89+'_')[ff9f0398ff9f]
	vars_list.update({'ff9f03b5ff9f':ff9f03b5ff9f})
	#12
	ff9fff70ff9f = ff9fff70ff9f + ff9f0398ff9f
	vars_list.update({'ff9fff70ff9f':ff9fff70ff9f})
	#13
	ff9f0414ff9f['ff9f03b5ff9f']='\\\\';
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#14
	ff9f0414ff9f['ff9f0398ff9fff89']=('[object Object]' + str(ff9fff70ff9f))[o^_^o -(ff9f0398ff9f)]
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#15
	off9fff70ff9fo=(ff9f03c9ff9fff89+'_')[c^_^o]
	vars_list.update({'off9fff70ff9fo':off9fff70ff9fo})
	#16
	ff9f0414ff9f['ff9foff9f']='\\"'
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})

	# First we split the code by semi-colon. We only want the third to last entrie because that is the obfuscated javascript. The rest we do in python.
	js_list = objscode.split(';')
	try:
		code = js_list[-3]
	except:
		return "fail"
	# unicode_escape the code so that we can use regular letters and numbers and not those funky symbols
	code = code.encode('unicode_escape')

	code = code.replace('\\u','')
	# This regular expression trims off the function calls. We aren't interested in executing the javascript.
	try:
		start = r'\(ff9f0414ff9f\) \[\'_\'\] \( \(ff9f0414ff9f\) \[\'_\'\] \('
		end = r'\) \(ff9f0398ff9f\)\) \(\'_\'\)'
		code = re.search(start+r'(.*?)'+end,code).group(1)
	except:
		return 'fail'

	#Remove all comments from code
    # see https://stackoverflow.com/questions/5989315/regex-for-match-replacing-javascript-comments-both-multiline-and-inline
	p = re.compile('\/\*.+?\*\/|\/\/.*(?=[\n\r])')
	code = p.sub('',code)

	# At this point we have the pure encoded javascript. 
	# Split all the code by plus sign.
	code_list = code.split('+')
	new_list = []
	idx=0

	# This is where the decoding happens. It is the previously declared variables concatenated, summed or subtracted and encoded in ascii and escaped.
	while idx<len(code_list):
		code = code_list[idx].strip()
		#First get all the values in single parentheses and evaluate them
		if code.startswith('(') and not code.startswith('((') and code.endswith(')') and not code.endswith('))') and not '[' in code:
			code = code.replace('(','')
			code = code.replace(')','')
			if '^' not in code:
				code = vars_list[code]
				new_list.append(code)
			else:
				value = evalxor(code)
				new_list.append(value)
			idx=idx+1
		#These are the dictionaries or objects in js. They take the form (object)[attribute]
		elif '[' in code and code.endswith(']'):
			code = code.replace('(','')
			code = code.replace(')','')
			array_rep = code.split('[')
			array_rep[1] = array_rep[1].replace(']','')
			code = vars_list[array_rep[0]][array_rep[1]]
			new_list.append(code)
			idx=idx+1
		#At the end there is an object that has another variable after it so it doesn't end in a bracket.
		# it only occurs once and it's only a quotation mars so it is safe to delete. 
		# This may be an error an this check might be unnecessary
		elif '[' in code and not code.endswith(']'):
			new_list.append(code)
			idx=idx+1
		#The stuff in double paranthesis seems to be arithmetic. 
		elif code.startswith('(('):
			while not code.endswith('))'):
				idx=idx+1
				code = code + '+' + code_list[idx].strip()
			#I just assume there will only be two values to add or subtract
			if '+' in code:
				add_this = code.split('+')
				index=0
				while index < len(add_this):
					add_this[index] = add_this[index].replace('(','').replace(')','')
					# This evaluates the xor that occur as (o^_^o) or similar
					if '^' in add_this[index]:
						add_this[index] = evalxor(add_this[index])
					else:
						add_this[index] = vars_list[add_this[index]]
					index = index+1
				code = add_this[0] + add_this[1]

			# Essentially the same as the adding loop but subtracting.
			elif '-' in code:
				sub_this = code.split('-')
				index=0
				while index < len(sub_this):
					sub_this[index] = sub_this[index].replace('(','').replace(')','')
					if '^' in sub_this[index]:
						sub_this[index] = evalxor(sub_this[index])
					else:
						sub_this[index] = vars_list[sub_this[index].strip()]
					index=index+1
				code = sub_this[0] - sub_this[1]
			new_list.append(code)
			idx=idx+1
		else:
			#The default if the variable just occurs with no parenthesis or brackets. 
			code = vars_list[code]
			new_list.append(code)
			idx=idx+1

	#put it all together. Remove the first and second elements because they are return\" 
	#we don't need the last element either, it was never evaluated, I think it comes out to a quotation mark
	#in any case unecessary
	complete = ''
	idx = 2
	while idx < len(new_list) - 1:
		complete = complete+str(new_list[idx])
		idx=idx+1

	# Since the code is escape ascii encoded, decode twice to get unicode. 
	return complete.decode('unicode_escape').decode('unicode_escape').strip()

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
				break
			else:
				code = 'fail'
		else:
			code = 'fail'
	#The second part of deobfuscation occurs here. Using module jsbeautifier. 
	if code != 'fail':
		xbmc.log(code,xbmc.LOGNOTICE)
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
