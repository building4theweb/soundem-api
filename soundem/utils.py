import jwt
from passlib.context import CryptContext


password_context = CryptContext(['pbkdf2_sha256'])


def make_password(raw_password):
    return password_context.encrypt(raw_password)


def check_password(raw_password, password):
    return password_context.verify(raw_password, password)


def generate_token(payload, secret):
    return jwt.encode(payload, secret)


def decode_token(token, secret):
    try:
        return jwt.decode(token, secret)
    except (jwt.ExpiredSignature, jwt.DecodeError):
        return None
