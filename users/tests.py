import json
import bcrypt

from django.test import TestCase
from django.test import Client

from users.models import User, Position


class SignUoTest(TestCase):

    def setUp(self):
        Position.objects.create(id=1, name='백엔드')
        Position.objects.create(id=2, name='프론트엔드')
        Position.objects.create(id=3, name='풀스택')
        User(email='fishingman@naver.com', position_id=1).save()

    def tearDown(self):
        User.objects.all().delete()
        Position.objects.all().delete()

    def test_signup_post_success(self):
        client = Client()
        user = {
                'name' : '정재유',
                'email' : 'fishingman99@naver.com',
                'password' : '1q2w3e4r',
                'phonenumber' : '010-4444-5555',
                'position' : '백엔드'
                }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_signup_post_fail_same_email(self):
        client = Client()
        user = {
                'name' : '정재유',
                'email' : 'fishingman@naver.com',
                'password' : '1q2w3e4r',
                'phonenumber' : '010-4444-5555',
                'position' : '백엔드'
                }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'ALREADY_EXISTS_USER'
                }
            )

    def test_signup_post_fail_email_validation(self):
        client = Client()
        user = {
                'name' : '정재유',
                'email' : 'fishingmannaver.com',
                'password' : '1q2w3e4r',
                'phonenumber' : '010-4444-5555',
                'position' : '백엔드'
                }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'INVALID_EMAIL'
                }
            )

    def test_signup_post_fail_password_validation(self):
        client = Client()
        user = {
                'name' : '정재유',
                'email' : 'fishingman99@naver.com',
                'password' : '1q',
                'phonenumber' : '010-4444-5555',
                'position' : '백엔드'
                }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'INVALID_PASSWORD'
                }
            )

    def test_signup_post_fail_phonenumber_validation(self):
        client = Client()
        user = {
                'name' : '정재유',
                'email' : 'fishingman99@naver.com',
                'password' : '1q2w3e4r',
                'phonenumber' : '01044445555',
                'position' : '백엔드'
                }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'INVALID_NUMBER'
                }
            )

    def test_signup_post_fail_keyerror(self):
        client = Client()
        user = {
                'name' : '정재유',
                'account' : 'fishingmannaver.com',
                'password' : '1q2w3e4r',
                'phonenumber' : '010-4444-5555',
                'position' : '백엔드'
                }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'KEY_ERROR'
                }
            )

class EmailCheckTest(TestCase):

    def setUp(self):
        Position.objects.create(id=1, name='백엔드')
        User.objects.create(name='정재유', email='fishingman99@naver.com', password='1q2w3e4r', phonenumber='010-4444-3333', position_id=1)

    def tearDown(self):
        User.objects.all().delete()
        Position.objects.all().delete()

    def test_email_check_success(self):
        client = Client()
        email = {'email' : 'fishingman99@naver.com'}
        

        response = client.post('/users/email', json.dumps(email), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_email_check_fail_invalid_email(self):
        client = Client()
        email = { 'email' :'fishingman99naver.com'}

        response = client.post('/users/email', json.dumps(email), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'INVALID_EMAIL'
                }
            )

    def test_email_check_fail_not_exist_account(self):
        client = Client()
        email = { 'email' :'fishingman@naver.com'}

        response = client.post('/users/email', json.dumps(email), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'ACCOUNT_NOT_EXIST'
                }
            )

    def test_email_check_fail_keyerror(self):
        client = Client()
        email = { 'account' :'fishingman99@naver.com'}

        response = client.post('/users/email', json.dumps(email), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'KEY_ERROR'
                }
            )

class SignInCheckTest(TestCase):

    def setUp(self):
        client = Client()
        Position.objects.create(id=1, name='백엔드')
        user = {
                'name' : '정재유',
                'email' : 'fishingman99@naver.com',
                'password' : '1q2w3e4r',
                'phonenumber' : '010-4444-5555',
                'position' : '백엔드'
                }

        client.post('/users/signup', json.dumps(user), content_type='application/json')

    def tearDown(self):
        User.objects.all().delete()
        Position.objects.all().delete()

    def test_signin_check_success(self):
        client = Client()
        user = {
                'email' : 'fishingman99@naver.com',
                'password' : '1q2w3e4r'
                }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_signin_check_fail_incorrect_password(self):
        client = Client()
        user = {
                'email' : 'fishingman99@naver.com',
                'password' : '1q2w3e'
                }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'INCORRECT_PASSWORD'
                }
            )

    def test_signin_check_fail_keyerror(self):
        client = Client()
        user = {
                'account' : 'fishingman99@naver.com',
                'password' : '1q2w3e4r'
                }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    'MESSAGE': 'KEY_ERROR'
                }
            )
