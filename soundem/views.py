from flask import jsonify

from soundem import app
from .models import Artist, Album, Song, Favorite


@app.route('/api/v1/artists', methods=['GET'])
def get_artists():
    artists = []

    for artist in Artist.query.all():
        artists.append({
            'id': artist.id,
            'name': artist.name,
            'bio': artist.bio,
            'albums': [album.id for album in artist.albums.all()]
        })

    return jsonify({'artists': artists})


@app.route('/api/v1/albums', methods=['GET'])
def get_albums():
    albums = []

    for album in Album.query.all():
        albums.append({
            'id': album.id,
            'name': album.name,
            'songs': [song.id for song in album.songs.all()]
        })

    return jsonify({'albums': albums})


@app.route('/api/v1/songs', methods=['GET'])
def get_songs():
    songs = []

    for song in Song.query.all():
        favorite = Favorite.query.filter_by(song=song).first()
        songs.append({
            'id': song.id,
            'name': song.name,
            'album': song.album.id,
            'favorite': True if favorite else False
        })

    return jsonify({'songs': songs})
