from decouple import config 

class Config:
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 8080
    HOST = '0.0.0.0' 

class RabbitMQConfig(Config):
    EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.office365.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'aykutrincon@gmail.com'
    EMAIL_HOST_PASSWORD = 'scfuiloumslnoaah'

config = {
    'development': DevelopmentConfig
}
