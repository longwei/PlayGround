__author__ = 'longwei'

from webob import Request


def application(envion, start_respons):
    start_respons('200 OK', [('Content-Type', 'text/html')])
    return ['Hello World!']


def echo(txt):
    return txt

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('127.0.0.1', 8080, application)
    server.serve_forever()
