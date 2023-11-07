from flask_login import UserMixin

from api import db

user_record = db.Table('user_record',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
                       db.Column('record_id', db.Integer, db.ForeignKey('record.record_id')))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    city = db.Column(db.String(50))
    records = db.relationship('Record', secondary=user_record, backref='users')

    def __init__(self, email, password, first_name,
                 last_name, address, zip_code, city):
        self.email = email
        self.password = password
        self.last_name = first_name
        self.first_name = last_name
        self.address = address
        self.zip_code = zip_code
        self.city = city

    def json(self) -> dict:
        return {
            'user_id': self.user_id,
            'email': self.email,
            'last_name': self.first_name,
            'first_name': self.last_name,
            'address': self.address,
            'zip_code': self.zip_code,
            'city': self.city,
            'records': [record.json() for record in self.records]
        }


class Record(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(10))
    title = db.Column(db.String(250))
    artist = db.Column(db.String(100))
    genre = db.Column(db.String(20))
    price = db.Column(db.Float)
    release_year = db.Column(db.Date())

    def __init__(self, ref, title, artist, genre, price, release_year):
        self.ref = ref
        self.title = title
        self.artist = artist
        self.genre = genre
        self.price = price
        self.release_year = release_year

    def json(self) -> dict:
        return {
            'record_id': self.record_id,
            'ref': self.ref,
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre,
            'price': self.price,
            'release_year': self.release_year,
        }

