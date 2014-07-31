import bcrypt
import jwt


def make_password(raw_password):
    return bcrypt.hashpw(
        raw_password.encode('utf-8'),
        bcrypt.gensalt()
    )


def check_password(raw_password, password):
    hashed = bcrypt.hashpw(
        raw_password.encode('utf-8'),
        password.encode('utf-8')
    )

    return hashed == password


def generate_token(payload, secret):
    return jwt.encode(payload, secret)


def decode_token(token, secret):
    try:
        return jwt.decode(token, secret)
    except (jwt.ExpiredSignature, jwt.DecodeError):
        return None
