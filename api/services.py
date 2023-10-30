from flask import jsonify, Response, session
from flask_login import login_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from api import db
from api.models import User, Record


class ApiServices:

    @classmethod
    def login_user(cls, email: str, password: str) -> Exception | Response:

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                session['user_id'] = user.user_id
                return user.json()
            else:
                return jsonify('error', 'Wrong password')
        else:
            return jsonify('error', 'User does not exists.')

    @classmethod
    def create_user(cls, user_data: dict) -> Exception | Response:

        email = user_data['email']
        password = user_data['password1']
        first_name = user_data['first_name']
        last_name = user_data['last_name']

        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify('message', 'User already exists.')

        if user_data['password1']:
            if user_data['password1'] == user_data['password2']:
                password = generate_password_hash(user_data['password1'],
                                                  method='scrypt')

        new_user = User(email, password, first_name, last_name, None, None, None)

        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify('message', 'Error while inserting user.')
        return new_user

    @classmethod
    def update_user(cls, user_id: int, user_data: dict) -> User | Exception:
        pass

    @classmethod
    def delete_user(cls, user_id: int) -> str | Exception:
        pass

    @classmethod
    def get_user(cls, user_id: int) -> Response | Exception:
        user = User.query.filter_by(user_id=user_id)
        return user.json()


    @classmethod
    def add_record(cls, record_data: dict) -> Record | Exception:
        pass

    @classmethod
    def update_record(cls, record_id: int, record_data: dict) -> Record | Exception:
        pass

    @classmethod
    def delete_record(cls, record_id: int) -> str | Exception:
        pass
