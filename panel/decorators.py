from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url='panel:login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Staff access required.')
        return view_func(request, *args, **kwargs)

    return wrapper
