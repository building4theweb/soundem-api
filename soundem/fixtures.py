import json

from soundem import db, BASE_PATH
from .models import Artist, Album, Song


def sample():
    fixture_path = '{}/fixtures/sample.json'.format(BASE_PATH)

    with open(fixture_path) as fixture_file:
        fixtures = json.load(fixture_file)

    for artist in fixtures:
        print 'Creating artist: {}'.format(artist['name'])
        _artist = Artist(
            name=artist['name'],
            bio=artist['bio']
        )

        db.session.add(_artist)

        for album in artist['albums']:
            print ' Creating album: {}'.format(album['name'])
            _album = Album(
                name=album['name'],
                artwork_url=album['artwork_url'],
                artist=_artist
            )

            db.session.add(_album)

            for song in album['songs']:
                print '     Creating song: {}'.format(song['name'])
                _song = Song(name=song['name'], album=_album, url=song['url'])

                db.session.add(_song)

        db.session.commit()
