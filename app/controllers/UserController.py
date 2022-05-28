import os

from flask import Blueprint, request, send_from_directory, url_for
from flask_login import login_required, current_user

from app.repositories.UserRepository import UserRepository
from app.util import json_response, get_upload_file_ext_if_allowed

user_blueprint = Blueprint('user_blueprint', __name__)
repository = UserRepository('app.models.User', 'User')

UPLOAD_FOLDER = 'app/static/avatars'

@user_blueprint.route('/profile', methods=['PUT'])
@login_required
def change_avatar():
    # Verify form contains file
    if 'file' not in request.files:
        return json_response(False, 'File not exist.', 400)
    
    file = request.files['file']
    # If user doesn't select a file, an empty file without a filename is submitted
    if file.filename == '':
        return json_response(False, 'File is empty.', 400)

    file_ext = get_upload_file_ext_if_allowed(file.filename)
    if file_ext != None:
        filename = f'{current_user.id}.{file_ext}'
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return json_response(True, {'new_avatar_url': filename})
    
    return json_response(False, 'File type not allowed', 400)


@user_blueprint.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory('static/avatars', filename)