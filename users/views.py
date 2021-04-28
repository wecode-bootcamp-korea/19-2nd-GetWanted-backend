import json
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from users.models      import User, Position
from users.validations import email_validation, phone_validation, password_validation

from my_settings import SECRET_KEY, algorithm

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            name         = data['name']
            phonenumber  = data['phonenumber']
            position     = data['position']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_EXISTS_USER'}, status=401)

            if not email_validation(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

            if not password_validation(password):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)

            if not phone_validation(phonenumber):
                return JsonResponse({'MESSAGE': 'INVALID_NUMBER'}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                    email       = email,
                    password    = hashed_password,
                    name        = name,
                    phonenumber = phonenumber,
                    position_id = Position.objects.get(name=position).id
                    )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)

class EmailCheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']

            if not email_validation(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'ACCOUNT_NOT_EXIST'}, status=401)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            user = User.objects.get(email=email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE': 'INCORRECT_PASSWORD'}, status=400)

            access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm = algorithm)

            return JsonResponse({'MESSAGE':'SUCCESS', 'TOKEN': access_token}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)
