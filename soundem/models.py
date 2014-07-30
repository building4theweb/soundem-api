from soundem import db, app
from .utils import make_password, check_password, generate_token, decode_token


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    @classmethod
    def create(cls, email, password):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def find_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def find_by_token(cls, token):
        payload = decode_token(token, app.config['SECRET_KEY'])

        if not payload or 'id' not in payload:
            return None

        return User.query.filter_by(id=payload['id']).first()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_auth_token(self):
        payload = {
            'id': self.id
        }

        return generate_token(payload, app.config['SECRET_KEY'])


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    bio = db.Column(db.Text())

    def __init__(self, name, bio):
        self.name = name
        self.bio = bio

    def __repr__(self):
        return '<Artist %r>' % self.name


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    artwork_url = db.Column(db.String(255))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist',
                             backref=db.backref('albums', lazy='dynamic'))

    def __init__(self, name, artist, artwork_url=None):
        self.name = name
        self.artist = artist

        if artwork_url:
            self.artwork_url = artwork_url

    def __repr__(self):
        return '<Album %r>' % self.name


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album',
                            backref=db.backref('songs', lazy='dynamic'))

    def __init__(self, name, album):
        self.name = name
        self.album = album

    def __repr__(self):
        return '<Song %r>' % self.name


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('favorites', lazy='dynamic'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    song = db.relationship('Song',
                           backref=db.backref('favorites', lazy='dynamic'))

    def __init__(self, song, user):
        self.song = song
        self.user = user

    def __repr__(self):
        return '<Favorite %r>' % self.song_id
