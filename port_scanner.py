import socket
import re
import common_ports

def get_open_ports(target, port_range, verbose = False):
    open_ports = []
    ip = ''
    try:
        ip = socket.gethostbyname(target)
        for port in range(port_range[0], port_range[1] +1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            s.close()
    except KeyboardInterrupt:
        return "Don't press anything!"
    except socket.gaierror:
        if re.search("[a-zA-Z]", target):
            return "Error: Invalid hostname"
        else: 
            return "Error: Invalid IP address"
    except socket.error:
        return "Connection error!"

    hostname = None
    try: 
        hostname = socket.gethostbyaddr(ip)[0]
    except: 
        hostname = None
    text = "Open ports for "
    if hostname != None:
        text += "{hostname} ({ip})\nPORT     SERVICE".format(hostname=hostname, ip =ip)
    else:
        text += "{ip}\nPORT     SERVICE".format(ip =ip)
    if verbose:
        for port in open_ports:
            text += "\n{port}".format(port=port) + " "*(9-len(str(port))) + "{service}".format(service = common_ports.ports_and_services[port])
        return text
    return(open_ports)

