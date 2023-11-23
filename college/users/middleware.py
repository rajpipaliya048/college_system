from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from users.models import RequestLog


class RequestLoggingMiddleware(MiddlewareMixin):
        
    def process_request(self, request):
        url = request.path_info
        method = request.method
        user = request.user if request.user.is_authenticated else None
        RequestLog.objects.create(user=user, url=url, method=method)
        
class AdminAccessOnlyMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        if request.path == '/course/create/' and not request.user.is_staff:
            return HttpResponseForbidden("Accessible for admins only")
        
class AddSkillsMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        if request.user.is_authenticated and not request.user.is_superuser and not request.path == '/update-skills/' and not request.path.startswith('/admin/'):
            student = request.user.student
            skills = student.skills
            if not skills:
                return render(request, 'users/update_skills.html')
