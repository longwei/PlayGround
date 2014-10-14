from unittest import TestCase
from template import *


__author__ = 'longwei'


class TestVarAndTokenized(TestCase):
    def test_tokenize(self):
        result = TOK_REGEX.split('{% each vars %}<i>{{it}}</i>{% end %}')
        self.assertEquals(result, ['', '{% each vars %}', '<i>', '{{it}}', '</i>', '{% end %}', ''])

    def test_tokenize_space(self):
        result = TOK_REGEX.split('{% each vars%}<i>{{it         }}</i>{% end %}')
        self.assertEquals(result, ['', '{% each vars%}', '<i>', '{{it         }}', '</i>', '{% end %}', ''])

    def test_tokenize_no_space(self):
        result = TOK_REGEX.split('{%each vars%}<i>{{it}}</i>{%end%}')
        self.assertEquals(result, ['', '{%each vars%}', '<i>', '{{it}}', '</i>', '{%end%}', ''])

    def test_var(self):
        input = "<div>{{ item }}<div>"
        rendered = Template(input).render(item = 'foo')
        self.assertEquals(rendered, "<div>foo<div>")

    def test_var_dict(self):
        input = "<div>{{ item.name }} {{item.age}}<div>"
        foo = dict(name="John", age=20)
        rendered = Template(input).render(item = foo)
        expect = '<div>John 20<div>'
        self.assertEquals(rendered, expect)

class TestEach(TestCase):
    def test_each(self):
        input = '{% each items %}<div>{{it}}</div>{% end %}'
        rendered = Template(input).render(items = ['foo', 'bar'])
        expect = '<div>foo</div><div>bar</div>'
        self.assertEquals(rendered, expect)

    def test_iterable_as_literal(self):
        input = '{% each [1,2,3] %}<div>{{it}}</div>{% end %}'
        rendered = Template(input).render(items = ['foo', 'bar'])
        expect = '<div>1</div><div>2</div><div>3</div>'
        self.assertEquals(rendered, expect)

    def test_each_each(self):
        input = '{% each items %}<div>{% each it%}<div>{{it}}</div>{%end%}</div>{% end %}'
        foo = ['foo_1','foo_2']
        bar = ['bar_1','bar_2']
        rendered = Template(input).render(items = [foo, bar])
        expect = '<div><div>foo_1</div><div>foo_2</div></div><div><div>bar_1</div><div>bar_2</div></div>'
        self.assertEquals(rendered, expect)

    def test_each_parent_context(self):
        rendered = Template('{% each [1, 2, 3] %}<div>{{..name}}-{{it}}</div>{% end %}').render(name='foo bar')
        expect = '<div>foo bar-1</div><div>foo bar-2</div><div>foo bar-3</div>'
        self.assertEquals(rendered, expect)

class IfTests(TestCase):
    def test_simple_if_is_true(self):
        rendered = Template('{% if num > 5 %}<div>more than 5</div>{% end %}').render(num=6)
        self.assertEquals(rendered, '<div>more than 5</div>')

    def test_shortcut(self):
        rendered = Template('{% if True %}<div>more than 5</div>{% end %}').render(num=6)
        self.assertEquals(rendered, '<div>more than 5</div>')

    def test_simple_if_is_false(self):
        rendered = Template('{% if num > 5 %}<div>more than 5</div>{% end %}').render(num=4)
        self.assertEquals(rendered, '')

    def test_if_else_if_branch(self):
        rendered = Template('{% if num > 5 %}<div>more than 5</div>{% else %}<div>less than 5</div>{% end %}').render(num=6)
        self.assertEquals(rendered, '<div>more than 5</div>')

    def test_if_else_else_branch(self):
        rendered = Template('{% if num > 5 %}<div>more than 5</div>{% else %}<div>less or equal to 5</div>{% end %}').render(num=4)
        self.assertEquals(rendered, '<div>less or equal to 5</div>')

    def test_nested_if(self):
        tmpl = '{% if num > 5 %}{% each [1, 2] %}{{it}}{% end %}{% else %}{% each [3, 4] %}{{it}}{% end %}{% end %}'
        rendered = Template(tmpl).render(num=6)
        self.assertEquals(rendered, '12')
        rendered = Template(tmpl).render(num=4)
        self.assertEquals(rendered, '34')

    def test_truthy_thingy(self):
        rendered = Template('{% if items %}we have items{% end %}').render(items=[])
        self.assertEquals(rendered, '')
        rendered = Template('{% if items %}we have items{% end %}').render(items=None)
        self.assertEquals(rendered, '')
        rendered = Template('{% if items %}we have items{% end %}').render(items='')
        self.assertEquals(rendered, '')
        rendered = Template('{% if items %}we have items{% end %}').render(items=[1])
        self.assertEquals(rendered, 'we have items')


def pow(m=2, e=2):
    return m ** e

class TestInvoke(TestCase):

    def test_no_args(self):
        rendered = Template('{% call pow %}').render(pow=pow)
        self.assertEquals(rendered, '4')

    def test_positional_args(self):
        rendered = Template('{% call pow 3 %}').render(pow=pow)
        self.assertEquals(rendered, '9')
        rendered = Template('{% call pow 2 3 %}').render(pow=pow)
        self.assertEquals(rendered, '8')

    def test_keyword_args(self):
        rendered = Template('{% call pow 2 e=5 %}').render(pow=pow)
        self.assertEquals(rendered, '32')
        rendered = Template('{% call pow e=4 %}').render(pow=pow)
        self.assertEquals(rendered, '16')
        rendered = Template('{% call pow m=3 e=4 %}').render(pow=pow)
        self.assertEquals(rendered, '81')


class TestInheritance(TestCase):
    def simple_inheritance(self):
        pass