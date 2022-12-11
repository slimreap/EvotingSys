from tokenize import group
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser

from functools import wraps


def session_login_required(function=None, session_key='user'):
    def decorator(view_func):
        @wraps(view_func)
        def f(request, *args, **kwargs):
            if session_key in request.session:
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, 'Please login')
            return redirect('public:home')
        return f
    if function is not None:
        return decorator(function)
    return decorator

def authenticated_user(view_func) :
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
    
            return view_func(request, *args, **kwargs)

        else : 
            messages.warning(request, "please fucking login")
            return redirect('public:home')

    return wrapper_func


def unathorized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('public:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            else:
                messages.warning(request, 'Access restricted, for admin only')
                return redirect('public:home')
        return wrapper_func
    return decorator