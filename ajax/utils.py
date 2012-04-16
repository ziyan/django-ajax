from django.http import Http404
from django.utils import simplejson
from django.utils.importlib import import_module
from . import ajax_get_functions, ajax_post_functions

def safe_dict(dictionary):
    """
    Recursively clone json structure with UTF-8 dictionary keys
    http://www.gossamer-threads.com/lists/python/bugs/684379
    """
    if isinstance(dictionary, dict):
        return dict([(key.encode('utf-8'), safe_dict(value)) for key, value in dictionary.iteritems()])
    elif isinstance(dictionary, list):
        return [safe_dict(x) for x in dictionary]
    else:
        return dictionary

def register_function(module, name, is_post=False):
    global ajax_get_funcitons, ajax_post_functions

    function = '%s.%s' % (module, name)
    if (function in ajax_get_functions) or (function in ajax_post_functions):
        return

    if is_post:
        ajax_post_functions.append(function)
    else:
        ajax_get_functions.append(function)

def call_function(request, function):
    global ajax_get_funcitons, ajax_post_functions

    argv = None

    if request.method == "GET":
        if not function in ajax_get_functions:
            raise Http404
        argv = request.GET.get('argv', None)
    elif request.method == "POST":
        if not function in ajax_post_functions:
            raise Http404
        argv = request.POST.get('argv', None)
    else:
        raise Http404

    if not argv is None:
        argv = simplejson.loads(argv)
        argv = safe_dict(argv)
    else:
        argv = {}

    function_parts = function.rsplit('.', 1)
    module_name = function_parts[0]
    function_name = function_parts[1]
    mod = import_module(module_name)
    func = mod.__getattribute__(function_name)

    return func(request, **argv)
