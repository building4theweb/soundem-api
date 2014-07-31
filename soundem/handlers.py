from flask import jsonify

from soundem import app


@app.errorhandler(400)
def bad_request_handler(e):
    return jsonify({
        'status_code': e.code,
        'error': 'Bad Request',
        'detail': e.description
    }), e.code


@app.errorhandler(401)
def unauthorized_handler(e):
    return jsonify({
        'status_code': e.code,
        'error': 'Unauthorized',
        'detail': e.description
    }), e.code


@app.errorhandler(404)
def not_found_handler(e):
    return jsonify({
        'status_code': e.code,
        'error': 'Not Found',
        'detail': e.description
    }), e.code
