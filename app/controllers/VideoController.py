# Import Pytube module to use API
from flask import Blueprint, request
from pytube import YouTube

from app.util import json_response

video_blueprint = Blueprint('video_blueprint', __name__)

@video_blueprint.route('/')
def get_video_subtitle():
    video_id = request.args.get('video_id')
    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    
    caption = None
    print(yt.captions)
    if 'en' in yt.captions:    
        caption = yt.captions.get_by_language_code('en')
    elif 'a.en' in yt.captions:
        caption = yt.captions.get_by_language_code('a.en')
    
    if caption == None:
        return json_response(False, 'Subtitle is unavailable in this video', 400)

    srt_caption = caption.generate_srt_captions()
    return json_response(True, srt_caption)