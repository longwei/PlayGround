from unittest import TestCase
import Router

__author__ = 'longwei'


class TestLoad_controller(TestCase):
    def test_load_controller(self):
        func = Router.load_controller('App:echo')
        self.assertEqual(func("hello world"), "hello world")


class TestTemplate_to_regex(TestCase):
    def test_template_to_regex_static(self):
        result = Router.template_to_regex('/a/static/path')
        expect = '^\/a\/static\/path$'
        self.assertEqual(result,expect)
    def test_template_to_regex_dynamic(self):
        result = Router.template_to_regex('/{year:\d\d\d\d}/{month:\d\d}/{slug}')
        expect = '^\/(?P<year>\d\d\d\d)\/(?P<month>\d\d)\/(?P<slug>[^/]+)$'
        self.assertEqual(result,expect)