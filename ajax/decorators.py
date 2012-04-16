from functools import wraps
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
from utils import register_function

def ajax_response(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        request = args[0]
        data = function(*args, **kwargs)
        if not isinstance(data, dict):
            raise ValueError('The ajax view function should return a dict.')
        response = simplejson.dumps(data)
        if request.META.get('HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest':
            return HttpResponse(response, mimetype='application/x-json')
        return HttpResponse(response)
    return wrapper

def ajax_post(function):
    register_function(function.__module__, function.__name__, True)
    print function.__module__, function.__name__
    return ajax_response(function)

def ajax_get(function):
    register_function(function.__module__, function.__name__, False)
    return ajax_response(function)

def ajax_login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated():
            return function(*args, **kwargs)
        return { '_ajax_redirect': settings.LOGIN_URL }
    return wrapper
