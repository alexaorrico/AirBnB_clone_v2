# API with Swagger

## Description

This Directory contains API files and documenation

## Environment

* __OS:__ Ubuntu 14.04 LTS
* __language:__ Python 3.4.3
* __application server:__ Flask 0.12.2, Jinja2 2.9.6
* __web server gateway:__ gunicorn (version 19.7.1)
* __database:__ mysql Ver 14.14 Distrib 5.7.18
* __documentation:__ Swagger (flasgger==0.6.6)
* __Style:__
  * __python:__ PEP 8 (v. 1.7.0)

## Testing API

* Execute program:

```
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db \
HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
```

* Testing with Swagger:

  * In browser visit path: `/apidocs` or:
  * localhost: `http://0.0.0.0:5000/apidocs`
  * your dowmain: `http://yourdomain/apidocs`

* Testing from CLI:

```
curl -X GET http://0.0.0.0:5000/api/v1/[YOUR API REQUEST]
```

example:
```
curl -X GET http://0.0.0.0:5000/api/v1/states/
```
