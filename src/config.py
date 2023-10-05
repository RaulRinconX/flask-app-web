from decouple import config 

class Config:
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 8080
    HOST = '0.0.0.0' 

config = {
    'development': DevelopmentConfig
}
