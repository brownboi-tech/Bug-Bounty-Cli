import os
import json
from recon import perform_recon
from http_capture import capture_traffic
from ai_agent import analyze_findings
from enrichment import enrich_findings
from reporting import generate_report

def run_scan(target: str, fast_mode: bool, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    recon_data = perform_recon(target, fast_mode)
    http_results = capture_traffic(target)
    raw_bugs = analyze_findings(recon_data, http_results)
    vulnerabilities = enrich_findings(raw_bugs)

    report_data = {
        "target": target,
        "recon": recon_data,
        "web": http_results,
        "vulnerabilities": vulnerabilities
    }

    # Sanitize target name for filename
    safe_target = target.replace('/', '_').replace(':', '_')
    report_path = os.path.join(output_dir, f"{safe_target}_report.json")
    
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=4)

    generate_report(report_path)
