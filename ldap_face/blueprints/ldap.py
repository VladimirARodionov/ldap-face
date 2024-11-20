import ldap3
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

from cache_config import cache
from load_env import env_config

bp = Blueprint("ldap", __name__)

@bp.route('/api/ldap/', methods=['OPTIONS', 'GET'])
@cross_origin()
@jwt_required()
def ldap():
    if request.method == 'OPTIONS':
        return 200
    current_user = get_jwt_identity()
    data = cache.get("current_user_" + current_user)
    print(data)
    if data:
        server = ldap3.Server(host=env_config.get('LDAP_HOST'), port=int(env_config.get('LDAP_PORT')))
        conn = ldap3.Connection(server=server, user=data['username'], password=data['password'])
        conn.bind()
        if conn.bound:
            search_base = 'ou=people,dc=new-world,dc=group'
            search_filter = '(objectClass=inetOrgPerson)'
            # search_filter = '(&(mail=john.doe@somecompany.com))'
            attrs = ["*"]
            result = conn.search(search_base=search_base, search_filter=search_filter, search_scope=ldap3.SUBTREE, attributes=attrs)
            print(conn.response)
            tree = []
            base = {'key': search_base, 'label': search_base, 'data': search_base, 'children': []}
            for resp in conn.response:
                data = resp['attributes']
                data.pop('userPassword')
                child = {'key': resp['dn'], 'label': resp['dn'], 'data': dict(data), 'children': []}
                base['children'].append(child)
            tree.append(base)
            print()
            print(tree)
            return jsonify({'data': tree}), 200
        else:
            return jsonify({'message': 'Error'}), 500
    else:
        return jsonify({'message': 'Error'}), 500
