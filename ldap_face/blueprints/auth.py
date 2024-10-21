import ldap3
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from load_env import env_config

bp = Blueprint("auth", __name__)


@bp.route('/api/auth/login/', methods=['OPTIONS', 'GET', 'POST'])
@cross_origin()
def authenticate():
    if request.method == 'OPTIONS':
        return 200
    data = request.form
    server = ldap3.Server(host=env_config.get('LDAP_HOST'), port=int(env_config.get('LDAP_PORT')))
    conn = ldap3.Connection(server=server, user=data.get('username'), password=data.get('password'))
    conn.bind()
    if conn.bound:
        search_base = 'dc=example,dc=com'
        search_filter = '(objectClass=inetOrgPerson)'
        # search_filter = '(&(mail=john.doe@somecompany.com))'
        attrs = ["*"]
        print(conn.search(search_base=search_base, search_filter=search_filter, attributes=attrs))
        return jsonify({'message': 'Success'}), 200
    else:
        return jsonify({'message': 'Error'}), 500
