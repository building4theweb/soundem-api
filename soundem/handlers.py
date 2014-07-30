from flask import jsonify

from soundem import app


@app.errorhandler(400)
def bad_request_handler(e):
    return jsonify({
        'status_code': 400,
        'detail': 'Bad Request'
    })


@app.errorhandler(401)
def unauthorized_handler(e):
    return jsonify({
        'status_code': 401,
        'detail': 'Unauthorized'
    })


@app.errorhandler(404)
def not_found_handler(e):
    return jsonify({
        'status_code': 404,
        'detail': 'Not Found'
    })
