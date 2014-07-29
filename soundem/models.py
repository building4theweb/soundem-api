from soundem import db


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
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    song = db.relationship('Song',
                           backref=db.backref('favorites', lazy='dynamic'))

    def __init__(self, song):
        self.song = song

    def __repr__(self):
        return '<Favorite %r>' % self.song_id
