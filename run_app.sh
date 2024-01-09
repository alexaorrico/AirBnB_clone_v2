#!/bin/bash

export HBNB_MYSQL_USER=hbnb_dev
export HBNB_MYSQL_PWD=hbnb_dev_pwd
export HBNB_MYSQL_HOST=0.0.0.0
export HBNB_MYSQL_DB=hbnb_dev_db
export HBNB_TYPE_STORAGE=db
export HBNB_API_HOST=0.0.0.0
export HBNB_API_PORT=5000

python3 -m api.v1.app