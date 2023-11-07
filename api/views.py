import jwt
from flask import Blueprint, request, Response, make_response, jsonify
from marshmallow import fields, validate
from webargs.flaskparser import use_args

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


@views.route('/add-record', methods=['PUT'])
@token_required
@use_args({
    'ref': fields.Str(required=True, validate=validate.Length(min=1, max=6)),
    'title': fields.Str(required=True, validate=validate.Length(min=3)),
    'artist': fields.Str(required=True, validate=validate.Length(min=1)),
    'genre': fields.Str(required=True, validate=validate.Length(min=3)),
    'price': fields.Str(required=True),
    'release_year': fields.Date(required=True)
})
def add_record(record_data: dict) -> Response:
    auth_token = request.headers.get('Authorization')
    if auth_token:
        payload = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        return ApiServices.add_record(record_data, user_id)

    response_object = {
        'status': 'error',
        'message': 'Invalid auth token.'
    }
    return make_response(jsonify(response_object))





