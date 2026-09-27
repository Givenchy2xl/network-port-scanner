import socket
import argparse
import ipaddress
from concurrent.futures import ThreadPoolExecutor


def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((ip, port))

    sock.close()

    return port, result == 0


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_ports(start_port, end_port):
    if not 1 <= start_port <= 65535:
        return False

    if not 1 <= end_port <= 65535:
        return False

    if start_port > end_port:
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Simple concurrent TCP port scanner"
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

    if not validate_ip(args.ip):
        print(f"Erreur : adresse IP invalide : {args.ip}")
        return

    if not validate_ports(args.start_port, args.end_port):
        print(
            "Erreur : les ports doivent être compris entre 1 et 65535 "
            "et le port de début doit être inférieur ou égal au port de fin."
        )
        return

    print(f"Scan de {args.ip} : ports {args.start_port}-{args.end_port}")
    print("-" * 40)

    open_ports = []

    ports = range(args.start_port, args.end_port + 1)

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(
            lambda port: scan_port(args.ip, port),
            ports
        )

        for port, is_open in results:
            if is_open:
                open_ports.append(port)
                print(f"[+] Port {port} ouvert")

    print()

    if not open_ports:
        print("Aucun port ouvert trouvé.")
    else:
        print(
            f"{len(open_ports)} port(s) ouvert(s) trouvé(s)."
        )


if __name__ == "__main__":
    main()
