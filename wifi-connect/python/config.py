import os

class HOTSPOT:
    _ssid = "Synaps-Demo"
    _pass = "password"
    _gateway_ip = "192.168.42.1"
    _dhcp_range = "192.168.42.2,192.168.42.10"

    @classmethod
    def SSID(cls):
        if os.environ.get('HOTSPOT_SSID') is not None:
            return os.environ.get('HOTSPOT_SSID')
        return cls._ssid

    @classmethod
    def PASSKEY(cls):
        if os.environ.get('HOTSPOT_PASSKEY') is not None:
            return os.environ.get('HOTSPOT_PASSKEY')
        return cls._pass

    @classmethod
    def GATEWAY_IP(cls):
        if os.environ.get('HOTSPOT_GATEWAY_IP') is not None:
            return os.environ.get('HOTSPOT_GATEWAY_IP')
        return cls._gateway_ip

    @classmethod
    def DHCP_RANGE(cls):
        if os.environ.get('HOTSPOT_DHCP_RANGE') is not None:
            return os.environ.get('HOTSPOT_DHCP_RANGE')
        return cls._dhcp_range

class ENVIRONMENT:
    _clear = False
    _connections_path = "/data/network_connect.connections"

    @classmethod
    def CLEAR_CONNECTIONS(cls):
        if os.environ.get('CLEAR_CONNECTIONS') is not None:
            return os.environ.get('CLEAR_CONNECTIONS') == "true"
        return cls._clear

    @classmethod
    def CONNECTIONS_PATH(cls):
        if os.environ.get('CUSTOM_CONNECTIONS_PATH') is not None:
            return os.environ.get('CUSTOM_CONNECTIONS_PATH')
        return cls._connections_path
