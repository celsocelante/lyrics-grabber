# Create your views here.
from django.http import HttpResponse
from grabber import grab_lyrics
from django.utils.encoding import *

def api_view(request):
	artist = request.GET['artist']
	song = request.GET['song']
	return HttpResponse(grab_lyrics(artist,song))
