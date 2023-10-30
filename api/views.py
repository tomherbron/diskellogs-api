from flask import Blueprint, request, jsonify, session

from api.services import ApiServices

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
def get_user():
    if request.method == 'GET':
        user_id = session['user_id']
        return jsonify(ApiServices.get_user(user_id))
