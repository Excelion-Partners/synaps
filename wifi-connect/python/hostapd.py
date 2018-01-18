import config
import subprocess
import sys


class Hostapd:
    ____hostapd_ps = None
    ____started = False

    @classmethod
    def start(cls, iface):
        # hostapd
        if not cls.____started:
            cls.____started = True

            hostapd_config_file = "/tmp/hostapd-" + str(iface) + ".conf"
            hcfg = "ssid=" + config.HOTSPOT.SSID() + "\ninterface=" + str(iface) + "\nchannel=6\ndriver=nl80211\nwpa=2\nwpa_passphrase=" + config.HOTSPOT.PASSKEY()

            hfile = open(hostapd_config_file,"w")
            hfile.write(hcfg)
            hfile.close()

            sargs = "hostapd " + str(hostapd_config_file)
            aargs = sargs.split()

            sys.stdout.write("Starting hostapd..\n")
            cls.____hostapd_ps = subprocess.Popen(aargs)

    @classmethod
    def stop(cls):
        if cls.____started:
            cls.____started = False

            sys.stdout.write("Stopping hostapd..\n")
            cls.____hostapd_ps.terminate()
            cls.____hostapd_ps.kill()
