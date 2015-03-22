# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from grabber import grab_lyrics
from django.utils.encoding import *

def api_view(request):
	try:
		artist = request.GET['artist']
		song = request.GET['song']
	
	except:
		artist = "none"
		song = "none"

	return HttpResponse(grab_lyrics(artist,song))

def home_view(request):
	return HttpResponseRedirect("https://play.google.com/store/apps/details?id=com.zipando.lyrics")
