import json
import requests

from flask import jsonify

def json_response(success, content, status_code = 200):
    return jsonify({'success': success, 'content': content}), status_code

def list_to_json_array(model_objs):
    for i in range(len(model_objs)):
        model_objs[i] = model_objs[i].as_dict()
    return model_objs

def tuple_to_dict(tuple):
    res = {}
    for i in range(len(tuple)):
       res.update(tuple[i].as_dict())
    return res 

def get_error_list(error):
    res = []
    for value in error.values():
        print(value)
        res.extend(value)
    return res

ALLOWED_EXTENSIONS = {'svg', 'png', 'jpg', 'jpeg', 'webp'}

def get_upload_file_ext_if_allowed(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return filename.rsplit('.', 1)[1].lower()
    return None

def google_translate(word):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = f"q={word}&target=vi&source=en"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "f692db72b2msh82608463a5858dep180a44jsnf5d1e09f2799",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = json.loads(requests.request("POST", url, data=payload, headers=headers).text)
    return response['data']['translations'][0]['translatedText']