from django.db import models


class Artist(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    albums = models.CharField(max_length=50)
    tracks = models.CharField(max_length=50)
    url = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Album(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artist_url = models.CharField(max_length=50)
    tracks = models.CharField(max_length=50)
    url = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Track(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=50)
    duration = models.IntegerField()
    times_played = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artist_url = models.CharField(max_length=50)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    album_url = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    def __str__(self):
        return self.name