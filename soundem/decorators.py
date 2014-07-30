from functools import wraps

from flask import abort
from flask.ext.security.decorators import _check_token


def auth_token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if _check_token():
            return fn(*args, **kwargs)
        return abort(401)
    return decorated
