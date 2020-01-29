#!/bin/bash

sudo service mysql start

echo "CREATE USER 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';" | sudo mysql -uroot -proot
echo "GRANT ALL ON *.* TO 'hbnb_dev'@'localhost';" | sudo mysql -uroot -proot
echo "CREATE DATABASE hbnb_dev_db;" | sudo mysql -uroot -proot
