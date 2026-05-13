def generate_report(results_path):
    import json
    with open(results_path, 'r') as f:
        data = json.load(f)
    
    print("\n" + "="*40)
    print(f" BUG HUNT REPORT: {data['target']}")
    print("="*40)
    print(f"IP Address: {data['recon']['ip_address']}")
    print(f"Open Ports: {data['recon']['open_ports']}")
    print(f"Endpoints Found: {len(data['web']['endpoints'])}")
    print("-"*40)
    
    if not data['vulnerabilities']:
        print("No vulnerabilities identified in this pass.")
    else:
        for bug in data['vulnerabilities']:
            print(f"[{bug['severity']}] {bug['type']} at {bug['location']}")
    print("="*40 + "\n")
