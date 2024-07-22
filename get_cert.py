#!/usr/bin/env python

import socket
import sqlite3
import ssl
import sys
import time
from datetime import datetime

# ANSI color codes
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# cache database path
DB_PATH = "/tmp/get_cert.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS cert_cache
                   (hostname TEXT PRIMARY KEY, cert TEXT, timestamp INTEGER)""")
    conn.commit()
    conn.close()


def get_cached_cert(hostname):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT cert, timestamp FROM cert_cache WHERE hostname = ?", (hostname,)
    )
    result = cur.fetchone()
    conn.close()

    if result:
        cert, timestamp = result
        if time.time() - timestamp <= 3600:
            return eval(cert)               # convert string representation back to dict
    return None


def cache_cert(hostname, cert):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO cert_cache VALUES (?, ?, ?)",
        (hostname, str(cert), int(time.time())),
    )
    conn.commit()
    conn.close()


def get_certificate(hostname, port=443):
    """Retrieve the certificate from a server or cache"""
    cached_cert = get_cached_cert(hostname)
    if cached_cert:
        print(f"{YELLOW}{hostname} (cached){RESET}")
        return cached_cert

    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                cert = secure_sock.getpeercert()
        cache_cert(hostname, cert)
        return cert
    except socket.gaierror as e:
        print(f"Error: {e}")
        exit(1)


def convert_cert_time(cert_time):
    """Convert certificate time to a human-readable format"""
    format_string = "%b %d %H:%M:%S %Y %Z"
    result = datetime.strptime(cert_time, format_string).astimezone()
    return result


def format_stdout(cert):
    """Format the certificate information for display"""
    subject = dict(x[0] for x in cert["subject"])
    issuer = dict(x[0] for x in cert["issuer"])
    not_before = convert_cert_time(cert["notBefore"])
    not_after = convert_cert_time(cert["notAfter"])

    subject_info = f"CN={subject.get('commonName', 'N/A')}, O={subject.get('organizationName', 'N/A')}"
    issuer_info = f"CN={issuer.get('commonName', 'N/A')}, O={issuer.get('organizationName', 'N/A')}"

    max_width = max(
        len(subject_info),
        len(issuer_info),
        len(str(not_before)),
        len(str(not_after)),
        len("Subject:"),
        len("Issuer:"),
        len("Valid from:"),
        len("Valid until:"),
    )
    spacing = max_width - 10

    print(f"\n{GREEN}{'Subject:':<{spacing}}{RESET} {subject_info}")
    print(f"{GREEN}{'Issuer:':<{spacing}}{RESET} {issuer_info}")
    print(f"{GREEN}{'Valid from:':<{spacing}}{RESET} {not_before}")
    print(f"{GREEN}{'Valid until:':<{spacing}}{RESET} {not_after}")


def main():
    init_db()
    if len(sys.argv) == 2:
        cert = get_certificate(sys.argv[1])
    else:
        msg = (
            YELLOW + "Enter the FQDN of the server: [www.example.com]" + RESET + "\n\n"
        )
        fqdn = input(msg)
        cert = get_certificate(fqdn)
    format_stdout(cert)


if __name__ == "__main__":
    main()
