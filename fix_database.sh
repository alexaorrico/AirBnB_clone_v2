#!/usr/bin/env bash
# this will fix the database problems

echo "DROP DATABASE IF EXISTS hbnb_dev_db;" | mysql -uroot -p
cmd setup_mysql_dev.sql | mysql -uroot -p
echo "USE hbnb_dev_db;" | mysql -uroot -p
cmd 100-hbnb.sql | mysql -uroot -p
echo "Database hbnb_dev_db and password hbnb_dev_pwd setup and ready for use"
