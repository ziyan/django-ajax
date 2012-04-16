from django.core.urlresolvers import reverse
from django.utils import simplejson
import urllib

class AjaxTestMixin(object):

    def ajax_get(self, function, argv=None, client=None, follow=True):
        client = client or self.client
        url = reverse('call', args=[function])
        if argv is not None:
            url = '%s?%s' % (url, urllib.urlencode({ 'argv': simplejson.dumps(argv) }))
        return client.get(url, follow=follow)

    def ajax_post(self, function, argv=None, client=None, follow=True):
        client = client or self.client
        url = reverse('call', args=[function])
        data = {}
        if argv is not None:
            data = { 'argv': simplejson.dumps(argv) }
        return client.post(url, data, follow=follow)

    def ajax_data(self, response):
        self.assertEqual(response.status_code, 200)
        return simplejson.loads(response.content)

    def assertAjaxPostSuccess(self, *args, **kwargs):
        response = self.ajax_post(*args, **kwargs)
        return self.ajax_data(response)

    def assertAjaxGetSucess(self, *args, **kwargs):
        response = self.ajax_get(*args, **kwargs)
        return self.ajax_data(response)

    def assertAjaxRedirectTo(self, response, url, ignore_parameters=True):
        data = self.ajax_data(response)
        self.assertIn('_ajax_redirect', data, 'The response did not redirect.')
        actual = data['_ajax_redirect']
        self.assertEquals(data, { '_ajax_redirect': actual })
        if ignore_parameters:
            index = actual.find('?')
            if index > -1:
                actual = actual[:index]
        self.assertEqual(actual, url)
