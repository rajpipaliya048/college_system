from functools import wraps
from django.http import HttpResponseForbidden

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Permission Denied: You must be a superuser to access this view.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view