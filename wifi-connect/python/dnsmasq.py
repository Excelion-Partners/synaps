import config
import subprocess
import sys


class Dnsmasq:
    ____dnsmasq_ps = None
    ____started = False

    @classmethod
    def start(cls, iface):
        if not cls.____started:
            cls.____started = True
            dnsmasq_config_file = "/tmp/dnsmasq-" + str(iface) + ".conf"
            dcfg = "interface=" + str(iface) + "\naddress=/#/" + config.HOTSPOT.GATEWAY_IP() + "\ndhcp-range=" + config.HOTSPOT.DHCP_RANGE() + "\nbind-interfaces"

            sargs = "dnsmasq -h -k -C " + str(dnsmasq_config_file)
            aargs = sargs.split()
            sys.stdout.write(str(aargs) + "\n")

            dfile = open(dnsmasq_config_file,"w")
            dfile.write(dcfg)
            dfile.close()

            sys.stdout.write("Starting dnsmasq..\n")
            cls.____dnsmasq_ps = subprocess.Popen(aargs)

    @classmethod
    def stop(cls):
        if cls.____started:
            cls.____started = False

            sys.stdout.write("Stopping dnsmasq..\n")

            cls.____dnsmasq_ps.terminate()
            cls.____dnsmasq_ps.kill()
