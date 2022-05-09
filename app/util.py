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