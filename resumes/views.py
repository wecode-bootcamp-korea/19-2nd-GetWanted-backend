import json
import unicodedata

from urllib.parse import unquote
from datetime     import datetime

from django.db.models import Count
from django.views     import View
from django.http      import JsonResponse

from users.utils      import login_required
from .utils           import user_infomation
from .models          import Resume,FileResume,Career

# Create your views here.

class ResumeView(View):
    @login_required
    def post(self,request):
        try:
            data         = json.loads(request.body)
            resume_id    = data.get('resume_id')
            careers_data = data.get('workInfo')

            resume, created = Resume.objects.update_or_create(
                id       = resume_id,
                user     = request.user,
                defaults = {
                    'title'        : data['title'],
                    'name'         : data['fullName'],
                    'phone_number' : data['phone'],
                    'email'        : data['email'],
                    'introduction' : data.get('intro',''),
                    'status'       : data.get('isFinal',0)
                }
            )
            if careers_data:
                for career_data in careers_data:
                    is_working    = 0
                    end_working   = ''
                    start_working = f"{career_data.get('startYear')}-{career_data.get('startMonth')}"

                    if career_data.get('isWorking'):
                        is_working  = 1
                        end_working = f"{career_data.get('endYear')}-{career_data.get('endMonth')}"

                    Career.objects.update_or_create(
                        id       = career_data.get('career_id'),
                        resume   = resume,
                        defaults = {
                            'is_working'    : is_working,
                            'start_working' : start_working,
                            'end_working'   : end_working,
                            'company_name'  : career_data.get('companyName',''),
                            'department'    : career_data.get('position',''),
                            'description'   : career_data.get('details','')
                        }
                    )
                return JsonResponse({'MESSAGE':'SUCCESS'},status=201)
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'},status=400)

    @login_required
    def get(self,request,resume_id=None):
        user = request.user

        if not resume_id:
            results = user_infomation(user)
            return JsonResponse({'MESSAGE':'SUCCESS', 'RESULTS':results}, status=200)

        if not Resume.objects.filter(id=resume_id).exists():
            return JsonResponse({'MESSAGE':'NOT_FOUND_RESUME'},status=404)

        resume  = Resume.objects.get(id=resume_id)
        results = {
            'id'       : resume.id,
            'title'    : resume.title,
            'intro'    : resume.introduction,
            'fullName' : resume.name,
            'phone'    : resume.phone_number,
            'email'    : resume.email,
            'workInfo' : [{
                'id'          : career.id,
                'isWorking'   : career.is_working,
                'startYear'   : career.start_working.split('-')[0],
                'startMonth'  : career.start_working.split('-')[-1],
                'endYear'     : career.end_working.split('-')[0],
                'endMonth'    : career.end_working.split('-')[-1],
                'companyName' : career.company_name,
                'position'    : career.department,
                'details'     : career.description
            }for career in resume.career_set.all()]
        }
        return JsonResponse({'MESSAGE':'SUCCESS','RESULTS':results},status=200)

    @login_required
    def delete(self,request,resume_id=None):
        try:
            if not Resume.objects.filter(id=resume_id).exists():
                return JsonResponse({"MESSAGE":"RESUME_NOT_FOUND"},status=404)

            Resume.objects.get(id=resume_id).delete()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)

class ResumeListView(View):
    @login_required
    def get(self,request):
        user    = request.user
        results = {
            'fileresume_list' : [{
                'id'   : file.id,
                'url'  : file.file_url,
                'name' : unquote(unicodedata.normalize('NFKD',file.file_url.split('/')[-1]).encode('utf-8')),
                'date' : file.updated_at.strftime('%Y-%m-%d')
            }for file in user.fileresume_set.all()],
            'resume_list' : [{
            'id'     : resume.id,
            'name'   : resume.title,
            'date'   : resume.updated_at.strftime('%Y-%m-%d'),
            'status' : resume.status
        }for resume in user.resume_set.all()]}
        return JsonResponse({'MESSAGE':'SUCCESS','RESULTS':results},status=200)
