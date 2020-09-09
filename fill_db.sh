#!/bin/bash
service mysql start
MYSQL_PWD=root
cat 7-dump.sql | mysql -uroot -p$MYSQL_PWD
cat 10-dump.sql | mysql -uroot -p$MYSQL_PWD
cat 100-dump.sql | mysql -uroot -p$MYSQL_PWD
