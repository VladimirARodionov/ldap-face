from flask import Flask
from flask_jwt_extended import JWTManager

from flask_cors import CORS

from cache_config import cache
from load_env import env_config


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})
    # cors = CORS(app, origins=[origin for origin in env_config.get('CORS_ALLOWED_ORIGINS').split(',')]) # resources={r"/api/*": {"origins": "*"}}
    # app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_mapping(
        SECRET_KEY=env_config.get('SECRET_KEY'),
        JWT_SECRET_KEY=env_config.get('JWT_SECRET_KEY'),
    )
    # apply the blueprints to the app
    from ldap_face.blueprints import auth_bp, ldap_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(ldap_bp)

    jwt = JWTManager(app)
    # app.add_url_rule("/", endpoint="employees.employees")
    # print(app.url_map)
    # app.debug = True
    return app, jwt


app, jwt = create_app()
