from flask import jsonify

from soundem import app


def json_error_handler(e):
    return jsonify({
        'status_code': e.code,
        'error': 'Bad Request',
        'detail': e.description
    }), e.code


@app.errorhandler(400)
def bad_request_handler(e):
    return json_error_handler(e)


@app.errorhandler(401)
def unauthorized_handler(e):
    return json_error_handler(e)


@app.errorhandler(404)
def not_found_handler(e):
    return json_error_handler(e)


@app.errorhandler(405)
def method_not_allowed_handler(e):
    return json_error_handler(e)
