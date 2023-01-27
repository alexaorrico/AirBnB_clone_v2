#!/usr/bin/env bash
# Fixing all the database issues

echo "DROP DATABASE IF EXISTS hbnb_dev_db;" | mysql -uroot -p
cat setup_mysql_dev.sql | mysql -uroot -p
echo "USE hbnb_dev_db;" | mysql -uroot -p
cat 100-hbnb.sql | mysql -uroot -p
echo "Database hbnb_dev_db and password hbnb_dev_pwd setup and ready for use"
