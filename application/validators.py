from wtforms.validators import StopValidation


def valid_password(*agr):
    password = agr[-1].data

    if len(password) < 8:
        raise StopValidation('Weak Password')
    return password


def valid_email(*agr):
    email = agr[-1].data.lower()
    print(email)
    if not email.endswith('@gmail.com'):
        raise StopValidation('Must Be Gmail(my custom)')
    return email

