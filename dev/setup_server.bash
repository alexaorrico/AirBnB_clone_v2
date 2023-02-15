#!/bin/bash
# various bash commands to setup environment
# TODO: create setup script or Docker Container that has these configurations
# Make it happen!
# sudo $MYSQL_ROOT_PASS=[PASSWORD] ./dev/setup.bash

$dir_path="~/github.com/johncoleman83/AirBnB_clone_v3/"

apt-get update
apt apt install -y --force-yes \
    git valgrind puppet shellcheck vim emacs \
    python3-pip python3-dev libmysqlclient-dev zlib1g-dev
wget http://dev.mysql.com/get/mysql-apt-config_0.6.0-1_all.deb
dpkg -i mysql-apt-config_0.6.0-1_all.deb
apt-get update
apt-get install -y --force-yes mysql-server
rm mysql-apt-config_0.6.0-1_all.deb
service mysql start
mkdir -p ~/github.com/johncoleman83/
cd ~/github.com/johncoleman83/
git clone https://github.com/jarehec/AirBnB_clone_v3.git
cd AirBnB_clone_v3
pip3 -install -r requirements.txt
cat dev/7-dump.sql | mysql -uroot -p"$MYSQL_ROOT_PASS"
cp config/nginx.default /etc/nginx/sites-available/default
cp config/airbnb* /etc/init/
start airbnb
