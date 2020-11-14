import os


class Config:
    # os.environ dictionary contains info about system and users, hardware, ...
    # get"SECRET_KEY" if exists else return"os.urandom(16)"
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x19\x0f\x1f&\xb9\xa8\x1aYy\xd3\xad\xd32T\xca\xa0'
    MONGODB_SETTINGS = {
        'db': 'UTA_Enrollment',
    }
