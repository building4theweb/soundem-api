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

    @classmethod
    def get_all(cls):
        return Artist.query.all()


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

    @classmethod
    def get_all(cls):
        return Album.query.all()

    @classmethod
    def total_count(cls):
        return Album.query.count()


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    url = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album',
                            backref=db.backref('songs', lazy='dynamic'))

    def __init__(self, name, album, url=None, duration=None):
        self.name = name
        self.album = album

        if url:
            self.url = url

        if duration:
            self.duration = duration

    @classmethod
    def get_all(cls, user=None, is_favorite=None):
        if user and is_favorite is not None:
            favorites = Favorite.query.filter_by(user=user)
            song_ids = [favorite.song_id for favorite in favorites]

            if not song_ids and is_favorite:
                # No favorite songs to filter
                return []

            if is_favorite:
                # Filter by favorite songs
                return Song.query.filter(Song.id.in_(song_ids))
            else:
                # Filter out favorite songs
                return Song.query.filter(~Song.id.in_(song_ids))

        return Song.query.all()

    @classmethod
    def total_count(cls):
        return Song.query.count()

    @classmethod
    def total_duration(cls):
        duration = 0

        for song in Song.get_all():
            duration += song.duration

        return duration

    @classmethod
    def favorite(cls, song_id, user):
        song = Song.query.filter_by(id=song_id).first()

        if not song:
            return None, False

        favorite = Favorite.query.filter_by(song=song, user=user).first()

        if favorite:
            is_favorited = False
            db.session.delete(favorite)
        else:
            is_favorited = True
            favorite = Favorite(song=song, user=user)
            db.session.add(favorite)

        db.session.commit()

        return song, is_favorited

    def is_favorited(self, user):
        favorite = Favorite.query.filter_by(song=self, user=user).first()

        return True if favorite else False


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
