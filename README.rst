===========
Django Ajax
===========

A simple barebone way to implement ajax for Django.

Usage
=====

In any of your apps, create an ajax.py file.
Define your ajax functions with the @ajax_get or @ajax_post decorator::

    from ajax.decorators import ajax_get, ajax_post, ajax_login_required

    @ajax_get
    def list_something(request):
        return { 'list': [1, 2, 3] }

    @ajax_post
    @ajax_login_required
    def save_something(request, number, text):
        # if the user is not logged in, they will be redirected to login first.
        # ...
        return {}

Your ajax function has to always return a dict which will be jsonified.

In your main urls.py, add::

    import ajax
    ajax.autodiscover()

Also in urls.py, add the following to your urlpatterns::

    url(r'^ajax/', include('ajax.urls', namespace='ajax')),

A sample client side coffeescript is provided::

    ajax.get('yourapp.ajax.list_something', {}, function(data, error) {
        if (!data) {
            console.log('ERROR: ' + error);
            return;
        }
        console.log(data.list);
    });

    ajax.post('yourapp.ajax.save_something', { number: 1, text: 'bla' }, function(data, error) {
        if (!data) {
            console.log('ERROR: ' + error);
            return;
        }
        console.log('It worked!');
    });

The coffeescript utility takes care of csrftoken and the special '_ajax_redirect' (for redirecting user to login).

That's it. Enjoy!

