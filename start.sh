#!/bin/bash
systemctl stop apache2.service

# NETWORK CONNECT ##############################################################
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

systemctl stop hostapd
systemctl stop dnsmasq

# grafana
GRAFANA_DIR="/data/grafana"
if [ ! -d "$GRAFANA_DIR" ];
then
    mkdir $GRAFANA_DIR
fi

chmod -R 777 /data/grafana

/bin/systemctl daemon-reload
/bin/systemctl enable grafana-server
service grafana-server start

# network connect
python /usr/pyNetworkConnect/python/main.py

# postgres
bash /usr/bash/postgres-init.sh

## apache
echo "starting apache..."
mv /usr/apache/000-default.conf /etc/apache2/sites-available/
sudo a2enmod proxy
sudo a2enmod proxy_http
systemctl start apache2.service

# By default docker gives us 64MB of shared memory size but to display heavy
# pages we need more.
umount /dev/shm && mount -t tmpfs shm /dev/shm

# using local electron module instead of the global electron lets you
# easily control specific version dependency between your app and electron itself.
# the syntax below starts an X istance with ONLY our electronJS fired up,
# it saves you a LOT of resources avoiding full-desktops envs

rm /tmp/.X0-lock &>/dev/null || true

if [ $DASHBOARD = "1" ];
then
    # dashboard
    cd /usr/app/dashboard/
    yarn install 
    # --enable-logging 
    yarn start & echo "starting socket" & cd /usr/app/socket/ && node index.js & sleep 30s & echo "starting electron" & startx /usr/app/electron/node_modules/electron/dist/electron /usr/app/electron & cd /usr/app/video-analysis && python3 main.py 
    # yarn start & sleep 5s && startx /usr/app/electron/node_modules/electron/dist/electron /usr/app/electron --enable-logging & cd /usr/app/socket/ && node index.js & sleep 1s & cd /usr/app/video-analysis && python3 main.py 
else 
    echo "starting socket" & cd /usr/app/socket/ && node index.js & sleep 5s & echo "starting electron" & startx /usr/app/electron/node_modules/electron/dist/electron /usr/app/electron & cd /usr/app/video-analysis && python3 main.py 
fi

while true
do
	sleep 5
done
