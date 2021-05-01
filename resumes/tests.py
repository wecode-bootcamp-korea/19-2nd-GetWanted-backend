import json, jwt

from django.test  import TestCase, Client

from users.models import User, Position
from .models      import Resume,Career
from my_settings  import SECRET_KEY,algorithm

# Create your tests here.

class ResumeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Position.objects.create(name='frontend')
        Position.objects.create(name='backend')
        cls.user = User.objects.create(
            id       = 1,
            email    = 'qwer@asdf.com',
            password = 'asdfqwer',
            position = Position.objects.get(name='backend')
        )
        Resume.objects.create(
            id           = 1,
            title        = 'title',
            name         = 'name',
            email        = 'email',
            phone_number = '000000000',
            introduction = 'introduction',
            status       = True,
            user         = User.objects.get(id=1)
        )
        Resume.objects.create(
            id           = 2,
            title        = '제목',
            name         = '이름',
            email        = '이메일',
            phone_number = '1111111111',
            introduction = '자기소개',
            status       = 1,
            user         = User.objects.get(id=1)
        )
        Career.objects.create(
            id            = 1,
            is_working    = 0,
            start_working = '2020-01',
            end_working   = '2020-12',
            company_name  = 'company_name',
            department    = 'department',
            description   = 'description',
            resume        = Resume.objects.get(id=1)
        )
        cls.access_token = jwt.encode({'user_id': cls.user.id}, SECRET_KEY, algorithm=algorithm)

    def test_resume_create_success(self):
        client  = Client()
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
            'title'    : '제목',
            'fullName' : '이름',
            'email'    : 'asdf@asdf.com',
            'phone'    : '전화번호',
            'intro'    : '간단 소개글',
            'isFinal'  : True
        }
        response = client.post('/resumes', json.dumps(request), **header, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'SUCCESS'})

    def test_resume_create_success_(self):
        client  = Client()
        header  = {'HTTP_Authorization': self.access_token}
        request = {
            'title'    : '제목',
            'fullName' : '이름',
            'email'    : 'asdf@asdf.com',
            'phone'    : '전화번호',
            'isFinal'  : True,
            'workInfo' : [
                {
                    "isWorking"   : True,
                    "companyName" : "회사 이름",
                    "startMonth"  : "12",
                    "startYear"   : "2014",
                    "position"    : "fkfkf",
                    "details"     : "sdlflf"
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

    def test_resume_get_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.access_token}

        response = client.get('/resumes',**headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'MESSAGE':'SUCCESS',
                          'RESULTS':{
                              'email'    : 'qwer@asdf.com',
                              'fullName' : '',
                              'phone'    : '',
                              'title'    : '_3'}
                          })

    def test_existing_resume_get_all_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.access_token}

        response = client.get('/resumes/1',**headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'MESSAGE':'SUCCESS',
            'RESULTS':
                {
                    'email'    : 'email',
                    'fullName' : 'name',
                    'id'       : 1,
                    'intro'    : 'introduction',
                    'phone'    : '000000000',
                    'title'    : 'title',
                    'workInfo' : [{
                        'id'          : 1,
                        "isWorking"   : 0,
                        "startYear"   : "2020",
                        "startMonth"  : "01",
                        "endYear"     : "2020",
                        "endMonth"    : "12",
                        "companyName" : "company_name",
                        "position"    : "department",
                        "details"     : "description"
                    }
                    ]}})

    def test_existing_resume_get_empty_workinfo_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.access_token}

        response = client.get('/resumes/2', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'MESSAGE':'SUCCESS',
            'RESULTS':
                {
                    'email'    : '이메일',
                    'fullName' : '이름',
                    'id'       : 2,
                    'intro'    : '자기소개',
                    'phone'    : '1111111111',
                    'title'    : '제목',
                    'workInfo' : [
                    ]}})

    def test_invalid_resume_error(self):
        client = Client()
        headers = {'HTTP_Authorization': self.access_token}

        response = client.get('/resumes/11',**headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'MESSAGE':'NOT_FOUND_RESUME'})

    def test_invalid_values_resume_get_error(self):
        client = Client()
        headers = {'HTTP_Authorization': self.access_token}

        response = client.get('/resumes/"ㅇㅇㅇ"',**headers)

        self.assertEqual(response.status_code, 404)

    def test_resume_list_get_success(self):
        client = Client()
        headers = {'HTTP_Authorization': self.access_token}

        response = client.get('/resumes/lists', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'MESSAGE' :'SUCCESS',
            'RESULTS' : {
                'fileresume_list' : [],
                'resume_list'     : [
                    {
                        'date'   : '2021-05-04',
                        'id'     : 1,
                        'name'   : 'title',
                        'status' : True
                    },
                    {
                        'date'   : '2021-05-04',
                        'id'     : 2,
                        'name'   : '제목',
                        'status' : True
                    }]}})