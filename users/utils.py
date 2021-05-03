import jwt

from django.http       import JsonResponse
from users.models      import User
from users.validations import email_validation

from my_settings       import algorithm,SECRET_KEY

def login_required(func):
    def decorator(self, request, *args, **kwargs):
        try:
            access_token = request.headers['Authorization']
            user         = jwt.decode(access_token, SECRET_KEY, algorithms = algorithm)
            request.user = User.objects.get(id=user['user_id'])

            return func(self, request, *args, **kwargs)

        except KeyError:
            return JsonResponse({"MESSAGE": "INVALID_LOGIN"}, status=401)

        except jwt.DecodeError:
            return JsonResponse({"MESSAGE": "INVALID_TOKEN"}, status=401)
    
    return decorator

def social_signin(name,email):
    if not email_validation(email):
        return 'INVALID_EMAIL'

    if not User.objects.filter(email=email).exists():
        User(name=name, email=email, position_id=1, is_social=1).save()

    user = User.objects.get(email=email)

    access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm = algorithm)

    return access_token
