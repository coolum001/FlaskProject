import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secret_key'
    UPLOAD_FOLDER = 'c:\\temp\\xxx'


# end Config

