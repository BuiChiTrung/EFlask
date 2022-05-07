from flask import Blueprint
from flask_login import current_user, login_required

from app.repositories.UserRepository import UserRepository
from app.util import list_to_json_array, json_response

user_blueprint = Blueprint('user_blueprint', __name__)
repository = UserRepository('app.models.User', 'User')

@user_blueprint.route('/decks')
@login_required
def show_decks():
    return json_response(True, list_to_json_array(current_user.decks.all()))
    