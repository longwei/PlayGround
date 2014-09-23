WSGI
====
It is interface between web server and web applications. It allows code pass around web request in a formal way.
It is like CGI-ish but with more context and meta data

WSGI has a application and a server

1. attaching env variables
2. boilerplate for parsing http headers, status response
3. define routes that point to controllers
4. IOC to create controllers

that's all for basically web framework 
To make a MVC web framework, also needs:

* ORM for manage model
* template engine for generating view
* Form handling
* authentication

routing
======

{RE, module_name:function_name}

input expect result will be:

static uri: 'a/static/path' => '^\/a\/static\/path$' to direct match the uri

dynamic uri: '/{year:\d\d\d\d}/{month:\d\d}/{slug}' => "^\/(?P<year>\d\d\d\d)\/(?P<month>\d\d)\/(?P<slug>[^/]+)$"
so a '/1992/12/anythinghere' will be 
year '1992'
month '12'
slug 'anythinghere'

another way to do is directly give named capturing group syntax:
/(?P<year>\d\d\d\d)/(?P<month>\d\d)/(?P<slug>\w+)

after extract parameter from url, the next step is to loading the controller function:
getattr(module, function_name) will return the function pointer to the controllers

URL generation and request Access
===================
because it is bad idea to have direct link inside html.
relative link are hard to manage and absolute links presume particular location