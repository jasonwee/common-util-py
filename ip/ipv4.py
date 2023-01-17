import socket

def is_valid(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False
