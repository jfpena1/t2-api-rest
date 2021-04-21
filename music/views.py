from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .models import Artist
from .serializers import ArtistSerializer
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Artist
from .helpers import encode_b64, get_urls
# Create your views here.
# returning all objects -----------------
#  all_entries = Entry.objects.all()
# returnin filetred objects ---------------
# Entry.objects.filter(pub_date__year=2006)
# getting one objetc: ------------------
# one_entry = Entry.objects.get(pk=1) o Blog.objects.get(id=14) 


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

################################# CRUD Artist #################################

@api_view(['GET', 'POST'])
def artists(request):
    if request.method == 'GET':
        all_artists = Artist.objects.all()
        artists_serializer = ArtistSerializer(all_artists, many=True)
        print(str(artists_serializer))
        return JsonResponse(artists_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        artist_data = JSONParser().parse(request)
        encoded_id = encode_b64(artist_data, "Artist")
        albums, tracks, self_url = get_urls(encoded_id, "Artist", request)
        artist_data["id"] = encoded_id
        artist_data["albums"] = albums
        artist_data["tracks"] = tracks
        artist_data["self"] = self_url
        print(artist_data)
        artist_serializer = ArtistSerializer(data=artist_data)
        print(artist_serializer)
        if artist_serializer.is_valid():
            artist_serializer.save()
            return JsonResponse(artist_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(artist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def artist(request, artist_id):
    if request.method == 'GET':
        try:
            selected_artist = Artist.objects.get(pk=artist_id)
        except:
            return JsonResponse({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        artist_serializer = ArtistSerializer(selected_artist)
        print(str(artist_serializer))
        return JsonResponse(artist_serializer.data, safe=False)

    elif request.method == 'DELETE':
        try: 
            artist_to_be_deleted = Artist.objects.get(pk=artist_id)
        except: 
            return JsonResponse({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND)

        artist_to_be_deleted.delete()
        return JsonResponse({'message': f'Artist {artist_to_be_deleted} was deleted successfully!'}, 
        status=status.HTTP_204_NO_CONTENT)
        

def get_artist_albums(request):
    pass

def get_artist_tracks(request):
    pass
#PUT
def edit_artist_reproductions(request):
    pass
#DELTE
def delete_artist(request):
    pass

################################# CRUD Album #################################

#POST
def create_album(request):
    # b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    #  b.save()
    pass

#GET
def get_albums(request):
    pass

def get_album(request):
    pass

def get_album_tracks(request):
    pass

#PUT
def edit_album_reproductions(request):
    pass

#DELETE
def delete_album(request):
    pass

################################# CRUD Track #################################

#POST
def create_track(request):
    # b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    #  b.save()
    pass

#GET
def get_track(request):
    pass

#PUT
def edit_track_reproductions(request):
    pass

#DELETE
def delete_track(request):
    pass

# ERROR 404
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})