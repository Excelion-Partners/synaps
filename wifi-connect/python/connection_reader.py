import os.path
import os
import sys
import NetworkConnection


def get_connections(filename):
    conns = []

    if os.path.isfile(filename):
        f = open(filename, "r")

        for line in f:
            sline = line.rstrip()
            if sline[0] != '#':
                x = sline.split(",")

                if x[0] == "Wired-DHCP":
                    conn = NetworkConnection.AutoEthernet(x)
                    conns.append(conn)
                elif x[0] == "Wired-Static":
                    conn = NetworkConnection.StaticEthernet(x)
                    conns.append(conn)
                elif x[0] == "Wireless-Static":
                    conn = NetworkConnection.StaticWifi(x)
                    conns.append(conn)
                elif x[0] == "Wireless-DHCP":
                    conn = NetworkConnection.AutoWifi(x)
                    conns.append(conn)
                else:
                    sys.stdout.write("Unrecognized connection: " + str(x) + "\n")

        if len(conns) > 0:
            return conns

    return None

def delete_all_connections(filename):
    open(filename, 'w').close()
