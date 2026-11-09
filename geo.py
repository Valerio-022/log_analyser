import json
import urllib.request
from logger_setup import get_logger

log = get_logger("geo")
CACHE = {}


def load_countries(ips):
    todo = [ip for ip in set(ips) if ip not in CACHE]
    for i in range(0, len(todo), 100):
        batch = todo[i:i + 100]
        try:
            req = urllib.request.Request(
                "http://ip-api.com/batch?fields=query,countryCode",
                data=json.dumps(batch).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                for item in json.loads(r.read()):
                    CACHE[item["query"]] = item.get("countryCode") or "Unknown"
        except Exception as e:
            log.error(f"Country lookup failed for a batch of {len(batch)} IPs: {e}")
            for ip in batch:
                CACHE[ip] = "Unknown"


def ip_to_country(ip):
    if ip not in CACHE:
        log.warning(f"No country found for IP: {ip}")
    return CACHE.get(ip, "Unknown")