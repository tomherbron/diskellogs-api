from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'diskellogs.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tom_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    register_endpoints(app)

    with app.app_context():
        from api.models import User, Record
        create_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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
