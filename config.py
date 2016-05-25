import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'nirajosh@in.ibm.com'
    MAIL_PASSWORD = 'summerc00l'
    SVS_MAIL_SUBJECT_PREFIX = '[SVSApp]'
    SVS_MAIL_SENDER = 'SVS_Admin<Svsadmin@svs.com>'
    SVS_ADMIN = 'nirav.joshi05@hotmail.com'
    SVS_PAGE_PHOTO = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\nirav\\Desktop\\SVSFromHaven\\SVSdata-dev.db'
    #SQLALCHEMY_DATABASE_URI = 'postgres://svsappdb:svsapp@localhost/svsappdb'
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'SVSdata-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'SVSdata.sqlite')

    @classmethod
    def init_app(cls,app):
        Config.init_app(app)

        #Email errors to admin
        import  logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.SVS_MAIL_SENDER,
            toaddrs=[cls.SVS_ADMIN],
            subject=cls.SVS_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
