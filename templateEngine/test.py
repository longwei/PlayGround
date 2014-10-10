from unittest import TestCase
from template import *


__author__ = 'longwei'


# class TestVarAndTokenized(TestCase):
#     def test_tokenize(self):
#         result = TOK_REGEX.split('{% each vars %}<i>{{it}}</i>{% end %}')
#         self.assertEquals(result, ['', '{% each vars %}', '<i>', '{{it}}', '</i>', '{% end %}', ''])
#
#     def test_tokenize_space(self):
#         result = TOK_REGEX.split('{% each vars%}<i>{{it         }}</i>{% end %}')
#         self.assertEquals(result, ['', '{% each vars%}', '<i>', '{{it         }}', '</i>', '{% end %}', ''])
#
#     def test_tokenize_no_space(self):
#         result = TOK_REGEX.split('{%each vars%}<i>{{it}}</i>{%end%}')
#         self.assertEquals(result, ['', '{%each vars%}', '<i>', '{{it}}', '</i>', '{%end%}', ''])
#
#     def test_var(self):
#         input = "<div>{{ item }}<div>"
#         rendered = Template(input).render(item = 'foo')
#         self.assertEquals(rendered, "<div>foo<div>")
#
#     def test_var_dict(self):
#         input = "<div>{{ item.name }} {{item.age}}<div>"
#         foo = dict(name="John", age=20)
#         rendered = Template(input).render(item = foo)
#         expect = '<div>John 20<div>'
#         self.assertEquals(rendered, expect)
#
# class TestEach(TestCase):
#     def test_each(self):
#         #      root()
#         #        |
#         #      each
#         #   /   |   \
#         #  {{   it   }}
#         input = '{% each items %}<div>{{it}}</div>{% end %}'
#         rendered = Template(input).render(items = ['foo', 'bar'])
#         expect = '<div>foo</div><div>bar</div>'
#         self.assertEquals(rendered, expect)
#
#     def test_each2(self):
#         input = '{% each [1,2,3] %}<div>{{it}}</div>{% end %}'
#         rendered = Template(input).render(items = ['foo', 'bar'])
#         expect = '<div>1</div><div>2</div><div>3</div>'
#         self.assertEquals(rendered, expect)
#
#     def test_each_each(self):
#         input = '{% each items %}<div>{% each it%}<div>{{it}}</div>{%end%}</div>{% end %}'
#         foo = ['foo_1','foo_2']
#         bar = ['bar_1','bar_2']
#         rendered = Template(input).render(items = [foo, bar])
#         expect = '<div><div>foo_1</div><div>foo_2</div></div><div><div>bar_1</div><div>bar_2</div></div>'
#         self.assertEquals(rendered, expect)
#
#     def test_each_parent_context(self):
#         rendered = Template('{% each [1, 2, 3] %}<div>{{..name}}-{{it}}</div>{% end %}').render(name='foo bar')
#         expect = '<div>foo bar-1</div><div>foo bar-2</div><div>foo bar-3</div>'
#         self.assertEquals(rendered, expect)

class IfTests(TestCase):

    def test_simple_if_is_true(self):
        rendered = Template('{% if num > 5 %}<div>more than 5</div>{% end %}').render(num=6)
        self.assertEquals(rendered, '<div>more than 5</div>')

    # def test_shortcut(self):
    #     rendered = Template('{% if True 5 %}<div>more than 5</div>{% end %}').render(num=6)
    #     self.assertEquals(rendered, '<div>more than 5</div>')