#!/usr/bin/env bash
# sets up the web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "This is a test" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx start

https://www.google.com/search?q=hotel+near+me&sca_esv=569950492&sxsrf=AM9HkKm3tJo96KpibpzmYOKQONBHGYjzpQ%3A1696234369982&ei=gXsaZd7FO4yPxc8PnbWJuAE&ved=0ahUKEwieitC49daBAxWMR_EDHZ1aAhcQ4dUDCBA&uact=5&oq=hotel+near+me&gs_lp=Egxnd3Mtd2l6LXNlcnAiDWhvdGVsIG5lYXIgbWUyBxAjGLECGCcyBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIGEAAYBxgeMgYQABgHGB5IzCFQqQpYkSBwAngBkAEAmAG7AqAB9QqqAQcwLjEuNC4xuAEDyAEA-AEBwgIKEAAYRxjWBBiwA8ICDRAAGEcY1gQYyQMYsAPCAgsQABiKBRiSAxiwA8ICChAAGIoFGLADGEPCAg4QABjkAhjWBBiwA9gBAcICFhAuGIoFGMcBGNEDGMgDGLADGEPYAQLCAgcQIxiKBRgnwgINEAAYigUYsQMYgwEYQ-IDBBgAIEGIBgGQBhC6BgYIARABGAm6BgYIAhABGAg&sclient=gws-wiz-serp&bshm=rimc/1