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





https://docs.djangoproject.com/en/dev/topics/templates/
