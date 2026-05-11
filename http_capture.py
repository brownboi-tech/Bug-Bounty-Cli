import requests

def capture_traffic(target):
    """
    Simulates HTTP discovery by checking common web paths.
    """
    print(f"[HTTP Capture] Analyzing web surface for {target}...")
    results = {"endpoints": [], "status_codes": {}}
    
    paths = ["/", "/login", "/admin", "/api/v1", "/robots.txt", "/.env"]
    protocol = "https://" if not target.startswith("http") else ""
    
    for path in paths:
        url = f"{protocol}{target}{path}"
        try:
            response = requests.get(url, timeout=3, allow_redirects=True)
            if response.status_code == 200:
                results["endpoints"].append(url)
            results["status_codes"][url] = response.status_code
        except requests.exceptions.RequestException:
            continue
            
    print(f"[HTTP Capture] Discovery finished. Found {len(results['endpoints'])} active endpoints.")
    return results
