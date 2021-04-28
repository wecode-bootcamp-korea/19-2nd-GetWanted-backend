import re

def email_validation(email):
    formula = re.compile('^[a-z0-9_-]+@[a-z0-9]+\.[a-z0-9.]+$')

    if formula.match(email):
        return True

    return False

def phone_validation(phone):
    formula = re.compile('^[0-9]{3}-[0-9]{3,4}-[0-9]{4}$')

    if formula.match(phone):
        return True

    return False

def password_validation(password):
    formula = re.compile('^[a-z\d]{6,}$')

    if formula.match(password):
        return True

    return False
