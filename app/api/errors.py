from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown Error')}
    if message:
        payload['message']= message
    response = jsonify(payload) # jsonify returns a Response object with default status code of 200
    response.status_code = status_code
    return response


def bad_request(message):
    error_response(400, message)

