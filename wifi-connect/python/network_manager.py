import socket
import struct
import dbus
import sys
import time
import systemd

DEVICE_TYPE_ETHERNET = 1
DEVICE_TYPE_WIRELESS = 2

def start():
	systemd.start("NetworkManager.service")

def stop():
    systemd.stop("NetworkManager.service")

def ready():
	systemd.wait_until_state("NetworkManager.service", "active")

def add_connection(conn):
    # disconnect device
    if conn.Type() == "Wired-Static":
        disconnect_device(str(conn.Interface()))
        time.sleep(2)

    bus = dbus.SystemBus()
    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

    sys.stdout.write("Adding Connection " + str(conn.Name()) + "...\n")

    conn_path = settings.AddConnection(conn.GET_ConnectionObject())

    sys.stdout.write("Connection Successfully Added! \n")

    time.sleep(2)

    sys.stdout.write("Fetching Device " + str(conn.Interface()) + "... \n")

    dev_path = get_device_path(conn.Interface())

    sys.stdout.write("Device " + str(conn.Interface()) + " found! \n")

    sys.stdout.write("Activating Connection... \n")

    activate_connection(conn_path, dev_path)

    sys.stdout.write("Connection Successfully Activated! \n")

def activate_connection(c_path, d_path):
    bus = dbus.SystemBus()
    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
    manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
    time.sleep(2)
    manager.ActivateConnection(c_path, d_path, "/")

def get_device_path(iface_name):
    bus = dbus.SystemBus()

    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
    manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")

    devices = manager.GetDevices()
    for d in devices:
        dev_proxy = bus.get_object("org.freedesktop.NetworkManager", d)
        prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
        iface = prop_iface.Get("org.freedesktop.NetworkManager.Device", "Interface")
        if iface == iface_name:
            return d

def get_wifi_interface_name():
    bus = dbus.SystemBus()

    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
    manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")

    devices = manager.GetDevices()
    for d in devices:
        dev_proxy = bus.get_object("org.freedesktop.NetworkManager", d)
        prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
        iface = prop_iface.Get("org.freedesktop.NetworkManager.Device", "Interface")
        dtype = prop_iface.Get("org.freedesktop.NetworkManager.Device", "DeviceType")
        if dtype == DEVICE_TYPE_WIRELESS:
            return iface
    return None

def disconnect_device(iface_name):
    bus = dbus.SystemBus()

    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
    manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")

    dpath = None

    devices = manager.GetDevices()
    for d in devices:
        dev_proxy = bus.get_object("org.freedesktop.NetworkManager", d)
        prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
        iface = prop_iface.Get("org.freedesktop.NetworkManager.Device", "Interface")
        if iface == iface_name:
            dpath = d
            break

    dev_proxy = bus.get_object("org.freedesktop.NetworkManager", dpath)
    dev_iface = dbus.Interface(dev_proxy, "org.freedesktop.NetworkManager.Device")
    prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")

    # Make sure the device is connected before we try to disconnect it
    state = prop_iface.Get("org.freedesktop.NetworkManager.Device", "State")

    sys.stdout.write("Device " + str(iface_name) + " state = " + str(state) + "\n")

    if state == 30 or state == 20:
        sys.stdout.write("Device " + str(iface_name) + " isn't connected. \n")
    else:
        # Tell NM to disconnect it
        dev_iface.Disconnect()
        sys.stdout.write("Device " + str(iface_name) + " has been disconnected. \n")

def delete_connection(con):
    bus = dbus.SystemBus()
    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

    con_path = None

    for c_path in settings.ListConnections():
        c_proxy = bus.get_object("org.freedesktop.NetworkManager", c_path)
        c_obj = dbus.Interface(c_proxy, "org.freedesktop.NetworkManager.Settings.Connection")
        c_settings = c_obj.GetSettings()

        if c_settings['connection']['id'] == con:
            c_obj.Delete(c_path)

def delete_all_connections():
    bus = dbus.SystemBus()
    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings")
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

    con_path = None

    for c_path in settings.ListConnections():
        c_proxy = bus.get_object("org.freedesktop.NetworkManager", c_path)
        c_obj = dbus.Interface(c_proxy, "org.freedesktop.NetworkManager.Settings.Connection")
        c_settings = c_obj.GetSettings()

        if c_settings['connection']['id'] != "Wired connection 1":
            c_obj.Delete(c_path)

def get_interfaces():
    bus = dbus.SystemBus()

    proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
    manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")

    devices_ret = []

    devices = manager.GetDevices()
    for d in devices:
        dev_proxy = bus.get_object("org.freedesktop.NetworkManager", d)
        prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
        iface_name = prop_iface.Get("org.freedesktop.NetworkManager.Device", "Interface")
        iface_type_id = prop_iface.Get("org.freedesktop.NetworkManager.Device", "DeviceType")

        if iface_type_id == 1:
            devices_ret.append({"InterfaceName": str(iface_name), "InterfaceTypeId": str(iface_type_id)})
        elif iface_type_id == 2:
            devices_ret.append({"InterfaceName": str(iface_name), "InterfaceTypeId": str(iface_type_id)})

    return devices_ret
