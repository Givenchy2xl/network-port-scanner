import socket
import argparse


def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((ip, port))

    sock.close()

    return result == 0


def main():
    parser = argparse.ArgumentParser(
        description="Simple TCP port scanner"
    )

    parser.add_argument(
        "ip",
        help="Adresse IP de la cible"
    )

    parser.add_argument(
        "port",
        type=int,
        help="Port TCP à tester"
    )

    args = parser.parse_args()

    if scan_port(args.ip, args.port):
        print(f"Port {args.port} ouvert sur {args.ip}")
    else:
        print(f"Port {args.port} fermé sur {args.ip}")


if __name__ == "__main__":
    main()
