import network_manager
import connection_reader
import hotspot
import config
import web_server

import sys
import os
import time
import socket
import requests
import json


def internet_connection_exists(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print ex.message
        return False

# check /data/network_connect.connections for saved connections
connections = connection_reader.get_connections(config.ENVIRONMENT.CONNECTIONS_PATH())

# if connections exist, create dbus nm connection objects and add them
if connections is not None:
    sys.stdout.write("Removing all connections.\n")

    network_manager.delete_all_connections()
    # start adding the connections
    for conn in connections:
        network_manager.disconnect_device(conn.Interface())
        time.sleep(2)

        sys.stdout.write(str(conn.GET_PRINTABLE_ConnectionObject()) + "\n")
        network_manager.add_connection(conn)

    connection_reader.delete_all_connections(config.ENVIRONMENT.CONNECTIONS_PATH())
else:
    #check for clear creds flag
    if config.ENVIRONMENT.CLEAR_CONNECTIONS():
        # delete all connections -- this will remove every connection except for Wired connection 1 (base eth connection)
        network_manager.delete_all_connections()

time.sleep(5)

# check internet connectivity
if not internet_connection_exists():
    p = network_manager.get_interfaces()
    web_server.load_devices(p)

    hotspot.Hotspot.start()
    time.sleep(2)
    web_server.main()
    time.sleep(2)
    hotspot.Hotspot.stop()

    # curl -X POST --header "Content-Type:application/json" --data '{"appId": '$RESIN_APP_ID'}' "$RESIN_SUPERVISOR_ADDRESS/v1/restart?apikey=$RESIN_SUPERVISOR_API_KEY"
    x = json.dumps({"appId": os.environ['RESIN_APP_ID']})
    x_url = os.environ['RESIN_SUPERVISOR_ADDRESS'] + "/v1/restart?apikey=" + os.environ['RESIN_SUPERVISOR_API_KEY']
    headers = {'content-type': 'application/json', 'Accept': 'application/json', 'charset': 'utf-8'}
    requests.post(x_url, data=x, headers=headers, verify=False)
