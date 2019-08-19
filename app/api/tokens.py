from flask import jsonify, g
from app import db
from .auth import basic_auth
from . import api_bp


@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@api_bp.route('/tokens', methods=['DELETE'])
@basic_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
