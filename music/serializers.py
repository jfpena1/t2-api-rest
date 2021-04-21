from rest_framework import serializers 
from .models import Artist, Artist, Track
 
 
class ArtistSerializer(serializers.ModelSerializer):
    self = serializers.CharField(source='url', read_only=False)
    class Meta:
        model = Artist
        fields = ('id',
                  'name',
                  'age',
                  'albums',
                  'tracks',
                  'self')