#!/bin/bash
kill -9 `cat api.pid` > /dev/null 2>&1;
sleep 2;

HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app > /dev/null 2>&1 &
echo $! > api.pid

sleep 5;
HBNB_TYPE_STORAGE=db
echo $HBNB_TYPE_STORAGE
