import json, jwt

from django.test import TestCase, Client

from users.models import User, Position
from .models import Resume,Career
from my_settings import SECRET_KEY,algorithm

# Create your tests here.

class ResumeTest(TestCase):

    def setUp(self):
        Position.objects.create(name='frontend')
        Position.objects.create(name='backend')
        user = User.objects.create(
            id       = 1,
            email    = 'qwer@asdf.com',
            password = 'asdfqwer',
            position = Position.objects.get(name='backend')
        )
        Resume.objects.create(
            title        = 'title',
            name         = 'name',
            email        = 'email',
            phone_number = '000000000',
            introduction = 'introduction',
            status       = True,
            user         = User.objects.get(id=1)
        )
        self.access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm=algorithm)

    def tearDown(self):
        User.objects.all().delete()
        Position.objects.all().delete()
        Career.objects.all().delete()
        Resume.objects.all().delete()

    def test_resume_create_success(self):
        client = Client()
        header  = {'HTTP_Authorization': self.access_token}
        request = {
            'title'    : '제목',
            'fullName' : '이름',
            'email'    : 'asdf@asdf.com',
            'phone'    : '전화번호',
            'intro'    : '간단 소개글',
            'isFinal'  : True,
            'workInfo' : [
                {
                    "isWorking"   : False,
                    "companyName" : "회사 이름",
                    "startMonth"  : "12",
                    "startYear"   : "2014",
                    "endMonth"    : "01",
                    "endYear"     : "2017",
                    "position"    : "fkfkf",
                    "details"     : "sdlflf"
                },
                {
                    "isWorking"   : True,
                    "companyName" : "2222",
                    "startMonth"  : "2014",
                    "startYear"   : "12",
                    "position"    : "fffffff",
                    "details"     : "dddddd"
                },
                {
                    "isWorking"   : False,
                    "companyName" : "3333",
                    "startMonth"  : "12",
                    "startYear"   : "2014",
                    "endMonth"    : "01",
                    "endYear"     : "2017",
                    "position"    : "ffasdfff",
                    "details"     : "ddsafdd"
                }
            ]
        }
        response = client.post('/resumes', json.dumps(request), **header, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{'MESSAGE':'SUCCESS'})

    def test_resume_create_success_empty_work_info(self):
        client = Client()
        header = {'HTTP_Authorization': self.access_token}
        request = {
            'title': '제목',
            'fullName': '이름',
            'email': 'asdf@asdf.com',
            'phone': '전화번호',
            'intro': '간단 소개글',
            'isFinal': True
        }
        response = client.post('/resumes', json.dumps(request), **header, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'SUCCESS'})

    def test_resume_create_success_(self):
        client = Client()
        header = {'HTTP_Authorization': self.access_token}
        request = {
            'title': '제목',
            'fullName': '이름',
            'email': 'asdf@asdf.com',
            'phone': '전화번호',
            'isFinal': True,
            'workInfo': [
                {
                    "isWorking": True,
                    "companyName": "회사 이름",
                    "startMonth": "12",
                    "startYear": "2014",
                    "position": "fkfkf",
                    "details": "sdlflf"
                }
            ]
        }
        response = client.post('/resumes', json.dumps(request), **header, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'SUCCESS'})

    def test_key_error(self):
        client = Client()
        headers = {'HTTP_Authorization': self.access_token}
        request = {
            'fullName' : 'name',
            'email'    : 'email',
            'phone'    : '000000000000',
            'intro'    : 'test'
        }
        response = client.post('/resumes', json.dumps(request), **headers, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'MESSAGE':'KEY_ERROR'})