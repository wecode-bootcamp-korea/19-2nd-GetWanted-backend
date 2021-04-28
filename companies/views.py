import json

from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import Paginator

from .models               import Image, Notification, Tag

class NotificationView(View):
    def get(self,request):
        tag              = request.GET.get('tag',None)
        page             = request.GET.get('page',1)
        notification_zip = Notification.objects.all()

        if tag:
            if not Tag.objects.filter(id=tag).exists():
                return JsonResponse({'MESSAGE': 'TAG_DOES_NOT_EXIST'},status=404)
            notification_zip = Tag.objects.get(id=tag).notification_set.all()

        paginator     = Paginator(notification_zip,16)
        notifications = paginator.get_page(page)

        notification_list = [{
            'title'   : notification.title,
            'image'   : notification.image_set.first().image_url,
            'id'      : notification.id,
            'area'    : notification.company.address.split()[0],
            'company' : notification.company.name
            } for notification in notifications]

        return JsonResponse({'notification_list' : notification_list, 'total' : len(notification_zip)}, status = 200)

class TagView(View):
    def get(self,request):
        tags = Tag.objects.all()
        tag_list =[{
            'id'   : tag.id,
            'name' : tag.name
        } for tag in tags]

        return JsonResponse({'tag_list': tag_list}, status=200)