ajax_get_functions = []
ajax_post_functions = []

def autodiscover():

    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule
    from django.conf import settings

    for app in settings.PROJECT_APPS:
        mod = import_module(app)
        try:
            import_module('%s.ajax' % app)
        except:
            if module_has_submodule(mod, 'ajax'):
                raise
