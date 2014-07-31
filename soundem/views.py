from flask import g, jsonify, request, abort

from flask_cors import cross_origin

from soundem import app
from .decorators import auth_token_required
from .models import Artist, Album, Song, User


@app.route('/api/v1/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    errors = {}

    if not email:
        errors['email'] = 'Field is required.'

    if not password:
        errors['password'] = 'Field is required.'

    user = User.find_by_email(email)

    if not user:
        errors['email'] = 'User does not exist.'
    elif not user.check_password(password):
        errors['password'] = 'Invalid password.'

    if errors:
        return jsonify({'errors': errors}), 400

    user_data = {
        'id': user.id,
        'email': user.email,
        'token': user.get_auth_token()
    }

    return jsonify({'user': user_data})


@app.route('/api/v1/register', methods=['POST'])
@cross_origin()
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    errors = {}

    if not email:
        errors['email'] = 'Field is required.'

    if not password:
        errors['password'] = 'Field is required.'

    existing_user = User.find_by_email(email)

    if existing_user:
        errors['email'] = 'Email is already taken'

    if errors:
        return jsonify({'errors': errors}), 400

    user = User.create(email=email, password=password)

    user_data = {
        'id': user.id,
        'email': user.email,
        'token': user.get_auth_token()
    }

    return jsonify({'user': user_data}), 201


@app.route('/api/v1/artists', methods=['GET'])
@auth_token_required()
@cross_origin()
def get_artists():
    artists = []

    for artist in Artist.get_all():
        artists.append({
            'id': artist.id,
            'name': artist.name,
            'bio': artist.bio,
            'albums': [album.id for album in artist.albums.all()]
        })

    return jsonify({'artists': artists})


@app.route('/api/v1/albums', methods=['GET'])
@auth_token_required()
@cross_origin()
def get_albums():
    albums = []

    for album in Album.get_all():
        albums.append({
            'id': album.id,
            'name': album.name,
            'songs': [song.id for song in album.songs.all()]
        })

    return jsonify({'albums': albums})


@app.route('/api/v1/songs', methods=['GET'])
@auth_token_required()
@cross_origin()
def get_songs():
    songs = []

    for song in Song.get_all():
        songs.append({
            'id': song.id,
            'name': song.name,
            'album': song.album.id,
            'favorite': song.is_favorited(g.user)
        })

    return jsonify({'songs': songs})


@app.route('/api/v1/songs/<int:song_id>/favorite', methods=['PUT'])
@auth_token_required()
@cross_origin()
def favorite_song(song_id):
    song, is_favorited = Song.favorite(song_id=song_id, user=g.user)

    if not song:
        abort(404)

    song_data = {
        'id': song.id,
        'name': song.name,
        'album': song.album.id,
        'favorite': is_favorited
    }

    return jsonify({'song': song_data})
