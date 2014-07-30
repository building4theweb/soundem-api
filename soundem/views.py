from flask import g, jsonify, request

from soundem import app, db
from .decorators import auth_token_required
from .models import Artist, Album, Song, Favorite, User


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
def register():
    data = request.get_json()
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
            song=song, user=g.user).first()

        songs.append({
            'id': song.id,
            'name': song.name,
            'album': song.album.id,
            'favorite': True if favorite else False
        })

    return jsonify({'songs': songs})


@app.route('/api/v1/songs/<int:song_id>/favorite', methods=['PUT'])
@auth_token_required
def favorite_song(song_id):
    song = Song.query.filter_by(id=song_id).first_or_404()
    favorite = Favorite.query.filter_by(song=song, user=g.user).first()

    if favorite:
        is_favorite = False
        db.session.delete(favorite)
    else:
        is_favorite = True
        favorite = Favorite(song=song, user=g.user)
        db.session.add(favorite)

    db.session.commit()

    song_data = {
        'id': song.id,
        'name': song.name,
        'album': song.album.id,
        'favorite': is_favorite
    }

    return jsonify({'song': song_data})
