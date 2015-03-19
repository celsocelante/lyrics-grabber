from django.db import models

class Lyrics(models.Model):
	artist = models.CharField(max_length=128)
	song = models.CharField(max_length=128)
	date = models.DateTimeField(auto_now_add=True)
	url = models.URLField()
	text = models.TextField()