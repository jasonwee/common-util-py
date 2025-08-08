import socket

def is_valid(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except:
        return False
