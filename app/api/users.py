from flask import jsonify, request, url_for, g, abort
from .auth import token_auth

from app import db
from . import api_bp
from .errors import bad_request
from app.models import User

# what about using current_user == user to judge if the user is authenticated??


@api_bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collect_dictionary(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@api_bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api_bp.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collect_dictionary(user.followers, page, per_page, 'api.get_followers', id=id)
    return jsonify(data)


@api_bp.route('/users/<int:id>/followed', methods=["GET"])
@token_auth.login_required
def get_followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collect_dictionary(user.followed, page, per_page, 'api.get_followed', id=id)
    return jsonify(data)


@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.from_json() or {}
    if 'username' not in data or 'password' not in data or 'email' not in data:
        return bad_request("username password and email required")
    if User.query.filter_by(username=data['username']).first():
        return bad_request("Username is taken!")
    if User.query.filter_by(email=data['email']).first():
        return bad_request("Email has been registered with")
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@api_bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if g.current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.from_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request("Please use a different username")
    if 'email' in data and data['email'] != user.email and \
        User.query.filter_by(email=data['email']).first():
        return bad_request("Please use a different email")
    user.from_dict(data)
    db.session.commit()
    response = jsonify(user.to_dict())
    return response

