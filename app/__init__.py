from flask import Flask, render_template, session, redirect, url_for, flash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    return app
