import network_manager
import connection_reader
import config
import hostapd
import dnsmasq
import sys
import time
import subprocess


class Hotspot:
    __started = False

    @classmethod
    def start(cls):
        if not cls.__started:
            cls.__started = True

            sys.stdout.write("Starting hotspot\n")

            # remove all connections
            # network_manager.delete_all_connections()

            # get wifi interface
            iface = network_manager.get_wifi_interface_name()

            # stop network manager
            network_manager.stop()

            # rfkill unblock wifi
            rfkill_unblock_wifi = "rfkill unblock wifi"
            rfkill_response = subprocess.call(rfkill_unblock_wifi.split())
            sys.stdout.write("rfkill response: " + str(rfkill_response) + "\n")

            # add ip
            add_ip_command = "ip addr add " + config.HOTSPOT.GATEWAY_IP() + "/24 dev " + str(iface)
            add_ip_response = subprocess.call(add_ip_command.split())
            sys.stdout.write("add ip response: " + str(add_ip_response) + "\n")

            # start hostapd
            hostapd.Hostapd.start(iface)

            # start dnsmasq
            dnsmasq.Dnsmasq.start(iface)

            sys.stdout.write("Started hotspot\n")

    @classmethod
    def stop(cls):
        if cls.__started:
            cls.__started = False

            # stop hostapd
            hostapd.Hostapd.stop()

            # stop dnsmasq
            dnsmasq.Dnsmasq.stop()

            # start network manager
            network_manager.start()
