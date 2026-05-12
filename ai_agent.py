def analyze_findings(recon_data, http_results):
    """
    Analyzes reconnaissance and HTTP data to identify potential vulnerabilities.
    """
    print("[AI Agent] Analyzing data for potential bugs...")
    vulnerabilities = []

    # Check for sensitive files found in HTTP discovery
    sensitive_patterns = [".env", "config", "backup", "admin"]
    for url in http_results.get("endpoints", []):
        if any(pattern in url.lower() for pattern in sensitive_patterns):
            vulnerabilities.append({
                "type": "Potential Sensitive File Exposure",
                "severity": "High",
                "location": url
            })

    # Analyze open ports for risky services
    risky_ports = {21: "FTP", 22: "SSH", 23: "Telnet"}
    for port in recon_data.get("open_ports", []):
        if port in risky_ports:
            vulnerabilities.append({
                "type": "Exposed Management Service",
                "severity": "Medium",
                "location": f"Port {port} ({risky_ports[port]})"
            })

    print(f"[AI Agent] Analysis complete. Identified {len(vulnerabilities)} issues.")
    return vulnerabilities
