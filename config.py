import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hardcto guess string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = '17791652478@163.com'
    MAIL_PASSWORD = 'Lzn19971012'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Suarezlin]'
    FLASKY_MAIL_SENDER = 'Suarezlin <17791652478@163.com>'
    WHOOSH_BASE = os.path.join(basedir, 'search.db')

    @staticmethod
    def init_app(app):
        pass


config = {'default': Config}
