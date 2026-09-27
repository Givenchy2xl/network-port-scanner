import socket
import argparse
import ipaddress
from concurrent.futures import ThreadPoolExecutor


COMMON_SERVICES = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    88: "Kerberos",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Proxy",
}


def get_service_name(port):
    return COMMON_SERVICES.get(port, "Service inconnu")


def scan_port(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

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

    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Délai d'attente en secondes (défaut : 1.0)"
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=50,
        help="Nombre de connexions simultanées (défaut : 50)"
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

    if args.timeout <= 0:
        print("Erreur : le timeout doit être supérieur à 0.")
        return

    if args.workers <= 0:
        print("Erreur : le nombre de workers doit être supérieur à 0.")
        return

    print(f"Scan de {args.ip} : ports {args.start_port}-{args.end_port}")
    print(f"Timeout : {args.timeout} seconde(s)")
    print(f"Workers : {args.workers}")
    print("-" * 50)

    open_ports = []

    ports = range(args.start_port, args.end_port + 1)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = executor.map(
            lambda port: scan_port(args.ip, port, args.timeout),
            ports
        )

        for port, is_open in results:
            if is_open:
                service = get_service_name(port)
                open_ports.append(port)

                print(
                    f"[+] Port {port} ouvert — {service}"
                )

    print("-" * 50)

    if not open_ports:
        print("Aucun port ouvert trouvé.")
    else:
        print(
            f"{len(open_ports)} port(s) ouvert(s) trouvé(s)."
        )


if __name__ == "__main__":
    main()
