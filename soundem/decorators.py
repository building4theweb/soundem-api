from functools import wraps

from flask import g, request, abort

from .models import User


def verify_auth_token():
    auth = request.headers.get('Authorization', None)

    if auth is None:
        abort(401, description='Authorization Required')

    parts = auth.split()

    if parts[0].lower() != 'jwt':
        raise abort(401, description='Unsupported authorization type')
    elif len(parts) == 1:
        raise abort(401, description='Token missing')
    elif len(parts) > 2:
        raise abort(401, description='Token contains spaces')

    user = User.find_by_token(parts[1])

    if not user:
        raise abort(401)

    g.user = user


def auth_token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_auth_token()
        return fn(*args, **kwargs)
    return decorated
