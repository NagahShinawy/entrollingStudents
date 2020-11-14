from flask import session


def is_authenticated():
    is_auth = False
    if session.get('username'):
        is_auth = True
    return is_auth
