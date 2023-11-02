import jwt
from flask import Blueprint, request, Response, make_response, jsonify
from api import token_required, app
from api.services import ApiServices

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@token_required
def home() -> Response:
    auth_token = request.headers.get('Authorization')
    if auth_token:
        payload = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        return ApiServices.get_user(user_id)

    response_object = {
        'status': 'error',
        'message': 'Invalid auth token.'
    }

    return make_response(jsonify(response_object))







