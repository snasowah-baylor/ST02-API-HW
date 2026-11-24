import requests

test_ips = [
    "51.83.59.99",     # Shodan sample (ports, CPEs, tags, vulns)
    "1.1.1.1",         # Cloudflare DNS (hostnames, ports)
    "151.101.41.140",  # CDN node (tags, CPEs)
    "192.0.2.1",       # Reserved TEST-NET (triggers 404 handling)
]

for ip in test_ips:
    resp = requests.get(f"https://internetdb.shodan.io/{ip}", timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        print(f"[200] {ip} -> Ports: {data.get('ports')} | Tags: {data.get('tags')} | Vulns: {data.get('vulns')}")
    else:
        print(f"[{resp.status_code}] {ip} -> {resp.json().get('detail')}")