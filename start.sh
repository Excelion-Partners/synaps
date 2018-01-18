#!/bin/bash

# NETWORK CONNECT ##############################################################
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

systemctl stop hostapd
systemctl stop dnsmasq

python /usr/pyNetworkConnect/python/main.py

# postgres
bash /usr/bash/postgres-init.sh

# By default docker gives us 64MB of shared memory size but to display heavy
# pages we need more.
umount /dev/shm && mount -t tmpfs shm /dev/shm

# using local electron module instead of the global electron lets you
# easily control specific version dependency between your app and electron itself.
# the syntax below starts an X istance with ONLY our electronJS fired up,
# it saves you a LOT of resources avoiding full-desktops envs

rm /tmp/.X0-lock &>/dev/null || true

cd /usr/src/socket/ && node index.js & sleep 5 & cd /usr/src/app/video-analysis && python3 main.py & startx /usr/src/app/node_modules/electron/dist/electron /usr/src/app --enable-logging 

while true
do
	sleep 5
done
