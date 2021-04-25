from rest_framework import serializers 
from .models import Artist, Album, Track
 
 
class ArtistSerializer(serializers.ModelSerializer):
    self = serializers.CharField(source='url', read_only=False)
    albums = serializers.CharField(source='albums_url', read_only=False)
    tracks = serializers.CharField(source='tracks_url', read_only=False)
    class Meta:
        model = Artist
        fields = ('id',
                  'name',
                  'age',
                  'albums',
                  'tracks',
                  'self')

class AlbumSerializer(serializers.ModelSerializer):
    self = serializers.CharField(source='url', read_only=False)
    artist = serializers.CharField(source='artist_url', read_only=False)
    tracks = serializers.CharField(source='tracks_url', read_only=False)
    class Meta:
        model = Album
        fields = ('id',
                  'artist_id',
                  'name',
                  'genre',
                  'artist',
                  'tracks',
                  'self')

class TrackSerializer(serializers.ModelSerializer):
    self = serializers.CharField(source='url')
    artist = serializers.CharField(source='artist_url')
    album = serializers.CharField(source='album_url')

    class Meta:
        model = Track
        fields = ('id',
                  'album_id',
                  'artist_id',
                  'name',
                  'duration',
                  'times_played',
                  'artist',
                  'album',
                  'self')
        # read_only_fields = ('is_active', 'is_staff')
        extra_kwargs = {
            'artist_id': {'write_only': True},
        }
