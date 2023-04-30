## Web Framework
> In the backend, we use Flask as the web framework and Jinja as the template.

### Resources:
* [What is a web framework?](https://jeffknupp.com/blog/2014/03/03/what-is-a-web-framework/)
* [Flask - Quickstart: Minimal Application, Routing except HTTP methods, Rendering templates](http://flask.pocoo.org/docs/1.0/quickstart/)
* [Jinja - Template Designer: Synopsis, Variables, Comments, Whitespace control, List of Control Structures (read up to Call)](http://jinja.pocoo.org/docs/2.9/templates/)

```
# import data on cities and states into sql database
$ curl -o 7-dump.sql "https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/290/7-states_list.sql"
$ cat 7-dump.sql | mysql -uroot -p
Enter password: 
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m web_flask.8-cities_by_states
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

```
# import data on places into sql database
$ curl -o 10-dump.sql "https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/290/10-hbnb_filters.sql"
$ cat 10-dump.sql | mysql -uroot -p
Enter password: 
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m web_flask.10-hbnb_filters
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

```
# test flask web app displays

# add this line into Vagrantfile on host
config.vm.network :forwarded_port, guest: 5000, host: 5000

# vagrant reload

# open connection
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m web_flask.10-hbnb_filters
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....

# check in browser
0.0.0.0:5000/hbnb or 127.0.0.1:5000/hbnb

# or check in CLI
curl 0.0.0.0:5000/hbnb ; echo ""
```

### Description of what each file shows:
* File 100-hbnb.py and templates/100-hbnb.html is cummulative of all files. The simple web-app shows how to use Flask to map what we see at each route, which html pages, and how to customize the html templates using Jinja. Each file can be run with ```python -m [dirname].[filename]```. This results in ```* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)```. To test the web app is running, for instance, in another terminal we can run ```curl 0.0.0.0:5000/number_odd_or_even/89 ; echo ""``` and should see the return value of our routes. 

### Environment
* Languages: Python 3.4.3, HTML, CSS
* OS: Ubuntu 14.04 LTS
* Framework: Flask ```pip3 install flask```
* Style guidelines: [W3C-Validator](https://github.com/holbertonschool/W3C-Validator) || [PEP 8 (version 1.7) for Python 3.5](https://www.python.org/dev/peps/pep-0008/) || [Google Style Python Docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

---
### Authors
Melissa Ng [![M](https://upload.wikimedia.org/wikipedia/fr/thumb/c/c8/Twitter_Bird.svg/30px-Twitter_Bird.svg.png)](https://twitter.com/MelissaNg__)