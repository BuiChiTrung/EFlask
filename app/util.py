from flask import jsonify

def json_response(success, content, status_code = 200):
    return jsonify({'success': success, 'content': content}), status_code