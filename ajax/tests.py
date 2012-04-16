from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth.models import User
from test_utils import AjaxTestMixin
from decorators import ajax_get, ajax_post, ajax_login_required

@ajax_get
def get(request):
    return {}

@ajax_get
def get_with_param(request, param):
    return { 'param': param }

@ajax_get
@ajax_login_required
def get_login_required(request):
    return {}

@ajax_post
def post(request):
    return {}

@ajax_post
def post_with_param(request, param):
    return { 'param': param }

@ajax_post
@ajax_login_required
def post_login_required(request):
    return {}

class AjaxTestCase(TestCase, AjaxTestMixin):
    def setUp(self):
        TestCase.setUp(self)

        self.client_anonymous = Client()

        self.user = User.objects.create_user('ajax', 'ajax@ajax.com', 'ajaxrocks')
        self.client = Client()
        self.assertTrue(self.client.login(username='ajax', password='ajaxrocks'))

class AjaxViewTest(AjaxTestCase):
    def test_get_call(self):
        response = self.ajax_get('ajax.tests.get')
        data = self.ajax_data(response)
        self.assertEqual(data, {})

        response = self.ajax_post('ajax.tests.get')
        self.assertEqual(response.status_code, 404)

        response = self.ajax_get('ajax.tests.get_with_param', argv={ 'param': 'test' })
        data = self.ajax_data(response)
        self.assertEqual(data, { 'param': 'test' })

        response = self.ajax_get('ajax.tests.get_login_required')
        data = self.ajax_data(response)
        self.assertEqual(data, {})

        response = self.ajax_get('ajax.tests.get_login_required', client=self.client_anonymous)
        data = self.ajax_data(response)
        self.assertEqual(data, { '_ajax_redirect': settings.LOGIN_URL })

    def test_post_call(self):
        response = self.ajax_post('ajax.tests.post')
        data = self.ajax_data(response)
        self.assertEqual(data, {})

        response = self.ajax_get('ajax.tests.post')
        self.assertEqual(response.status_code, 404)

        response = self.ajax_post('ajax.tests.post_with_param', argv={ 'param': 'test' })
        data = self.ajax_data(response)
        self.assertEqual(data, { 'param': 'test' })

        response = self.ajax_post('ajax.tests.post_login_required')
        data = self.ajax_data(response)
        self.assertEqual(data, {})

        response = self.ajax_post('ajax.tests.post_login_required', client=self.client_anonymous)
        data = self.ajax_data(response)
        self.assertEqual(data, { '_ajax_redirect': settings.LOGIN_URL })
