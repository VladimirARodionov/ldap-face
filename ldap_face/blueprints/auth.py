import ast
import json

import ldap3
from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from cache_config import cache
from load_env import env_config

bp = Blueprint("auth", __name__)

import logging
logging.basicConfig(filename="log_file.log", level=logging.DEBUG)
from ldap3.utils.log import set_library_log_detail_level, get_detail_level_name, set_library_log_hide_sensitive_data, EXTENDED

set_library_log_detail_level(EXTENDED)
set_library_log_hide_sensitive_data(False)


@bp.route('/api/auth/login/', methods=['OPTIONS', 'POST'])
@cross_origin()
def authenticate():
    if request.method == 'OPTIONS':
        return 200
    data = request.json
    print("1")
    server = ldap3.Server(host=env_config.get('LDAP_HOST'), port=int(env_config.get('LDAP_PORT')))
    print("2")
    conn = ldap3.Connection(server=server, user=data['username'], password=data['password'])
    print("3")
    conn.bind()
    print("4")
    if conn.bound:
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        cache.set("current_user_" + data['username'], data)
        return jsonify({'user': data['username'], 'access': access_token, 'refresh': refresh_token}), 200
    else:
        cache.delete("current_user_" + data['username'])
        return jsonify({'message': 'Error'}), 500


@bp.route('/api/auth/refresh/', methods=['OPTIONS', 'POST'])
@cross_origin()
@jwt_required()
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'user': current_user, 'access': access_token}), 200


@bp.route('/api/auth/logout/', methods=['OPTIONS', 'POST'])
@cross_origin()
@jwt_required()
def user_logout():
    current_user = get_jwt_identity()
    cache.delete("current_user_" + current_user)
    return jsonify({'message': "success"}), 204

