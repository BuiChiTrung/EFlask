import json
import os
import requests

from dotenv import load_dotenv
from google.cloud import vision
from pytube import YouTube
from twilio.rest import Client

from app.util.constants import GOOGLE_AUTH_ENDPOINT, GOOGLE_TRANSLATE_API, YOUTUBE_BASE_URL

load_dotenv()

def google_oauth(access_token):
    url = GOOGLE_AUTH_ENDPOINT
    headers = {
        'Authorization': f'Bearer  {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data={})
    return response

def google_translate(word):
    url = GOOGLE_TRANSLATE_API

    payload = f"q={word}&target=vi&source=en"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": os.getenv('X_RAPIDAPI_KEY'),
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = json.loads(requests.request("POST", url, data=payload, headers=headers).text)
    print(response)
    return response['data']['translations'][0]['translatedText']

def google_vision_api_detect_obj(image):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'API_VISION.json'
    client = vision.ImageAnnotatorClient()
    
    image = vision.Image(content = image.read())
    return client.object_localization(image=image).localized_object_annotations    

def twilio_sent_new_pass_via_sms(new_password, receiver): 
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=f'EFlask new password: {new_password}',
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=receiver
    )
    
def youtube_get_caption(video_id):
    yt = YouTube(f'{YOUTUBE_BASE_URL}?v={video_id}')
    
    caption = None
    print(yt.captions)
    if 'en' in yt.captions:    
        caption = yt.captions.get_by_language_code('en')
    elif 'a.en' in yt.captions:
        caption = yt.captions.get_by_language_code('a.en')
    
    return caption