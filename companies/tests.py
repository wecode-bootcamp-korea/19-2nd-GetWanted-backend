import json

from django.test import TestCase,Client
from .models     import Notification,NotificationTag,Image,Tag,Company

class NotificationlistTest(TestCase):
    def setUp(self):
        Company.objects.create(id=1,name='test1',address='서울 동대문구 한천로 63길 10',latitude=19.121212, longitude=20.12121)
        Notification.objects.create(id=1,title='adasd',company=Company.objects.get(id=1),description='dasdas')
        Image.objects.create(id=1,image_url='asdasdasdasdasdasdsa.jpg',notification=Notification.objects.get(id=1))
        Image.objects.create(id=2,image_url='asdasdasdasdasdasdsa.jpg',notification=Notification.objects.get(id=1))
        Tag.objects.create(id=1,name='하이하이')
        Tag.objects.create(id=2,name='하이하이2')
        NotificationTag.objects.create(id=1,notification=Notification.objects.get(id=1),tag=Tag.objects.get(id=1))
        NotificationTag.objects.create(id=2,notification=Notification.objects.get(id=1),tag=Tag.objects.get(id=2))

    def tearDown(self):
        Company.objects.all().delete()
        Notification.objects.all().delete()
        Image.objects.all().delete()
    
    def test_notification_list_get_success(self):
        client=Client()
        response = client.get('/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'notification_list': 
        [{'title' : 'adasd', 
        'image'   : 'asdasdasdasdasdasdsa.jpg', 
        'id'      : 1,
         'area'   : '서울', 
         'company': 'test1'}], 
         'total'  : 1})

    def test_notification_list_get_tag_does_not_exist(self):
        client=Client()
        response = client.get('/notifications?tag=7')
        self.assertEqual(response.json(),{'MESSAGE':'TAG_DOES_NOT_EXIST'})
        self.assertEqual(response.status_code,404)
    
    def test_notification_list_get_search_success(self):
        client=Client()
        response = client.get('/notifications?search=test1')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{'notification_list': 
        [{'title' : 'adasd', 
        'image'   : 'asdasdasdasdasdasdsa.jpg', 
        'id'      : 1,
         'area'   : '서울', 
         'company': 'test1'}], 
         'total'  : 1})

    def test_notification_list_get_value_error(self):
        client=Client()
        response = client.get('/notifications?tag=asdasdas')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),{'MESSAGE': 'VALUE_ERROR'})

class TagTest(TestCase):

    def setUp(self):
        Tag.objects.create(id=1,name='test1')
        Tag.objects.create(id=2,name='test2')
        Tag.objects.create(id=3,name='test3')

    def tearDown(self):
        Tag.objects.all().delete()

class NotificationDetailTest(TestCase):
    def setUp(self):
        Company.objects.create(id=1,name='test1',address='서울 동대>문구 한천로 63길 10',latitude=19.121212, longitude=20.12121)
        Notification.objects.create(id=1,title='adasd',company=Company.objects.get(id=1),description='dasdas')
        Image.objects.create(id=1,image_url='asdasdasdasdasdasdsa.jpg',notification=Notification.objects.get(id=1))
        Image.objects.create(id=2,image_url='asdasdasdasdasdasdsa.jpg',notification=Notification.objects.get(id=1))
        Tag.objects.create(id=1,name='하이하이')
        Tag.objects.create(id=2,name='하이하이2')
        NotificationTag.objects.create(id=1,notification=Notification.objects.get(id=1),tag=Tag.objects.get(id=1))
        NotificationTag.objects.create(id=2,notification=Notification.objects.get(id=1),tag=Tag.objects.get(id=2))

    def tearDown(self):
        Company.objects.all().delete()
        Notification.objects.all().delete()

    def test_notification_detail_get_success(self):
        client=Client()
        response = client.get('/notifications/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'NOTIFICATION_DETAIL': 
        [{'notification_id' : 1, 
          'title'           : 'adasd', 
          'description'     : 'dasdas',
          'image_list'      : [{'id': 1, 'image_url': 'asdasdasdasdasdasdsa.jpg'}, 
                               {'id': 2, 'image_url': 'asdasdasdasdasdasdsa.jpg'}], 
          'tag_list'        : [{'id': 1, 'name'     : '하이하이'},
                               {'id': 2, 'name'     : '하이하이2'}], 
          'company_name'    : 'test1', 
          'company_address' : '서울 동대>문구 한천로 63길 10',
          'company_area'    : '서울', 
          'latitude'        : '19.1212120000', 
          'longitude'       : '20.1212100000'}]})

    def test_notification_detail_get_notification_does_not_exist(self):
        client=Client()
        response = client.get('/notifications/555')
        self.assertEqual(response.json(),{'MESSAGE':'NOTIFICATION_DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)