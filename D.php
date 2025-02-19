<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
</body>
</html>

sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/phptest

server {
        listen 80;
        listen [::]:80;

        root /var/www/example.com/html;
        index index.html index.htm index.nginx-debian.html;

        server_name example.com www.example.com;

        location / {
                try_files $uri $uri/ =404;
        }
}

sudo cp /etc/nginx/sites-available/phptest /etc/nginx/sites-available/caretest

sudo ln -s /etc/nginx/sites-available/phptest /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/caretest /etc/nginx/sites-enabled/