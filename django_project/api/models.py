from django.db import models

class Lyrics(models.Model):
	artist = models.CharField(max_length=128)
	song = models.CharField(max_length=128)
	text = models.TextField()