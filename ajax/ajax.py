from decorators import ajax_get, ajax_post, ajax_login_required

@ajax_get
def test_get(request):
    return {}

@ajax_get
def test_get_with_param(request, param):
    return { 'param': param }

@ajax_get
@ajax_login_required
def test_get_login_required(request):
    return {}

@ajax_post
def test_post(request):
    return {}

@ajax_post
def test_post_with_param(request, param):
    return { 'param': param }

@ajax_post
@ajax_login_required
def test_post_login_required(request):
    return {}
