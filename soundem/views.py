from flask import jsonify, request
from flask.ext.security import utils, current_user

from soundem import app, db
from .decorators import auth_token_required
from .models import Artist, Album, Song, Favorite, user_datastore


@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    errors = {}

    if not email:
        errors['email'] = 'Field is required.'

    if not password:
        errors['password'] = 'Field is required.'

    user = user_datastore.get_user(email)

    if not user:
        errors['email'] = 'User does not exist.'

    if not utils.verify_and_update_password(password, user):
        errors['password'] = 'Invalid password.'

    if not user.is_active():
        errors['email'] = 'User is not active.'

    if errors:
        return jsonify({'errors': errors}), 400

    utils.login_user(user)

    user_data = {
        'id': user.id,
        'email': user.email,
        'active': user.is_active(),
        'token': user.get_auth_token()
    }

    return jsonify({'user': user_data})

@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    errors = {}

    if not email:
        errors['email'] = 'Field is required.'

    if not password:
        errors['password'] = 'Field is required.'

    existing_user = user_datastore.get_user(email=email)

    if existing_user:
        errors['email'] = 'Email is already taken'

    if errors:
        return jsonify({'errors': errors}), 400

    user = user_datastore.create_user(email=email, password=password)
    db.session.commit()

    user_data = {
        'id': user.id,
        'email': user.email,
        'active': user.is_active(),
        'token': user.get_auth_token()
    }

    return jsonify({'user': user_data}), 201


@app.route('/api/v1/artists', methods=['GET'])
@auth_token_required
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
@auth_token_required
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
@auth_token_required
def get_songs():
    songs = []

    for song in Song.query.all():
        favorite = Favorite.query.filter_by(
            song=song, user=current_user).first()

        songs.append({
            'id': song.id,
            'name': song.name,
            'album': song.album.id,
            'favorite': True if favorite else False
        })

    return jsonify({'songs': songs})
