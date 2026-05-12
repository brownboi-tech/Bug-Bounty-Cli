import socket

def perform_recon(target, fast_mode=False):
    """
    Performs basic reconnaissance on a given target.
    """
    print(f"[Recon] Starting reconnaissance for {target}...")
    
    results = {
        "target": target,
        "ip_address": None,
        "subdomains": [],
        "open_ports": []
    }

    try:
        results["ip_address"] = socket.gethostbyname(target)
        print(f"[Recon] Resolved {target} to {results['ip_address']}")
    except socket.gaierror:
        print(f"[Recon] Could not resolve {target}")
        return results

    # Simulated Subdomain Enumeration
    # In a real tool, you might use a wordlist or an API
    common_subs = ["www", "dev", "api", "test", "staging"]
    if fast_mode:
        common_subs = ["www"]
    
    print(f"[Recon] Checking common subdomains...")
    for sub in common_subs:
        full_url = f"{sub}.{target}"
        try:
            socket.gethostbyname(full_url)
            results["subdomains"].append(full_url)
        except socket.gaierror:
            continue

    # Basic Port Scan (Top common ports)
    ports_to_check = [80, 443, 8080, 21, 22]
    if fast_mode:
        ports_to_check = [80, 443]

    print(f"[Recon] Scanning common ports...")
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((results["ip_address"], port))
        if result == 0:
            results["open_ports"].append(port)
        sock.close()

    print(f"[Recon] Reconnaissance finished.")
    return results
