"""
This file initializes the inventory app. The database, login manager, and
bootstrap framework are all initialized here. This file also sends errors via
email to the administrator.
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_bootstrap import Bootstrap

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# mail = Mail(app)
# login = LoginManager(app)
# bootstrap = Bootstrap(app)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.manage import bp as manage_bp
    app.register_blueprint(manage_bp, url_prefix='/manage')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug:
        # Send errors to email
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            # Used for external emails
            # secure = None
            # if app.config['MAIL_USE_TLS']:
            #     secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='AMMK Inventory System Failure',
                credentials=auth)
                # If TLS was in use, append this to SMTPHandler
                # , secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    # Write errors to log file
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/inventory.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    if os.environ['FLASK_ENV'] != 'development':
        app.logger.setLevel(logging.INFO)
        app.logger.info('AMMK Inventory System startup')

    return app

from app import models
