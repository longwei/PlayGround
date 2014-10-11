__author__ = 'longwei'

import re
import operator
import ast


# def enum(*sequential, **named):
#     enums = dict(zip(sequential, range(len(sequential))), **named)
#     return type('Enum', (), enums)

def enum(**enums):
    return type('Enum', (), enums)

TOKEN_TYPE = enum(VAR_FRAGMENT=0, OPEN_BLOCK_FRAGMENT=1, CLOSE_BLOCK_FRAGMENT=2, TEXT_FRAGMENT=3)

WHITESPACE = re.compile('\s+')
VAR_START = '{{'
VAR_END = '}}'
BLOCK_START = '{%'
BLOCK_END = '%}'
TOK_REGEX = re.compile(r"(%s.*?%s|%s.*?%s)" % (
    VAR_START,
    VAR_END,
    BLOCK_START,
    BLOCK_END
))

operator_lookup_table = {
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}

class TemplateError(Exception):
    pass

class TemplateContextError(TemplateError):

    def __init__(self, context_var):
        self.context_var = context_var

    def __str__(self):
        return "cannot resolve '%s'" % self.context_var

class TemplateSyntaxError(TemplateError):

    def __init__(self, fragment):
        self.fragment_var = fragment

    def __str__(self):
        return "SyntaxError '%s'" % self.fragment



def eval_expression(expr):
    try:
        return 'literal', ast.literal_eval(expr)
    except ValueError, SyntaxError:
        return 'name', expr


def resolve(name, context):
    if name.startswith('..'):
        context = context.get('..', {})
        name = name[2:]
    try:#resolve name.foo.bar
        for tok in name.split('.'):
            context = context[tok]
        return context
    except KeyError:
        raise TemplateContextError(name)


#text fragment just after regex split, {{ var}} {% each ...%},
# need to take out wrapping symbol for ast node
class _Fragment(object):
    def __init__(self, raw_text):
        self.raw = raw_text
        self.clean = self.clean_fragment()

    def clean_fragment(self):
        if self.raw[:2] in (VAR_START, BLOCK_START):
            return self.raw.strip()[2:-2].strip()
        return self.raw

    @property
    def type(self):
        raw_start = self.raw[:2]
        if raw_start == VAR_START:
            return TOKEN_TYPE.VAR_FRAGMENT
        elif raw_start == BLOCK_START:#normal open block {% whatever ...%} or close symbol {% end %}
            return TOKEN_TYPE.CLOSE_BLOCK_FRAGMENT if self.clean[:3] == 'end' else TOKEN_TYPE.OPEN_BLOCK_FRAGMENT
        else:
            return TOKEN_TYPE.TEXT_FRAGMENT

class _Node(object):
    creates_scope = False

    def __init__(self, fragment=None):
        self.children = []
        self.process_fragment(fragment)

    def process_fragment(self, fragment):
        pass

    def enter_scope(self):
        pass

    def render(self, context):
        pass

    def exit_scope(self):
        pass

    def render_children(self, context, children=None):
        if children is None:
            children = self.children
        def render_child(child):
            child_html = child.render(context)
            return '' if not child_html else str(child_html)
        return ''.join(map(render_child, children))



class _ScopableNode(_Node):
    creates_scope = True

class _Root(_Node):
    def render(self, context):
        return self.render_children(context)

class _Variable(_Node):
    def process_fragment(self, fragment):
        self.name = fragment

    def render(self, context):
        return resolve(self.name, context)

class _Text(_Node):
    def process_fragment(self, fragment):
        self.text = fragment

    def render(self, context):
        return self.text

#      root()
#        |
#      each
#   /   |   \
#  {{   it   }}
class _Each(_ScopableNode):
    def process_fragment(self, fragment):
        try:
            # fragment is like "each list_var"
            _, it = WHITESPACE.split(fragment, 1)
            self.it = eval_expression(it) #('name' | 'literal', list_var)
        except ValueError:
            raise TemplateSyntaxError(fragment)

    def render(self, context):
        items = self.it[1] if self.it[0] == 'literal' else resolve(self.it[1], context)
        def render_item(item):
            return self.render_children({'..': context, 'it': item})
        return ''.join(map(render_item, items))


#      parent()
#        |
#       ifNode-------------
#      / | \    \          \
#    lhs op rhs  if_branch else_branch
class _If(_ScopableNode):
    def process_fragment(self, fragment):
        # foo > bar or BooleanValue
        compareBool = fragment.split()[1:]
        if len(compareBool) not in (1, 3):
            raise TemplateSyntaxError(fragment)
        #get the type for left and right side
        self.lhs = eval_expression(compareBool[0])
        if len(compareBool) == 3:
            self.op = compareBool[1]
            self.rhs = eval_expression(compareBool[2])

    def render(self, context):
        lhs = self.resolve_side(self.lhs, context)
        if hasattr(self, 'op'):
            op = operator_lookup_table.get(self.op)
            if op is None:
                raise TemplateSyntaxError(self.op)
            rhs = self.resolve_side(self.rhs, context)
            exec_if_branch = op(lhs, rhs)
        else:
            exec_if_branch = operator.truth(lhs)
        if_branch, else_branch = self.split_children()
        return self.render_children(context,
            self.if_branch if exec_if_branch else self.else_branch)

    def resolve_side(self, side, context):
        return side[1] if side[0] == 'literal' else resolve(side[1], context)

    def exit_scope(self):
        self.if_branch, self.else_branch = self.split_children()

    def split_children(self):
        if_branch, else_branch = [], []
        curr = if_branch
        for child in self.children:
            if isinstance(child, _Else):
                curr = else_branch
                continue
            curr.append(child)
        return if_branch, else_branch

class _Else(_Node):
    def render(self, context):
        pass

class _Call(_Node):
    def process_fragment(self, fragment):
        try:
            bits = WHITESPACE.split(fragment)
            self.callable = bits[1]
            self.args, self.kwargs = self._parse_params(bits[2:])
        except ValueError, IndexError:
            raise TemplateSyntaxError(fragment)

    def _parse_params(self, params):
        args, kwargs = [], {}
        for param in params:
            if '=' in param:
                name, value = param.split('=')
                kwargs[name] = eval_expression(value)
            else:
                args.append(eval_expression(param))
        return args, kwargs

    def render(self, context):
        resolved_args, resolved_kwargs = [], {}
        for kind, value in self.args:
            if kind == 'name':
                value = resolve(value, context)
            resolved_args.append(value)
        for key, (kind, value) in self.kwargs.iteritems():
            if kind == 'name':
                value = resolve(value, context)
            resolved_kwargs[key] = value
        resolved_callable = resolve(self.callable, context)
        if hasattr(resolved_callable, '__call__'):
            return resolved_callable(*resolved_args, **resolved_kwargs)
        else:
            raise TemplateError("'%s' is not a callable" % self.callable)


class Compiler(object):
    def __init__(self, template_string):
        self.template_string = template_string

    def each_fragment(self):
        for fragment in TOK_REGEX.split(self.template_string):
            if fragment:
                yield _Fragment(fragment)

    def compile(self):
        root = _Root()
        scope_stack = [root]
        for fragment in self.each_fragment():
            if not scope_stack:
                raise TemplateError('nesting issues')
            parent_scope = scope_stack[-1]
            if fragment.type == TOKEN_TYPE.CLOSE_BLOCK_FRAGMENT:
                parent_scope.exit_scope()
                scope_stack.pop()
                continue
            new_node = self.create_node(fragment)
            if new_node:
                #append every node this this scope until we see a {% end %}
                parent_scope.children.append(new_node)
                if new_node.creates_scope:
                    scope_stack.append(new_node)
                    new_node.enter_scope()
        return root

    def create_node(self, fragment):
        node_class = None
        if fragment.type == TOKEN_TYPE.TEXT_FRAGMENT:
            node_class = _Text
        elif fragment.type == TOKEN_TYPE.VAR_FRAGMENT:
            node_class = _Variable
        elif fragment.type == TOKEN_TYPE.OPEN_BLOCK_FRAGMENT:
            cmd = fragment.clean.split()[0]
            if cmd == 'each':
                node_class = _Each
            elif cmd == 'if':
                node_class = _If
            elif cmd == 'else':
                node_class = _Else
            elif cmd == 'call':
                node_class = _Call
        if node_class is None:
            raise TemplateSyntaxError(fragment)
        return node_class(fragment.clean)


class Template(object):
    def __init__(self, contents):
        self.contents = contents
        self.root = Compiler(contents).compile()

    def render(self, **kwargs):
        return self.root.render(kwargs)