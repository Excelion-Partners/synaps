from systemd_dbus.manager import Manager
import sys
import time


def start(xunit):
    manager = Manager()
    unit = manager.get_unit(xunit)
    unit.start('fail')

    sys.stdout.write("Network Manager started...\n")

    time.sleep(5)

def stop(xunit):
    manager = Manager()
    unit = manager.get_unit(xunit)
    unit.stop('fail')

    sys.stdout.write("Network Manager stopped...\n")

    time.sleep(5)
