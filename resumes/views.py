import json

from django.views import View
from django.http  import JsonResponse,FileResponse

from users.utils  import login_required

from .models      import Resume,FileResume,Career

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
