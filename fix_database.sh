#!/usr/bin/env bash
# this will fix the database problems

cat setup_mysql_dev.sql | mysql -uroot -p
cat 100-hbnb.sql | mysql -uroot -p
echo "Database hbnb_dev_db and password hbnb_dev_pwd setup and ready for use"
