class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '12345678'
    MYSQL_DB = 'beca2'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:12345678@localhost/beca2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    



config = {
    'development': DevelopmentConfig
}