from logger_setup import get_logger

log = get_logger("geo")

PREFIXES = {
    "45.33.": "United States",
    "103.21.": "India",
    "185.220.": "Germany",
    "91.134.": "France",
    "192.168.": "Local network",
}


def ip_to_country(ip):
    try:
        for prefix, country in PREFIXES.items():
            if ip.startswith(prefix):
                return country
        log.warning(f"No country found for IP: {ip}")
        return "Unknown"
    except AttributeError:
        log.error(f"Invalid IP value: {ip!r}")
        return "Unknown"
    except Exception as e:
        log.error(f"Unexpected error in ip_to_country: {e}")
        return "Unknown"