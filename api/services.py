from datetime import datetime, timedelta
import jwt
from flask import jsonify, Response, session, make_response
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from api import db, app
from api.models import User, Record


class ApiServices:

    @classmethod
    def login_user(cls, credentials: dict) -> Exception | Response:
        email = credentials['email']
        password = credentials['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            response_object = {
                'status': 'error',
                'message': 'Unable to verify.'
            }
            return make_response(jsonify(response_object))
        else:
            if check_password_hash(user.password, password):
                session['logged_in'] = True

                token = jwt.encode({
                    'user_id': user.user_id,
                    'expiration': str(datetime.utcnow() + timedelta(minutes=30)),
                }, app.config['SECRET_KEY'])

                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in!',
                    'token': token
                }
                return make_response(jsonify(response_object))

    @classmethod
    def create_user(cls, user_data: dict) -> Response | User:
        email = user_data['email']
        password = user_data['password1']
        first_name = user_data['first_name']
        last_name = user_data['last_name']

        user = User.query.filter_by(email=email).first()

        if not user:
            if user_data['password1']:
                if user_data['password1'] == user_data['password2']:
                    password = generate_password_hash(user_data['password1'],
                                                      method='scrypt')

            new_user = User(email, password, first_name, last_name, None, None, None)

            try:
                db.session.add(new_user)
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.'
                }
                return make_response(jsonify(response_object))

            except SQLAlchemyError:
                db.session.rollback()
                responseObject = {
                    'status': 'error',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject))
        else:
            response_object = {
                'status': 'error',
                'message': 'User already exists. Please log in.',
            }
            return make_response(jsonify(response_object))

    @classmethod
    def get_user(cls, user_id: int) -> Response | Exception:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return user.json()
        else:
            response_object = {
                'status': 'error',
                'message': 'Unable to retrieve user.',
            }
            return make_response(jsonify(response_object))

    @classmethod
    def update_user(cls, user_id: int, user_data: dict) -> User | Exception:
        pass

    @classmethod
    def delete_user(cls, user_id: int) -> Response | Exception:
        pass

    @classmethod
    def add_record(cls, record_data: dict) -> Record | Exception:
        pass

    @classmethod
    def update_record(cls, record_id: int, record_data: dict) -> Record | Exception:
        pass

    @classmethod
    def delete_record(cls, record_id: int) -> Response | Exception:
        pass
