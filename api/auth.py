from flask import Blueprint, Response, jsonify, session, make_response
from flask_cors import cross_origin
from flask_login import login_user
from marshmallow import fields, validate
from webargs.flaskparser import use_args

from api.services import ApiServices

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@use_args({
    'email': fields.Email(required=True),
    'password': fields.Str(required=True, validate=validate.Length(min=8)),
})
def login(credentials: dict) -> Response:
    return ApiServices.login_user(credentials)


def logout():
    pass


@auth.route('/register', methods=['POST'])
@use_args({
    'first_name': fields.Str(required=True, validate=validate.Length(min=3)),
    'last_name': fields.Str(required=True, validate=validate.Length(min=3)),
    'email': fields.Email(required=True),
    'password1': fields.Str(required=True, validate=validate.Length(min=8)),
    'password2': fields.Str(required=True, validate=validate.Length(min=8)),
})
def register(user_data: dict) -> Response:
    return ApiServices.create_user(user_data)
