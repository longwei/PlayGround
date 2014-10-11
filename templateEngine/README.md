Overview
========

template engine is the "view" in web mvc.
It combines the html template with the data model.

usage:

```
template = Template('template.html')
data = {"name": foo, "age":23,"address":bar}
output = template.render(data=data)
```
* variables:  ```{{myvar}}```
* condition and comparaisons
  * 
  ```
  {% if apple_count >= 12 %}
    ...
  {% else %}
    ...
  ```
* filter: ```{{ name | lower }}```

* Loops 
  * 
  ```
   {% for friend in friends %}
   {{friend}},
   {% endfor %}
   ..."
  ```
* inheritance
  * base.html
  
  ```
  <!doctype html>
  <html>
    <head>
        {% block head %}{% endblock %}
    </head>
    <body>
        {% block body %}{% end block %}
    </body>
  </html>
  ``` 
  * children.html
  
  ```
  {% extends base.template %}
  {% block head %}
  <title>My first templated page!</title>
  {% endblock %}
  {% block body %}
  <h1>Hello to the templated world!</h1>
  {% endblock %}
  ```


implementation
===
the first step will be make a AST!

text and variables fragments => directly translate
block, type is decide by the first word in the fragment

each node has its own scope


parser:

Node: Text
    | Var
    | block

block: ScopeBlock
     | call
     | else
     | end

ScopeBlock: each | if
====
ScopeStack:
[root x   ][if scope][each scope][...]
```
0
1  {% if x > 0%}
1  ...
2  {% each x.foo%}
1  {% end %}
0  {% end %}
```

REF
===
https://docs.djangoproject.com/en/dev/topics/templates/
http://alexmic.net/building-a-template-engine/