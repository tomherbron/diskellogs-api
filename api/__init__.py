from functools import wraps
from os import path

import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from api.exceptions import JWTException

db = SQLAlchemy()
DB_NAME = 'diskellogs.db'
app = Flask(__name__)


def create_app():
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = 'tom_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    register_endpoints(app)

    with app.app_context():
        from api.models import User, Record
        create_database()

    return app


def create_database():
    if not path.exists('app/' + DB_NAME):
        db.create_all()
        print('Database created!')


def register_endpoints(app):
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify('error', 'Token is missing.'), 403

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except JWTException:
            return jsonify('error', 'Invalid token')
    return decorated
