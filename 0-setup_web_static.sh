#!/usr/bin/env bash
# install & configure nginx

apt-get update -y
apt-get install -y nginx

wb_path="/data/web_static"
mkdir -p "$wb_path/releases/test/"
mkdir -p "$wb_path/shared/"
echo "Holberton School" > "$wb_path/releases/test/index.html"
ln -sf "$wb_path/releases/test/" "$wb_path/current"

chown -R ubuntu "$wb_path"
chgrp -R ubuntu "$wb_path"

nginx_config="/etc/nginx/sites-available/default"
cat > "$nginx_config" <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias $wb_path/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}
EOF

service nginx restart
