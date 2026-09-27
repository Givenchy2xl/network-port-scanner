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
    """Retourne le nom du service associé au port."""
    return COMMON_SERVICES.get(port, "Service inconnu")


def scan_port(ip, port, timeout):
    """Teste si un port TCP est ouvert."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))

        return port, result == 0

    except socket.error:
        return port, False


def validate_ip(ip):
    """Vérifie si l'adresse IP est valide."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_ports(start_port, end_port):
    """Vérifie si la plage de ports est valide."""
    if not 1 <= start_port <= 65535:
        return False

    if not 1 <= end_port <= 65535:
        return False

    if start_port > end_port:
        return False

    return True


def validate_timeout(timeout):
    """Vérifie que le timeout est valide."""
    return timeout > 0


def validate_workers(workers):
    """Vérifie que le nombre de workers est valide."""
    return workers > 0


def scan_ports(ip, start_port, end_port, timeout, workers):
    """Scanne une plage de ports et retourne les ports ouverts."""
    open_ports = []

    ports = range(start_port, end_port + 1)

    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = executor.map(
                lambda port: scan_port(ip, port, timeout),
                ports
            )

            for port, is_open in results:
                if is_open:
                    service = get_service_name(port)
                    open_ports.append((port, service))

    except (OSError, ValueError):
        return []

    return open_ports


def save_report(
    filename,
    ip,
    start_port,
    end_port,
    timeout,
    workers,
    open_ports
):
    """Enregistre les résultats du scan dans un fichier."""
    try:
        with open(filename, "w", encoding="utf-8") as report:
            report.write("Network Port Scanner\n")
            report.write("=" * 50 + "\n")
            report.write(f"Cible : {ip}\n")
            report.write(f"Ports : {start_port}-{end_port}\n")
            report.write(f"Timeout : {timeout} seconde(s)\n")
            report.write(f"Workers : {workers}\n")
            report.write("\n")

            if not open_ports:
                report.write("Aucun port ouvert trouvé.\n")
            else:
                report.write("Ports ouverts :\n")

                for port, service in open_ports:
                    report.write(
                        f"- Port {port} — {service} — OPEN\n"
                    )

            report.write("\n")
            report.write(
                f"Total : {len(open_ports)} port(s) ouvert(s)\n"
            )

        return True

    except OSError:
        return False


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

    parser.add_argument(
        "--output",
        help="Fichier texte dans lequel enregistrer les résultats"
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

    if not validate_timeout(args.timeout):
        print("Erreur : le timeout doit être supérieur à 0.")
        return

    if not validate_workers(args.workers):
        print("Erreur : le nombre de workers doit être supérieur à 0.")
        return

    print(f"Scan de {args.ip} : ports {args.start_port}-{args.end_port}")
    print(f"Timeout : {args.timeout} seconde(s)")
    print(f"Workers : {args.workers}")
    print("-" * 50)

    open_ports = scan_ports(
        args.ip,
        args.start_port,
        args.end_port,
        args.timeout,
        args.workers
    )

    for port, service in open_ports:
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

    if args.output:
        if save_report(
            args.output,
            args.ip,
            args.start_port,
            args.end_port,
            args.timeout,
            args.workers,
            open_ports
        ):
            print(
                f"Rapport enregistré dans : {args.output}"
            )
        else:
            print(
                f"Erreur lors de l'enregistrement du rapport : "
                f"{args.output}"
            )


if __name__ == "__main__":
    main()
