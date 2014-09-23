from unittest import TestCase
import app as test
from webob import Request


__author__ = 'longwei'


class TestTemplate_to_regex(TestCase):
    def test_template_to_regex_static(self):
        result = test.template_to_regex('/a/static/path')
        expect = '^\/a\/static\/path$'
        self.assertEqual(result, expect)

    def test_template_to_regex_dynamic(self):
        result = test.template_to_regex('/{year:\d\d\d\d}/{month:\d\d}/{slug}')
        expect = '^\/(?P<year>\d\d\d\d)\/(?P<month>\d\d)\/(?P<slug>[^/]+)$'
        self.assertEqual(result, expect)


class TestUrl(TestCase):
    test.get_request.register(Request.blank('http://localhost/'))
    def test_url(self):
        input = test.url('article', 1, 2, "foo")
        expect = "http://localhost/article/1/2/foo"
        self.assertEqual(input, expect)
    def test_url_with_para(self):
        input = test.url('article', 1, 2, "foo", q='some query')
        expect = 'http://localhost/article/1/2/foo?q=some+query'
        self.assertEqual(input, expect)
