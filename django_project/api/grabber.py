# -*- coding: utf8 -*-
import requests
import re, urllib, json
from django.utils.encoding import *
from api.models import Lyrics

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

def make_url_vaga(artist, song):
	#artist = iri_to_uri(artist)
	try:
		data = {}
		data['artist'] = artist
		data['song'] = song
		data['nolyrics'] = 1

		data = encoded_dict(data)

		url_values = urllib.urlencode(data)
		url_api = "http://api.vagalume.com.br/search.php?" + url_values

		decoded = json.loads(requests.get(url_api).content)

		if decoded['type'] == 'exact' or decoded['type'] == 'aprox':
			music = decoded['mus'][0]
			return music['url']
		else:
			return None
	except:
		return None

def fetch_lyrics_vaga(artist, song):
	url = make_url_vaga(artist, song)

	if url is None:
		return None, None
	try:
		page = requests.get(url)

		ctype, charset = page.headers['Content-Type'].split(';')
		encoding = charset[len(' charset='):]

		lyrics = re.search(b'<div itemprop=description>(.*?)<\/div>', page.content, re.DOTALL)

		if lyrics:
			return lyrics.group(1).replace("<br/>","\n").strip(' \t\n\r').decode(encoding), url
		else:
			return None, None
	except:
		return None, None

def fetch_lyrics_terra(artist, song):
	artist = artist.replace(" ","+").lower()
	song = song.replace(" ", "+").lower()


	data = {}
	data['t'] = artist + "-" + song

	data = encoded_dict(data)

	url_values = urllib.urlencode(data)
	url = "http://letras.mus.br/winamp.php?" + url_values

	try:
		page = requests.get(url)

		ctype, charset = page.headers['Content-Type'].split(';')
		encoding = charset[len(' charset='):]
		resp = page.content

		start = resp.find("<p>")
		if start == -1:
			return None, None
		resp = resp[(start+3):]
		end = resp.find("<div id=")
		if end == -1:
			return None, None
		resp = resp[:(end)]

		# replace unwanted parts
		resp = resp.replace("<br/>", "")
		resp = resp.replace("</p>", "")
		resp = resp.replace("<p>", "\n")

		resp = resp.strip(' \t\n\r')

		return resp, url

	except:
		return None, None

'''def fetch_lyrics_az(artist, song):
	# Construct the url
	artist = artist.replace(" ","").lower()
	song = song.replace(" ", "").lower()

	url = "http://www.azlyrics.com/lyrics/%s/%s.html" % (artist, song)

	# Get url content's and search
	page = requests.get(url)
	lyrics = re.search(b'<!-- start of lyrics -->(?:\r\n)+(.+)(?:\r\n)+<!-- end of lyrics -->', page.content, re.DOTALL)

	if lyrics:
		return re.sub(r'<.+>', '', lyrics.group(1).decode('utf8'))
	else:
		return None'''

'''def fetch_lyrics_chart(artist, song):
	artist = artist.lower()
	song = song.lower()

	data = {}
	data['artist'] = artist
	data['song'] = song

	url_values = urllib.urlencode(data)
	url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist={}&song={}".format(artist,song)

	try:
		page = requests.get(url)

		ctype, charset = page.headers['Content-Type'].split(';')
		encoding = charset[len(' charset='):]

		id = re.search(b'<LyricId>(.*?)<\/LyricId>', page.content, re.DOTALL)
		if id == "0":
			return None

		lyrics = re.search(b'<Lyric>(.*?)<\/Lyric>', page.content, re.DOTALL)

		if lyrics:
			return lyrics.group(1).replace("<br/>","\n").decode(encoding)
		else:
			return None
	except:
		return None'''


'''def fetch_lyrics_wikia(artist, song):
	artist = uri_to_iri(artist.replace(" ","_").title())
	song = song.replace(" ", "_").title()
	MARKER_NOLYRICS = 'PUT LYRICS HERE'
	url = "http://lyrics.wikia.com/index.php?title=%s:%s&action=edit" % (artist, song)

	try:
		page = requests.get(url)

		ctype, charset = page.headers['Content-Type'].split(';')
		encoding = charset[len(' charset='):]

		lyrics = re.search(b'&lt;lyrics>(.*?)&lt;/lyrics>', page.content, re.DOTALL)


		if lyrics.group(1).find(MARKER_NOLYRICS) > -1:
			return None

		if lyrics:
			return lyrics.group(1)
		else:
			return None
	except:
		return None'''

def grab_lyrics(artista, musica):
	data = {}
	data['status'] = 'ok'
	data['source'] = 'external'
	data['url'] = None

	database = Lyrics.objects.filter(artist__icontains=artista,song__icontains=musica)[:1]

	if database.count() is 1:
		data['text'] = database[0].text
		data['source'] = 'database'
		data['url'] = database[0].url
		return json.dumps(data)



	vaga, url = fetch_lyrics_vaga(artista, musica)

	if vaga is not None:
		data['text'] = vaga
		data['url'] = url

		lyric_object = Lyrics(artist=artista, song=musica, text=vaga)
		lyric_object.save()

		return json.dumps(data)
	
	data['text'] = "not found"
	data['status'] = '404'
	data['source'] = None
	return json.dumps(data)