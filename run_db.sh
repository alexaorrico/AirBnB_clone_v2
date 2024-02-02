#!/usr/bin/env bash

export HBNB_MYSQL_HOST=localhost
export HBNB_TYPE_STORAGE=db

if [ "$#" -lt 1 ] || [ "$1" = "console" ]; then
    export HBNB_ENV=dev
    export HBNB_MYSQL_USER=hbnb_dev
    export HBNB_MYSQL_PWD=hbnb_dev_pwd
    export HBNB_MYSQL_DB=hbnb_dev_db

    ./console.py
elif [ "$1" = "test" ]; then
    export HBNB_ENV=test
    export HBNB_MYSQL_USER=hbnb_test
    export HBNB_MYSQL_PWD=hbnb_test_pwd
    export HBNB_MYSQL_DB=hbnb_test_db

    # HBNB_MYSQL_HOST=localhost HBNB_TYPE_STORAGE=db HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd HBNB_MYSQL_DB=hbnb_test_db

    if [ "$2" = "dev" ]; then
        export HBNB_MYSQL_USER=hbnb_dev
        export HBNB_MYSQL_PWD=hbnb_dev_pwd
        export HBNB_MYSQL_DB=hbnb_dev_db
    fi

    python3 -m unittest discover tests --local -c # -f
else
    echo 'Usage: '"$0" '[console | test | test dev]'
fi
