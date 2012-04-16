from django.conf import settings
from django.test import TestCase, Clienta
from django.contrib.auth.models import User
from test_utils import AjaxTestMixin

class AjaxTestCase(TestCase, AjaxTestMixin):
    def setUp(self):
        TestCase.setUp(self)

        self.client_anonymous = Client()

        self.user = User.objects.create_user('ajax', 'ajax@ajax.com', 'ajaxrocks')
        self.client = Client()
        self.assertTrue(self.client.login(username='ajax', password='ajaxrocks'))

class AjaxViewTest(AjaxTestCase):
    def test_get_call(self):
        response = self.ajax_get('ajax.ajax.test_get')
        data = self.ajax_data(response)
        self.assertEqual(data, {})

        response = self.ajax_post('ajax.ajax.test_get')
        self.assertEqual(response.status_code, 404)

        response = self.ajax_get('ajax.ajax.test_get_with_param', argv={ 'param': 'test' })
        data = self.ajax_data(response)
        self.assertEqual(data, { 'param': 'test' })

        response = self.ajax_get('ajax.ajax.test_get_login_required')
        data = self.ajax_data(response)
        self.assertEqual(data, {})

        response = self.ajax_get('ajax.ajax.test_get_login_required', client=self.client_anonymous)
        data = self.ajax_data(response)
        self.assertEqual(data, { '_ajax_redirect': settings.LOGIN_URL })

    def test_post_call(self):
        response = self.ajax_post('ajax.ajax.test_post')
        data = self.ajax_data(response)
        self.assertEqual(data, {})

        response = self.ajax_get('ajax.ajax.test_post')
        self.assertEqual(response.status_code, 404)

        response = self.ajax_post('ajax.ajax.test_post_with_param', argv={ 'param': 'test' })
        data = self.ajax_data(response)
        self.assertEqual(data, { 'param': 'test' })

        response = self.ajax_post('ajax.ajax.test_post_login_required')
        data = self.ajax_data(response)
        self.assertEqual(data, {})

        response = self.ajax_post('ajax.ajax.test_post_login_required', client=self.client_anonymous)
        data = self.ajax_data(response)
        self.assertEqual(data, { '_ajax_redirect': settings.LOGIN_URL })
