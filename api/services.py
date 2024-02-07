from flask import jsonify, Response, make_response
from sqlalchemy.exc import SQLAlchemyError

from api import db
from api.models import User, Record


class ApiServices:
    @classmethod
    def get_user(cls, user_id: int) -> Response:
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
    def add_record(cls, record_data: dict, user_id: int) -> Response:

        # Retrieve user

        user = User.query.filter_by(user_id=user_id).first()

        # Check if record already exists in user's collection

        for record in user.records:
            if record.artist == record_data['artist'] and record.title == record_data['title']:
                response_object = {
                    'status': 'error',
                    'message': 'Record already exists in user collection.'
                }
                return make_response(jsonify(response_object))

        # Check if record already exists in db

        record_from_db = Record.query.filter_by(artist=record_data['artist'], title=record_data['title']).first()

        if record_from_db:
            try:
                user.records.append(record_from_db)
                response_object = {
                    'status': 'success',
                    'message': 'Record added to user collection.'
                }
            except SQLAlchemyError as e:
                response_object = {
                    'status': 'error',
                    'message': 'Unable to add record.',
                }
            return make_response(jsonify(response_object))

        # If not, create new record in db and append it to user's collection

        else:
            new_record = Record(record_data['ref'], record_data['title'], record_data['artist'], record_data['genre'],
                                float(record_data['price']), record_data['release_year'])
            try:
                user.records.append(new_record)
                db.session.add(new_record)
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Record added successfully.'
                }
            except SQLAlchemyError as e:
                response_object = {
                    'status': 'error',
                    'message': 'Unable to retrieve user.',
                }
            return make_response(jsonify(response_object))

    @classmethod
    def update_record(cls, record_id: int, record_data: dict) -> Record | Exception:
        pass

    @classmethod
    def delete_record(cls, record_id: int) -> Response | Exception:
        pass
