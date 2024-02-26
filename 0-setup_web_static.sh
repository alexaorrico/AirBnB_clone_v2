#!/usr/bin/env bash
# prepare your web servers

# install nginx if it's not installed
sudo apt-get -y update
sudo apt-get -y install nginx

# create folders if they don't already exist
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/releases/test/

# create fake html file
sudo echo -e "<html>
<head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# change ownership of data folder
sudo chown -R ubuntu:ubuntu /data

# update nginx config
file=/etc/nginx/sites-available/default
str="location /hbnb_static/{\n\talias /data/web_static/current/;\n}\n"
sudo sed -i "27i $str" $file

sudo service nginx restart
