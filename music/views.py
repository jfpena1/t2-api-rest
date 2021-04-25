from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Artist, Album, Track
from .helpers import encode_b64, get_urls, verify_inputs, create_album_serializer, create_track_serializer


def index(request):
    return HttpResponse("Hello, world. You're at the music index.")

################################# CRUD Artist #################################

@api_view(['GET', 'POST'])
def artists(request):
    if request.method == 'GET':
        all_artists = Artist.objects.all()
        artists_serializer = ArtistSerializer(all_artists, many=True)
        print(str(artists_serializer))
        return JsonResponse(artists_serializer.data, safe=False, 
        status=status.HTTP_200_OK)
 
    elif request.method == 'POST':
        artist_data = JSONParser().parse(request)
        print(artist_data)
        # Check input format
        if not verify_inputs(artist_data, "Artist"):
            print("invalid inputs!")
            return JsonResponse({'message':"Inputs invalidos"}, status=status.HTTP_400_BAD_REQUEST)

        encoded_id = encode_b64(artist_data, "Artist")
        # Check if exists already:
        if Artist.objects.filter(pk=encoded_id).first() is not None:
            print("artista existe")
            return JsonResponse({ 'message': "Artista ya existe!"}, status=status.HTTP_409_CONFLICT)
        
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
        else:
            return JsonResponse(artist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def artist(request, artist_id):
    try:
        selected_artist = Artist.objects.get(pk=artist_id)
    except:
        return JsonResponse({'message': 'The artist does not exist'}, 
        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        artist_serializer = ArtistSerializer(selected_artist)
        return JsonResponse(artist_serializer.data, safe=False, 
        status=status.HTTP_200_OK)

    elif request.method == 'DELETE': 
        name = selected_artist.name
        selected_artist.delete()
        return JsonResponse({'message': f'Artist {name} was deleted successfully!'}, 
        status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET', 'POST'])
def artist_details(request, artist_id, detail):
    try:
        selected_artist = Artist.objects.get(pk=artist_id)
        data = JSONParser().parse(request)    
        print(f"Artist: {selected_artist}")
    except:
        return JsonResponse({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if detail == "albums":
            return get_artist_albums(selected_artist)

        elif detail == "tracks":
            return get_artist_tracks(selected_artist)
        
    elif request.method == 'POST':
        create_artist_album(data, selected_artist, request)
            
@api_view(['PUT'])
def artist_play_tracks(request, artist_id):
    try:
        selected_artist = Artist.objects.get(pk=artist_id)
        print(f"Album: {selected_artist}")
    except:
        return JsonResponse({'message': 'The artist does not exist'}, 
        status=status.HTTP_404_NOT_FOUND)
    
    artist_tracks = Track.objects.filter(artist_id=selected_artist)
    print(artist_tracks)
    for track in artist_tracks:
        track.times_played += 1
        track.save()
    return JsonResponse(
        {'message': 
        f'Tracks were played!'}, 
        safe=False, 
        status=status.HTTP_200_OK
    )
       
def get_artist_albums(selected_artist):
    print("albums! of an artist")
    albums = Album.objects.filter(artist_id=selected_artist.id)
    serialized_albums = [AlbumSerializer(album).data for album in albums]
    return JsonResponse(serialized_albums, safe=False, 
    status=status.HTTP_200_OK)

def get_artist_tracks(selected_artist):
    print("tracks! of an artist")
    tracks = Track.objects.filter(artist_id=selected_artist.id)
    # print(AlbumSerializer(album).data)
    serialized_tracks = [TrackSerializer(track).data for track in tracks]
    print(serialized_tracks)
    return JsonResponse(serialized_tracks, safe=False, 
    status=status.HTTP_200_OK)

def create_artist_album(data, selected_artist, request):
    if not verify_inputs(data, "Album"):
        return JsonResponse({'message':"Inputs de album invalidos"}, 
        status=status.HTTP_400_BAD_REQUEST)

    data["artist_id"] = selected_artist.id
    encoded_id = encode_b64(data, "Album")

    if Album.objects.filter(id=encoded_id).first() is not None:
        print(f"Album ya existe")
        return JsonResponse({ 'message': f"Album ya existe!"}, 
        status=status.HTTP_409_CONFLICT)

    album_serializer = create_album_serializer(data, request)
    
    if album_serializer.is_valid():
        album_serializer.save()
        return JsonResponse(album_serializer.data, status=status.HTTP_201_CREATED)

    return JsonResponse(album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def edit_artist_reproductions(request):
    pass

################################# CRUD Album #################################

@api_view(['GET'])
def albums(request):
    all_albums = Album.objects.all()
    albums_serializer = AlbumSerializer(all_albums, many=True)
    print(str(albums_serializer))
    return JsonResponse(albums_serializer.data, safe=False, 
    status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def album(request, album_id):
    print("Album view")
    try:
        selected_album = Album.objects.get(pk=album_id)
    except:
        return JsonResponse({'message': 'The album does not exist'}, 
        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        album_serializer = ArtistSerializer(selected_album)
        print(str(album_serializer))
        return JsonResponse(album_serializer.data, safe=False, 
        status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        name = selected_album.name
        selected_album.delete()
        return JsonResponse({'message': f'Album {name} was deleted successfully!'}, 
        status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def album_tracks(request, album_id, detail):
    try:
        selected_album = Album.objects.get(pk=album_id)
        print(f"Album: {selected_album}")
    except:
        return JsonResponse({'message': 'The album does not exist'}, 
        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return get_album_tracks(selected_album)
        
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        return create_album_track(data, selected_album, request)

@api_view(['PUT'])
def album_play_tracks(request, album_id):
    try:
        selected_album = Album.objects.get(pk=album_id)
        print(f"Album: {selected_album}")
    except:
        return JsonResponse({'message': 'The album does not exist'}, 
        status=status.HTTP_404_NOT_FOUND)
    
    album_tracks = Track.objects.filter(album_id=selected_album)
    print(album_tracks)
    for track in album_tracks:
        track.times_played += 1
        track.save()
    return JsonResponse(
        {'message': 
        f'Tracks were played!'}, 
        safe=False, 
        status=status.HTTP_200_OK
    )


def get_album_tracks(selected_album):
    print("tracks! of an album")
    tracks = Track.objects.filter(album_id=selected_album.id)
    serialized_tracks = [TrackSerializer(track).data for track in tracks]
    print(serialized_tracks)
    return JsonResponse(serialized_tracks, safe=False, 
    status=status.HTTP_200_OK)

def create_album_track(data, selected_album, request):
    if not verify_inputs(data, "Track"):
        print("invalid inputs!")
        return JsonResponse({'message':"Inputs invalidos"}, 
        status=status.HTTP_400_BAD_REQUEST)

    data["artist_id"] = selected_album.artist_id.id   
    data["album_id"] = selected_album.id
    encoded_id = encode_b64(data, "Track")

    if Track.objects.filter(id=encoded_id).first() is not None:
        print(f"Track ya existe")
        return JsonResponse({ 'message': f'Track ya existe!'}, status=status.HTTP_409_CONFLICT)

    track_serializer = create_track_serializer(data, request)
    if track_serializer.is_valid():
        track_serializer.save()
        return JsonResponse(track_serializer.data, status=status.HTTP_201_CREATED)

    return JsonResponse(track_serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        
################################# CRUD Track #################################

@api_view(['GET'])
def tracks(request):
    all_tracks = Track.objects.all()
    tracks_serializer = TrackSerializer(all_tracks, many=True)
    return JsonResponse(tracks_serializer.data, safe=False, 
    status=status.HTTP_200_OK)

@api_view(['GET', 'DELETE'])
def track(request, track_id):
    print("holi")
    try:
        selected_track = Track.objects.get(pk=track_id)
    except:
        return JsonResponse({'message': 'The tracks does not exist'}, 
        status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        print("GET de track wewqdewhgh")
        print(selected_track)
        track_serializer = TrackSerializer(selected_track, 
        many=True)
        print(track_serializer)
        return JsonResponse(track_serializer, 
        status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        track_name = selected_track.name
        selected_track.delete()
        return JsonResponse({'message': f'Track {track_name} was deleted successfully!'}, 
        status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def track_play(request, track_id):
    try:
        selected_track = Track.objects.get(pk=track_id)
    except:
        return JsonResponse({'message': 'The tracks does not exist'}, 
        status=status.HTTP_404_NOT_FOUND)
    
    selected_track.times_played += 1
    selected_track.save()
    name = selected_track.name

    return JsonResponse(
        {'message': 
        f'Track {name} was played!. It has been played {selected_track.times_played} times'}, 
        safe=False, 
        status=status.HTTP_200_OK
    )


