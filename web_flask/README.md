# AirBnB Clone - Web Framework

## Overview

The "AirBnB Clone - Web Framework" series(at this stage) is a web-based implementation of the AirBnB platform using the ***Flask*** web framework. `Flask` is a micro web framework written in Python, and it is used to build web applications in a simple and efficient manner. In this project, we leverage Flask's features to create a dynamic web application


## Built With:

The project is built using the following technologies:

- *Flask*: The web framework that forms the backbone of the application. Flask provides routing mechanisms, templating support, and handling of HTTP requests and responses.

- *Jinja2* Templating Engine: Jinja2 is a powerful templating engine that is integrated with Flask. It allows us to create dynamic HTML templates with placeholders that get filled with data from the backend.

- *SQLAlchemy ORM*: SQLAlchemy is a popular Object-Relational Mapping library that enables us to interact with the database using Python objects and methods. It abstracts the database interactions and provides a higher-level, Pythonic interface.

- *MySQL Database*: The project uses a MySQL database to store and manage the application's data, such as user information, cities, and states, reviews etc.


## Flask:
Flask is a lightweight [`WSGI`](https://wsgi.readthedocs.io/en/latest/) web application framework. You can design with it quickly, with the ability to scale up to complex applications. It began as a simple wrapper around [Werkzeug](https://palletsprojects.com/p/werkzeug/) and [Jinja](https://palletsprojects.com/p/jinja/) and has become one of the most popular Python web application frameworks.

Flask offers suggestions, but doesn't enforce any dependencies or project layout. It is up to the developer to choose the tools and libraries they want to use. There are many extensions provided by the community that make adding new functionality easy.
```bash
$ cat app.py
#!/usr/bin/python3
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
$
```

```bash
$ export FLASK_APP=app.py && export FLASK_DEBUG=True && flask run --reload
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Jinja:
> Jinja is Beautiful.  

Jinja2 is a full-featured template engine for Python. It has full unicode support, an optional integrated sandboxed execution environment, powerful automatic HTML escaping system for cross site scripting prevention, conveninent configurable syntax e.g. you can reconfigure Jinja2 to better fit output formats such as HTML, LaTeX or JavaScript.

```bash
{% extends "layout.html" %}
{% block body %}
  <ul>
  {% for user in users %}
    <li><a href="{{ user.url }}">{{ user.username }}</a></li>
  {% endfor %}
  </ul>
{% endblock %}
```

## Flask - Jinja
As an example, let's see how we can use Flask and Jinja2 to display a list of cities in a resource endpoint. First off, we define a route in a mock `app.py` to handle requests to the homepage.

```python
@app.route('/hbnb/cities')
def cities():
    # fetch cities from the database:
    cities = City.query.all()

    # render the template and pass the query list to it
    return render_template('index.html', cities=cities)
```

In the `templates/index.html` template, we can use *Jinja2*'s `template` tags to iterate over the cities and display their information.

```html
<!DOCTYPE html>
<html>
<head>
    <title>AirBnB Clone - Cities</title>
</head>
<body>
    <h1>Welcome to AirBnB Clone!</h1>
    <h2>Available Cities:</h2>
    <ul>
        {% for city in cities %}
        <li>{{ city.title }} - {{ city.price }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

When a user visits the cities page, Flask will execute the `cities()` function, fetch the cities from the database, and pass them to the `index.html` template. Jinja2 will then render the HTML with the information dynamically inserted into the page.

## References:

- About: [Flask](https://palletsprojects.com/p/flask/), [Jinja](https://palletsprojects.com/p/jinja/)
- [Jinja Templating](https://jinja.palletsprojects.com/en/3.1.x/templates/)
