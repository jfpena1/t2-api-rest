from base64 import b64encode

def encode_b64(data, model_type):
    if model_type == "Artist":
        raw_string = data["name"]
        encoded = b64encode(raw_string.encode()).decode('utf-8')[0:22]
    return encoded    

def get_urls(encoded_id, model_type, request):
    if model_type == "Artist":
        raw_url =  request.get_host() + request.get_full_path()
        albums_path = raw_url + "/" + encoded_id + "/albums" 
        tracks_path = raw_url + "/" + encoded_id + "/tracks"
        self_url = raw_url + "/" + encoded_id
        urls = [albums_path, tracks_path, self_url] 
    return urls