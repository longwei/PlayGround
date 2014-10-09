from unittest import TestCase
from template import TOK_REGEX


__author__ = 'longwei'


class Test(TestCase):
    def test_tokenize(self):
        result = TOK_REGEX.split('{% each vars %}<i>{{it}}</i>{% endeach %}')
        print result
