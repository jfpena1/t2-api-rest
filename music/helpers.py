from base64 import b64encode
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
def encode_b64(data, model_type):
    if model_type == "Artist":
        artist_name = data["name"]
        encoded = b64encode(artist_name.encode()).decode('utf-8')[0:22]

    elif model_type == "Album":
        album_name = data["name"]
        artist_id = data["artist_id"]
        raw_string = album_name + ":" + artist_id
        encoded = b64encode(raw_string.encode()).decode('utf-8')[0:22]
    
    elif model_type == "Track":
        track_name = data["name"]
        album_id = data["album_id"]
        raw_string = track_name + ":" + album_id
        encoded = b64encode(raw_string.encode()).decode('utf-8')[0:22]

    return encoded    

def get_urls(encoded_id, model_type, request, data={}):
    if model_type == "Artist":
        raw_url =  request.get_host() + request.get_full_path()
        albums_path = raw_url + "/" + encoded_id + "/albums" 
        tracks_path = raw_url + "/" + encoded_id + "/tracks"
        self_url = raw_url + "/" + encoded_id
        urls = [albums_path, tracks_path, self_url]

    elif model_type == "Album":
        raw_url =  request.get_host()
        print(raw_url)
        artist_path = raw_url + "/artists" + "/" + data["artist_id"]
        self_url = raw_url + "/albums/" + encoded_id
        tracks_path = self_url + "/tracks" 
        urls = [artist_path, tracks_path, self_url]
    
    elif model_type == "Track":
        raw_url =  request.get_host()
        print(data)
        artist_path = raw_url + "/artists/" + data["artist_id"]
        self_url = raw_url + "/tracks/" + encoded_id
        album_path = raw_url + "/albums/" + data["album_id"]
        urls = [artist_path, album_path, self_url]

    return urls

def verify_inputs(dict_data, model_type):
    if model_type == "Artist":
        body_attributes = {"name": str, "age": int}
    elif model_type == "Album":
        body_attributes = {"name": str, "genre": str}
    elif model_type == "Track":
        body_attributes = {"name": str, "duration": int}
    
    print(set(body_attributes.keys()))
    print(set(dict_data.keys()))
    if set(body_attributes.keys()) == set(dict_data.keys()):
        input_format_is_ok = True
        for att in dict_data.keys():
            if body_attributes[att] == type(dict_data[att]):
                continue
            else:
                input_format_is_ok = False
                break
    else:
        input_format_is_ok = False
    
    return input_format_is_ok

def create_album_serializer(data, request):
    encoded_id = encode_b64(data, "Album")
    artist_path, tracks_path, self_url = get_urls(encoded_id, "Album", request, data=data)
    data["id"] = encoded_id
    data["artist"] = artist_path
    data["tracks"] = tracks_path
    data["self"] = self_url
    # print(data)
    album_serializer = AlbumSerializer(data=data)
    # print(album_serializer)
    return album_serializer

def create_track_serializer(data, request):
    encoded_id = encode_b64(data, "Track")
    artist_path, album_path, self_url = get_urls(encoded_id, "Track", request, data=data)
    data["id"] = encoded_id
    data["artist"] = artist_path
    data["album"] = album_path
    data["times_played"] = 0
    data["self"] = self_url
    print(data)
    track_serializer = TrackSerializer(data=data)
    return track_serializer