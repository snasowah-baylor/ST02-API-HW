"""
Shodan InternetDB is a free, unauthenticated REST API provided by Shodan for
fast, passive IPv4 reconnaissance and threat enrichment. Rather than performing
active network scans or returning raw service banners, it returns a compact
JSON summary of what Shodan's global crawlers have indexed on an IP address.

Core SpecificationsBase URL:
[https://internetdb.shodan.io](https://internetdb.shodan.io)

Endpoint:
GET /{ip} (accepts a single IPv4 address; OpenAPI docs are hosted at
[https://internetdb.shodan.io/docs](https://internetdb.shodan.io/docs))

Authentication: None required (no API key or account needed)
Update Cadence: Refreshed weekly (unlike Shodan's paid REST API, which updates
continuously in real time)   Rate Limits & Licensing: Designed for high-
throughput lookups; free for personal, academic, and internal corporate
security use, though prohibited from being resold inside commercial products.
Response Schema & Fields A 200 OK response returns a flat JSON object
containing six fields—five of which are arrays.
"""

import requests

test_ips = [
    "51.83.59.99",  # Shodan sample (ports, CPEs, tags, vulns)
    "1.1.1.1",  # Cloudflare DNS (hostnames, ports)
    "151.101.41.140",  # CDN node (tags, CPEs)
    "192.0.2.1",  # Reserved TEST-NET (triggers 404 handling)
]

for ip in test_ips:
    resp = requests.get(f"https://internetdb.shodan.io/{ip}", timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        print(
            f"[200] {ip} -> Ports: {data.get('ports')} | Tags: {data.get('tags')} | Vulns: {data.get('vulns')}"
        )
    else:
        print(f"[{resp.status_code}] {ip} -> {resp.json().get('detail')}")
