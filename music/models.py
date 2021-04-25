from django.db import models

# en heroku migraciones:
#heroku run python manage.py migrate

class Artist(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    albums_url = models.CharField(max_length=200, default="")
    tracks_url = models.CharField(max_length=200, default="")
    url = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name

class Album(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE, default="")
    artist_url = models.CharField(max_length=200, default="") #url
    tracks_url = models.CharField(max_length=200, default="")
    url = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name

class Track(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    times_played = models.IntegerField()
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE, default="")
    artist_url = models.CharField(max_length=200, default="") #url
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, default="")
    album_url = models.CharField(max_length=200, default="") #url
    url = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name