__author__ = 'longwei'

import sys
import re
from webob import Request
from webob import exc

var_regex = re.compile(r'''
\{          # The exact character "{"
(\w+)       # The variable name (restricted to a-z, 0-9, _)
(?::([^}]+))? # The optional :regex part
\}          # The exact character "}"
''', re.VERBOSE)

def template_to_regex(template):
    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    # force the re to match the complete string
    regex = '^%s$' % regex
    return regex

def load_controller(string):
    module_name, function_name = string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, function_name)
    return func


class Router(object):
    def __int__(self):
        self.routes = []

    def add_routes(self, template, controller, **var):
        if isinstance(controller, basestring):
            controller = load_controller(controller)
            self.routes.append((re.compile(template_to_regex(template)), controller, vars))

    def __call__(self, environ, start_response):
        req = Request(environ)
        # vars is any extra variables
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)

