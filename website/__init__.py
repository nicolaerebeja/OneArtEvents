from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from datetime import date
from urllib.parse import quote_plus

db = SQLAlchemy()
DB_NAME_OLD = "database.db"

DB_NAME = 'gnmmd_afoa'
DB_USER = 'gnmmd_afoa'
DB_PASS = 'jS?%PLoJw7QW'
DB_HOST = '195.178.106.105'
DB_PORT = '3306'  # Portul implicit pentru MySQL

# Construirea șirului de conexiune pentru SQLAlchemy
db_uri = f'mysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'degrsgmitmov rfrfrfr'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME_OLD}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.context_processor
    def inject_user():
        return dict(user=current_user)


    return app