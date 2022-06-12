# Import Pytube module to use API
import os
from google.cloud import vision

from flask import Blueprint, request
from pytube import YouTube

from app.util.others import json_response, get_upload_file_ext_if_allowed
from app.util.constant import YOUTUBE_BASE_URL

third_party_blueprint = Blueprint('third_party_blueprint', __name__)


@third_party_blueprint.route('/youtube')
def get_youtube_subtitle():
    video_id = request.args.get('video_id')
    yt = YouTube(f'{YOUTUBE_BASE_URL}?v={video_id}')
    
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


@third_party_blueprint.route('/cloud-vision', methods=["POST"])
def detect_obj_from_image():    
    image = request.files['image']
    
    if image.filename == '':
        return json_response(False, 'File is empty.', 400)

    file_ext = get_upload_file_ext_if_allowed(image.filename)
    if file_ext == None:
        return json_response(False, 'File type not allowed', 400)
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'API_VISION.json'
    client = vision.ImageAnnotatorClient()
    
    image = vision.Image(content = image.read())
    objects = client.object_localization(
        image=image).localized_object_annotations

    if len(objects) == 0:
        return json_response(False, 'Can\'t detect object from image', 400)
    
    # MAX_RETURN_OBJ = 3
    # ACCEPTED_CONFIDENT = 0.75
    
    # for i in range (1, min(MAX_RETURN_OBJ, len(objects))):
    #     if objects[i].score >= ACCEPTED_CONFIDENT:
    #         res.append(objects[i].name)
        
    max_area = 0
    res = objects[0].name
    
    for object_ in objects:
        # print('\n{} (confidence: {})'.format(object_.name, object_.score))
        # for vertex in object_.bounding_poly.normalized_vertices:
        #     print(' - ({}, {})'.format(vertex.x, vertex.y))
        
        vertex = object_.bounding_poly.normalized_vertices
        obj_area = abs(vertex[0].x - vertex[1].x) * abs(vertex[2].x - vertex[3].x)
        if obj_area > max_area:
            res = object_.name
            max_area = obj_area
    
    return json_response(True, res)