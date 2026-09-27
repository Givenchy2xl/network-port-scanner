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
        "start_port",
        type=int,
        help="Premier port à scanner"
    )

    parser.add_argument(
        "end_port",
        type=int,
        help="Dernier port à scanner"
    )

    args = parser.parse_args()

    print(f"Scan de {args.ip} : ports {args.start_port}-{args.end_port}")
    print("-" * 40)

    open_ports = 0

    for port in range(args.start_port, args.end_port + 1):
        if scan_port(args.ip, port):
            print(f"[+] Port {port} ouvert")
            open_ports += 1

    print()

    if open_ports == 0:
        print("Aucun port ouvert trouvé.")
    else:
        print(f"{open_ports} port(s) ouvert(s) trouvé(s).")


if __name__ == "__main__":
    main()
