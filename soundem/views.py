from flask import g, jsonify, request, abort

from flask_cors import cross_origin

from soundem import app
from .decorators import auth_token_required
from .models import Artist, Album, Song, User


@app.route('/api/v1/login', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
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
@cross_origin(headers=['Content-Type', 'Authorization'])
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
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth_token_required
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


@app.route('/api/v1/artists/<int:artist_id>', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth_token_required
def get_artist(artist_id):
    artist = Artist.get(artist_id)

    if not artist:
        abort(404)

    artist_data = {
        'id': artist.id,
        'name': artist.name,
        'bio': artist.bio,
        'albums': [album.id for album in artist.albums.all()]
    }

    return jsonify({'artist': artist_data})


@app.route('/api/v1/albums', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth_token_required
def get_albums():
    albums = []

    for album in Album.get_all():
        albums.append({
            'id': album.id,
            'name': album.name,
            'artworkURL': album.artwork_url,
            'artist': album.artist_id,
            'songs': [song.id for song in album.songs.all()]
        })

    return jsonify({'albums': albums})


@app.route('/api/v1/albums/<int:album_id>', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth_token_required
def get_album(album_id):
    album = Album.get(album_id)

    if not album:
        abort(404)

    album_data = {
        'id': album.id,
        'name': album.name,
        'artworkURL': album.artwork_url,
        'artist': album.artist_id,
        'songs': [song.id for song in album.songs.all()]
    }

    return jsonify({'album': album_data})


@app.route('/api/v1/songs', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth_token_required
def get_songs():
    songs = []
    favorite = request.args.get('favorite')
    is_favorited = None

    if favorite == 'true':
        is_favorited = True
    elif favorite == 'false':
        is_favorited = False

    for song in Song.get_all(user=g.user, is_favorite=is_favorited):
        songs.append({
            'id': song.id,
            'name': song.name,
            'album': song.album.id,
            'favorite': song.is_favorited(g.user)
        })

    return jsonify({'songs': songs})


@app.route('/api/v1/songs/<int:song_id>', methods=['GET', 'PUT'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth_token_required
def song(song_id):
    song = Song.get(song_id)
    is_favorited = None

    if not song:
        abort(404)

    if request.method == 'PUT':
        data = request.get_json() or {}
        favorite = data.get('favorite')

        if favorite is not None:
            # Update song if favorite param was sent
            is_favorited = song.set_favorite(g.user, favorite)
    else:
        song = Song.get(song_id)

    if is_favorited is None:
        # Check if song was favorited
        is_favorited = song.is_favorited(g.user)

    song_data = {
        'id': song.id,
        'name': song.name,
        'album': song.album.id,
        'favorite': is_favorited
    }

    return jsonify({'song': song_data})


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@auth_token_required
def user(user_id):
    user = g.user

    if user.id != user_id:
        abort(403)

    user_data = {
        'id': user.id,
        'email': user.email,
        'songTotal': Song.total_count(),
        'albumTotal': Album.total_count(),
        'durationTotal': Song.total_duration()
    }

    return jsonify({'user': user_data})
