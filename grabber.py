# -*- coding: utf8 -*-
import requests
import re, urllib, json

# Method found on: http://stackoverflow.com/questions/6480723/urllib-urlencode-doesnt-like-unicode-values-how-about-this-workaround
def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

def make_url_vaga(artist, song):
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

def grab_lyrics(artista, musica):
    data = {}
    data['status'] = 'ok'
    data['url'] = None

    vaga, url = fetch_lyrics_vaga(artista, musica)
    if vaga is not None:
    	data['text'] = vaga
    	data['url'] = url

    	return json.dumps(data)

    terra, url = fetch_lyrics_terra(artista, musica)
    if terra is not None:
    	data['text'] = terra
    	data['url'] = url

    	return json.dumps(data)

    data['text'] = "not found"
    data['status'] = '404'
    return json.dumps(data)

s = str(raw_input("Enter a song name: "))
a = str(raw_input("Enter the artist of the song: "))
print grab_lyrics(a, s)
