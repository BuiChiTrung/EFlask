from flask import jsonify

def json_response(success, content, status_code = 200):
    return jsonify({'success': success, 'content': content}), status_code

def json_array_convert(model_objs):
    for i in range(len(model_objs)):
        model_objs[i] = model_objs[i].as_dict()
    return model_objs