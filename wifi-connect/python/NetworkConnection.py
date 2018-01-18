import dbus
import struct
import socket
import uuid

SECONDARY_NIC_ROUTE_METRIC = 2000

class IpUtilities:
    @classmethod
    def ip_to_int(cls, ip_string):
        return struct.unpack("=I", socket.inet_aton(ip_string))[0]

    @classmethod
    def int_to_ip(cls, ip_int):
        return socket.inet_ntoa(struct.pack("=I", ip_int))

    @classmethod
    def netmask_to_cidr(cls, netmask):
        sections = netmask.split(".")
        totals = []

        for section in sections:
            xsect = int(section)
            bitz = []
            for x in [1, 2, 4, 8, 16, 32, 64, 128]:
                bitz.append(1 if (xsect & x) == x else 0)
            totals.append(sum(bitz))
        return sum(totals)


class Connection:
    __type = None
    __name = None
    __primary = None
    __interface = None

    def __init__(self, type, name, primary, interface):
        self.__type = type
        self.__name = name
        self.__primary = primary == "true"
        self.__interface = interface

    def Type(self, val=None):
        if val is not None:
            self.__type = val
        return self.__type

    def Name(self, val=None):
        if val is not None:
            self.__name = val
        return self.__name

    def Primary(self, val=None):
        if val is not None:
            self.__primary = val
        return self.__primary

    def Interface(self, val=None):
        if val is not None:
            self.__interface = val
        return self.__interface


class AutoEthernet(Connection):
    __ip = None
    __cidr = None
    __gateway = None
    __uuid = None

    def __init__(self, vals):
        Connection.__init__(self, vals[0], vals[1], vals[2], vals[3])
        self.__uuid = uuid.uuid4()

    def GET_ConnectionObject(self):
        s_wired = dbus.Dictionary({'duplex': 'full'})
        s_con = dbus.Dictionary({
            'type': '802-3-ethernet',
            'uuid': str(self.__uuid),
            'interface-name': self.Interface(),
            'id': self.Name()})

        s_ip4 = None

        if self.Primary():
            s_ip4 = dbus.Dictionary({
                'method': 'auto'
            })
        else:
            s_ip4 = dbus.Dictionary({
                'method': 'auto',
                'never-default': True,
                'route-metric': SECONDARY_NIC_ROUTE_METRIC
            })

        s_ip6 = dbus.Dictionary({'method': 'ignore'})

        con = dbus.Dictionary({
            '802-3-ethernet': s_wired,
            'connection': s_con,
            'ipv4': s_ip4,
            'ipv6': s_ip6})

        return con

    def GET_PRINTABLE_ConnectionObject(self):
        return_string = ""

        return_string += "---Interface:  " + str(self.Interface()) + "---\n"
        return_string += "802-3-ethernet\n"
        return_string += "    duplex: full\n"
        return_string += "connection\n"
        return_string += "    type: 802-3-ethernet\n"
        return_string += "    uuid: " + str(self.__uuid) + "\n"
        return_string += "    interface-name: " + str(self.Interface()) + "\n"
        return_string += "    id: " + str(self.Name()) + "\n"
        return_string += "ipv4\n"
        return_string += "    method: auto\n"

        if not self.Primary():
            return_string += "    never-default: true\n"
            return_string += "    route-metric: " + str(SECONDARY_NIC_ROUTE_METRIC) + "\n"

        return_string += "ipv6\n"
        return_string += "    method: ignore\n"

        return return_string

class StaticEthernet(Connection):
    __ip = None
    __cidr = None
    __gateway = None
    __uuid = None

    def __init__(self, vals):
        Connection.__init__(self, vals[0], vals[1], vals[2], vals[3])
        self.__ip = vals[4]
        self.__cidr = IpUtilities.netmask_to_cidr(vals[5])
        self.__gateway = vals[6]
        self.__uuid = uuid.uuid4()

    def GET_ConnectionObject(self):
        s_wired = dbus.Dictionary({'duplex': 'full'})
        s_con = dbus.Dictionary({
            'type': '802-3-ethernet',
            'uuid': str(self.__uuid),
            'interface-name': self.Interface(),
            'id': self.Name()})

        addr1 = dbus.Array([IpUtilities.ip_to_int(self.__ip), dbus.UInt32(self.__cidr), IpUtilities.ip_to_int(self.__gateway)], signature=dbus.Signature('u'))
        s_ip4 = None

        if self.Primary():
            s_ip4 = dbus.Dictionary({
                'addresses': dbus.Array([addr1], signature=dbus.Signature('au')),
                'method': 'manual'
            })
        else:
            s_ip4 = dbus.Dictionary({
                'addresses': dbus.Array([addr1], signature=dbus.Signature('au')),
                'method': 'manual',
                'never-default': True,
                'route-metric': SECONDARY_NIC_ROUTE_METRIC
            })

        s_ip6 = dbus.Dictionary({'method': 'ignore'})

        con = dbus.Dictionary({
            '802-3-ethernet': s_wired,
            'connection': s_con,
            'ipv4': s_ip4,
            'ipv6': s_ip6})

        return con

    def GET_PRINTABLE_ConnectionObject(self):
        return_string = ""

        return_string += "---Interface:  " + str(self.Interface()) + "---\n"
        return_string += "802-3-ethernet\n"
        return_string += "    duplex: full\n"
        return_string += "connection\n"
        return_string += "    type: 802-3-ethernet\n"
        return_string += "    uuid: " + str(self.__uuid) + "\n"
        return_string += "    interface-name: " + str(self.Interface()) + "\n"
        return_string += "    id: " + str(self.Name()) + "\n"
        return_string += "ipv4\n"
        return_string += "    addresses: [" + str(self.__ip) + ", " + str(self.__cidr) + ", " + str(self.__gateway) + "]\n"
        return_string += "    method: manual\n"

        if not self.Primary():
            return_string += "    never-default: true\n"
            return_string += "    route-metric: " + str(SECONDARY_NIC_ROUTE_METRIC) + "\n"

        return_string += "ipv6\n"
        return_string += "    method: ignore\n"

        return return_string


class AutoWifi(Connection):
    __ssid = None
    __passkey = None
    __uuid = None

    def __init__(self, vals):
        Connection.__init__(self, vals[0], vals[1], vals[2], vals[3])
        self.__ssid = vals[4]
        self.__passkey = vals[5]
        self.__uuid = uuid.uuid4()

    def GET_ConnectionObject(self):
        s_con = dbus.Dictionary({
            'type': '802-11-wireless',
            'uuid': str(self.__uuid),
            'interface-name': str(self.Interface()),
            'id': str(self.Name())})

        s_wifi = dbus.Dictionary({
            'ssid': dbus.ByteArray(self.__ssid),
            'mode': 'infrastructure',
        })

        s_wsec = dbus.Dictionary({
            'auth-alg': 'open',
            'key-mgmt': 'wpa-psk',
            'psk': self.__passkey
        })

        s_ip4 = dbus.Dictionary({'method': 'auto'})
        s_ip6 = dbus.Dictionary({'method': 'ignore'})

        con = dbus.Dictionary({
            'connection': s_con,
            '802-11-wireless': s_wifi,
            '802-11-wireless-security': s_wsec,
            'ipv4': s_ip4,
            'ipv6': s_ip6
        })

        return con

    def GET_PRINTABLE_ConnectionObject(self):
        return_string = ""

        return_string += "---Interface:  " + str(self.Interface()) + "---\n"
        return_string += "802-11-wireless\n"
        return_string += "    ssid: " + str(self.__ssid) + "\n"
        return_string += "    mode: infrastructure\n"
        return_string += "802-11-wireless-security\n"
        return_string += "    key-mgmt: wpa-psk\n"
        return_string += "    auth-alg: open\n"
        return_string += "    psk: " + str(self.__passkey) + "\n"
        return_string += "connection\n"
        return_string += "    type: 802-11-wireless\n"
        return_string += "    uuid: " + str(self.__uuid) + "\n"
        return_string += "    interface-name: " + str(self.Interface()) + "\n"
        return_string += "    id: " + str(self.Name()) + "\n"
        return_string += "ipv4\n"
        return_string += "    method: auto\n"
        return_string += "ipv6\n"
        return_string += "    method: ignore\n"

        return return_string


class StaticWifi(Connection):
    __ssid = None
    __passkey = None

    __ip = None
    __cidr = None
    __gateway = None
    __uuid = None

    def __init__(self, vals):
        Connection.__init__(self, vals[0], vals[1], vals[2], vals[3])
        self.__ssid = vals[4]
        self.__passkey = vals[5]
        self.__ip = vals[6]
        self.__cidr = IpUtilities.netmask_to_cidr(vals[7])
        self.__gateway = vals[8]
        self.__uuid = uuid.uuid4()

    def GET_ConnectionObject(self):
        s_con = dbus.Dictionary({
            'type': '802-11-wireless',
            'uuid': str(self.__uuid),
            'interface-name': self.Interface(),
            'id': self.Name()})

        s_wifi = dbus.Dictionary({
            'ssid': dbus.ByteArray(self.__ssid.encode("utf-8")),
            'mode': 'infrastructure',
        })

        s_wsec = dbus.Dictionary({
            'key-mgmt': 'wpa-psk',
            'auth-alg': 'open',
            'psk': self.__passkey,
            'psk-flags': 0
        })

        addr1 = dbus.Array([IpUtilities.ip_to_int(self.__ip), dbus.UInt32(self.__cidr), IpUtilities.ip_to_int(self.__gateway)], signature=dbus.Signature('u'))
        s_ip4 = dbus.Dictionary({
            'addresses': dbus.Array([addr1], signature=dbus.Signature('au')),
            'method': 'manual'
        })

        s_ip6 = dbus.Dictionary({'method': 'ignore'})

        con = dbus.Dictionary({
            'connection': s_con,
            '802-11-wireless': s_wifi,
            '802-11-wireless-security': s_wsec,
            'ipv4': s_ip4,
            'ipv6': s_ip6
        })

        return con

    def GET_PRINTABLE_ConnectionObject(self):
        return_string = ""

        return_string += "---Interface:  " + str(self.Interface()) + "---\n"
        return_string += "802-11-wireless\n"
        return_string += "    ssid: " + str(self.__ssid) + "\n"
        return_string += "    mode: infrastructure\n"
        return_string += "802-11-wireless-security\n"
        return_string += "    key-mgmt: wpa-psk\n"
        return_string += "    auth-alg: open\n"
        return_string += "    psk: " + str(self.__passkey) + "\n"
        return_string += "connection\n"
        return_string += "    type: 802-11-wireless\n"
        return_string += "    uuid: " + str(self.__uuid) + "\n"
        return_string += "    interface-name: " + str(self.Interface()) + "\n"
        return_string += "    id: " + str(self.Name()) + "\n"
        return_string += "ipv4\n"
        return_string += "    addresses: [" + str(self.__ip) + ", " + str(self.__cidr) + ", " + str(self.__gateway) + "]\n"
        return_string += "    method: manual\n"
        return_string += "ipv6\n"
        return_string += "    method: ignore\n"

        return return_string
