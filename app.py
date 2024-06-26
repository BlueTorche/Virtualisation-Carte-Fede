import os
import sys
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv
from flask_wtf import CSRFProtect

from Models.utils.flask_qrcode import QRcode

from Models.database.databasemodels import db as db
from Models.routes.change_credentials_route import ChangeCredentials
# from Models.routes.Register_route import Register
from Models.routes.login_route import Login
from Models.routes.home_route import Home
# from Models.routes.Logout_route import Logout
from Models.routes.admin_route import Admin
from Models.routes.logout_route import Logout
from Models.routes.scan_route import Scan
from Models.routes.view_route import View
from Models.routes.gestion_route import Gestion

from Models.flutter_api.flutter_login_route import FlutterLogin
from Models.flutter_api.flutter_admin_route import FlutterAdmin
from Models.flutter_api.flutter_gestion_route import FlutterGestion
from Models.flutter_api.flutter_view_route import FlutterView
from Models.flutter_api.flutter_change_password import FlutterChangePassword
from Models.flutter_api.flutter_qr_route import FlutterQRCode

from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended.exceptions import NoAuthorizationError


# from Models.routes.ChangeCredentials_route import ChangeCredentials
# from Models.utils.limiter import limiter

def handle_no_authorization_error(e):
    # Handle the NoAuthorizationError here
    # You can log the error or perform any other actions if needed
    # Redirect the user to a specific page
    return redirect(url_for('login'))

def load_env():
    if os.path.exists('.env'):
        print('Importing environment from .env...')
        load_dotenv()

        dbusername = os.getenv('POSTGRES_ENV_USER')
        dbpassword = os.getenv('POSTGRES_ENV_PASSWORD')
        dbname = os.getenv('POSTGRES_ENV_DATABASE')
        dbhost = "localhost"  # cause it would mean we are outside the docker container and we need to connect to the docker container
        dbport = os.getenv('POSTGRES_ENV_PORT')
        flask_secret_key = os.getenv('FLASK_SECRET_KEY')
        jwt_secret_key = os.getenv('JWT_SECRET_KEY')

    else:
        dbusername = os.getenv('POSTGRES_ENV_USER') if os.getenv('POSTGRES_ENV_USER') else ""
        dbpassword = os.getenv('POSTGRES_ENV_PASSWORD') if os.getenv('POSTGRES_ENV_PASSWORD') else ""
        dbname = os.getenv('POSTGRES_ENV_DATABASE') if os.getenv('POSTGRES_ENV_DATABASE') else ""
        dbhost = os.getenv('POSTGRES_ENV_HOSTNAME') if os.getenv('POSTGRES_ENV_HOSTNAME') else "postgredb"
        dbport = os.getenv('POSTGRES_ENV_PORT') if os.getenv('POSTGRES_ENV_PORT') else "5432"
        flask_secret_key = os.getenv('FLASK_SECRET_KEY') if os.getenv('FLASK_SECRET_KEY') else ""
        jwt_secret_key = os.getenv('JWT_SECRET_KEY') if os.getenv('JWT_SECRET_KEY') else ""

    return dbusername, dbpassword, dbname, dbhost, dbport, flask_secret_key, jwt_secret_key


def create_app():
    dbusername, dbpassword, dbname, dbhost, dbport, flask_secret_key, jwt_secret_key = load_env()

    app = Flask(__name__, static_url_path='/static')
    api = Api(app)

    QRcode(app)

    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'postgresql://' + dbusername + ':' + dbpassword + '@' + dbhost + ':' + dbport + '/' + dbname,
        'MAX_CONTENT_LENGTH': 32 * 1024 * 1024,
        'PERMANENT_SESSION_LIFETIME': timedelta(days=30),
        'JWT_TOKEN_LOCATION': ["headers", "cookies"],
        'JWT_ACCESS_COOKIE_PATH': '/',
        'JWT_COOKIE_CSRF_PROTECT': False,
        'JWT_HEADER_NAME': "X-Access-Token",
        'JWT_HEADER_TYPE': "CustomScheme",
        'JWT_QUERY_STRING_NAME': "token",
        'JWT_SECRET_KEY': jwt_secret_key,
        'JWT_ACCESS_TOKEN_EXPIRES': timedelta(days=30),
        'JWT_REFRESH_TOKEN_EXPIRES': timedelta(days=30),
        'JWT_BLACKLIST_ENABLED': True,
        'JWT_BLACKLIST_TOKEN_CHECKS': ['access', 'refresh'],
        'JWT_ERROR_MESSAGE_KEY': 'message',
    })

    jwt = JWTManager(app)

    app.register_error_handler(NoAuthorizationError, handle_no_authorization_error)
    app.register_error_handler(ExpiredSignatureError, handle_no_authorization_error)

    app.secret_key = flask_secret_key
    # CSRFProtect(app)
    # limiter.init_app(app)

    # ajoute les ressources à l'api et les joint à la route
    # api.add_resource(Register, '/register')
    api.add_resource(Login, '/')
    api.add_resource(Home, '/home')
    api.add_resource(Admin, '/admin')
    api.add_resource(View, '/view')
    api.add_resource(Scan, '/scan')
    api.add_resource(Logout, '/logout')
    api.add_resource(Gestion, '/gestion')
    api.add_resource(ChangeCredentials, '/change-credentials')

    api.add_resource(FlutterLogin, '/api/login')
    api.add_resource(FlutterAdmin, '/api/admin')
    api.add_resource(FlutterGestion, '/api/gestion')
    api.add_resource(FlutterView, '/api/view')
    api.add_resource(FlutterChangePassword, '/api/change_password')
    api.add_resource(FlutterQRCode, '/api/qrcode')

    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)




if __name__ == '__main__':
    ARGDEBUG = len(sys.argv) > 1 and sys.argv[1] in ('-d', '--debug')
    app = create_app()
    app.run(debug=ARGDEBUG, host='0.0.0.0')



