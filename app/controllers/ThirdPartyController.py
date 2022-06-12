# Import Pytube module to use API
import os

from flask import Blueprint, request

from app.util.others import json_response, get_upload_file_ext_if_allowed
from app.util.services import google_vision_api_detect_obj, youtube_get_caption

third_party_blueprint = Blueprint('third_party_blueprint', __name__)

@third_party_blueprint.route('/youtube')
def get_youtube_subtitle():
    caption = youtube_get_caption(request.args.get('video_id'))
    
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
    
    objects = google_vision_api_detect_obj(image)
    if len(objects) == 0:
        return json_response(False, 'Can\'t detect object from image', 400)
        
    return json_response(True, get_obj_take_most_space(objects))


def get_obj_take_most_space(objects):
    max_area = 0
    res = objects[0].name
    
    for object_ in objects:
        vertex = object_.bounding_poly.normalized_vertices
        obj_area = abs(vertex[0].x - vertex[1].x) * abs(vertex[2].x - vertex[3].x)
        if obj_area > max_area:
            res = object_.name
            max_area = obj_area
    
    return res