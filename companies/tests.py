import json

from django.test import TestCase,Client
from .models     import Company,Notification,Image,Tag

class NotificationTest(TestCase):

    def setUp(self):
        Company.objects.create(id=1,name='asdasds',address='dasdas',latitude=19.123123,longitude=22.231312)
        Company.objects.create(id=2,name='asdasds',address='dasdas',latitude=19.123123,longitude=22.231312)
        Company.objects.create(id=3,name='asdasds',address='dasdas',latitude=19.123123,longitude=22.231312)
        Notification.objects.create(id=1,title='하이',description='dsadas',company=Company.objects.get(id=1))
        Notification.objects.create(id=2,title='하이',description='dsadas',company=Company.objects.get(id=2))
        Notification.objects.create(id=3,title='하이',description='dsadas',company=Company.objects.get(id=3))
        Image.objects.create(id=1,image_url='sadasdasdasdas',notification=Notification.objects.get(id=1))
        Image.objects.create(id=2,image_url='sadasdasdasdas',notification=Notification.objects.get(id=2))
        Image.objects.create(id=3,image_url='sadasdasdasdas',notification=Notification.objects.get(id=3))

    def tearDown(self):
        Notification.objects.all().delete()
        Company.objects.all().delete()
        Image.objects.all().delete()
    
    def test_notification_list_get_success(self):
        client=Client()
        response = client.get('/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'notification_list':[{'title'   : '하이',
                                  'image'   : 'sadasdasdasdas',
                                  'id'      : 1,
                                  'area'    : 'dasdas',
                                  'company' : 'asdasds'},
                                 {'title'   : '하이', 
                                  'image'   : 'sadasdasdasdas', 
                                  'id'      : 2, 
                                  'area'    : 'da', 
                                  'company' : 'asdasds'}, 
                                 {'title'   : '하이', 
                                  'image'   : 'sadasdasdasdas', 
                                  'id'      : 3,
                                  'area'    : 'da',
                                  'company' : 'asdasds'}],
                                  'total'   : 3})

    def test_notification_list_get_tag_does_not_exist(self):
        client=Client()
        response = client.get('/notifications?tag=7')
        self.assertEqual(response.json(),{'MESSAGE':'TAG_DOES_NOT_EXIST'})
        self.assertEqual(response.status_code,404)

class TagTest(TestCase):

    def setUp(self):
        Tag.objects.create(id=1,name='test1')
        Tag.objects.create(id=2,name='test2')
        Tag.objects.create(id=3,name='test3')

    def tearDown(self):
        Tag.objects.all().delete()

    def test_tag_all_get_success(self):
        client=Client()
        response=client.get('/notifications/tag')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                        {'tag_list':[{'id' : 1, 'name' : 'test1'},
                                     {'id' : 2, 'name' : 'test2'},
                                     {'id' : 3, 'name' : 'test3'}]})