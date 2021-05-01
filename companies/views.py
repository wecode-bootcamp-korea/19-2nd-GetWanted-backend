import json

from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import Paginator
from django.db.models      import Q

from .models               import Notification, Tag

class NotificationView(View):
    def get(self,request):
        try:
            tag              = request.GET.get('tag',None)
            page             = request.GET.get('page',1)
            search           = request.GET.get('search', None)
            notification_zip = Notification.objects.select_related('company').prefetch_related('image_set').all()

            if search:
                notification_zip = Notification.objects.select_related('company').prefetch_related('image_set').filter(Q(title__icontains=search) | Q(company__name__icontains=search))

            if tag:
                if not Tag.objects.filter(id=tag).exists():
                    return JsonResponse({'MESSAGE': 'TAG_DOES_NOT_EXIST'},status=404)
                notification_zip  = Notification.objects.select_related('company').prefetch_related('image_set','tag').filter(tag__id=tag)

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

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'},status = 400)


class TagView(View):
    def get(self,request):
        tags = Tag.objects.all()
        tag_list =[{
            'id'   : tag.id,
            'name' : tag.name
        } for tag in tags]

        return JsonResponse({'tag_list': tag_list}, status=200)

class NotificationDetailView(View):
    def get(self,request,notification_id):
        try:
            notification    = Notification.objects.select_related('company').prefetch_related('image_set','tag').get(id=notification_id)
            notification_detail = [{
                'notification_id' : notification.id,
                'title'           : notification.title,
                'description'     : notification.description,
                'image_list'      : [{'id'        : image.id,
                                      'image_url' : image.image_url
                                     } for image in notification.image_set.all()],
                'tag_list'        : [{'id'   : tag.id,
                                      'name' : tag.name
                                     } for tag in notification.tag.all()],
                'company_name'    : notification.company.name,
                'company_address' : notification.company.address,
                'company_area'    : notification.company.address.split()[0],
                'latitude'        : notification.company.latitude,
                'longitude'       : notification.company.longitude 
                }]
            return JsonResponse({'NOTIFICATION_DETAIL' : notification_detail}, status=200)

        except Notification.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'NOTIFICATION_DOES_NOT_EXIST'},status=404)
