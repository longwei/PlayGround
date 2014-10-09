from unittest import TestCase
from template import *


__author__ = 'longwei'


class Test(TestCase):


    def test_var(self):
        input = "<div>{{ item }}<div>"
        rendered = Template(input).render(item = 'foo')
        print rendered

    def test_each(self):
        input = '{% each items %}<div>{{it}}</div>{% end %}'
        rendered = Template(input).render(items = ['foo', 'bar'])
        print rendered

    def test_each2(self):
        input = '{% each [1,2,3] %}<div>{{it}}</div>{% end %}'
        rendered = Template(input).render(items = ['foo', 'bar'])
        print rendered

    # def test_each(self):
    #     input = "{% each items %} <div>{{ it }}<div> {%end%}"
    #     rendered = Template(input).render(items = ['foo','bar'])
    #     print rendered

    def test_tokenize(self):
        result = TOK_REGEX.split('{% each vars %}<i>{{it}}</i>{% endeach %}')
        self.assertEquals(result, ['', '{% each vars %}', '<i>', '{{it}}', '</i>', '{% endeach %}', ''])





