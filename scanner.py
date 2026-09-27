import socket


def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((ip, port))

    sock.close()

    return result == 0

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 22

    if scan_port(ip, port):
        print(f"Port {port} ouvert")
    else:
        print(f"Port {port} fermé")


