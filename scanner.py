import socket
import ssl
import ipaddress
from urllib.parse import urlparse
import requests


def validate_url(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return None

        if not parsed.hostname or parsed.username or parsed.password:
            return None

        # Resolve DNS and reject non-public addresses.
        addresses = socket.getaddrinfo(
            parsed.hostname, None, type=socket.SOCK_STREAM
        )

        ips = list(set(item[4][0] for item in addresses))

        if not ips:
            return None

        for ip in ips:
            address = ipaddress.ip_address(ip)
            if not address.is_global:
                return None

        return parsed

    except (ValueError, OSError):
        return None


def get_website_info(url):
    parsed = validate_url(url)

    if not parsed:
        return {"error": "Invalid URL or non-public destination"}

    domain = parsed.hostname

    result = {
        "domain": domain,
        "ip_addresses": [],
        "https": False,
        "status": "Unknown"
    }

    try:
        result["ip_addresses"] = list(set(
            item[4][0] for item in socket.getaddrinfo(
                domain, None, type=socket.SOCK_STREAM
            )
        ))

        if parsed.scheme == "https":
            context = ssl.create_default_context()

            with socket.create_connection(
                (domain, 443), timeout=5
            ) as connection:
                with context.wrap_socket(
                    connection, server_hostname=domain
                ):
                    result["https"] = True

        response = requests.get(
            url,
            timeout=8,
            allow_redirects=False,
            stream=True
        )

        result["status"] = response.status_code
        response.close()

    except requests.RequestException:
        result["status"] = "Connection failed"
    except (OSError, ssl.SSLError):
        result["https"] = False

    return result
