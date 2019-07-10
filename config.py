import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO Fix SQLALCHEMY_BINDS Usage
    #
    # The following line will create a "TypeError: string indices must be
    # integers" Error that will break the site. Binds are used for multiple
    # databases to be referenced using SQLALCHEMY. This may be fixed in later
    # builds.
    #
    #  SQLALCHEMY_BINDS = os.getenv("SQLALCHEMY_BINDS")

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMINS = os.getenv("ADMINS")
