# Import Pytube module to use API
from flask import Blueprint, request
from pytube import YouTube

from app.util import json_response

video_blueprint = Blueprint('video_blueprint', __name__)

@video_blueprint.route('/', methods=['POST'])
def get_video_subtitle():
    video_url = request.form['url']
    yt = YouTube(video_url)
    
    caption = None
    print(yt.captions)
    if 'en' in yt.captions:    
        caption = yt.captions.get_by_language_code('en')
    elif 'a.en' in yt.captions:
        caption = yt.captions.get_by_language_code('a.en')

    srt_caption = caption.generate_srt_captions()
    return json_response(True, srt_caption)