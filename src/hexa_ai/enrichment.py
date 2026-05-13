import json
import os

def enrich_findings(vulnerabilities):
    print("[Enrichment] Mapping findings to CWE database...")
    # Load cwe_map.json from same directory as this file
    cwe_map_path = os.path.join(os.path.dirname(__file__), 'cwe_map.json')
    try:
        with open(cwe_map_path, 'r') as f:
            cwe_data = json.load(f)
    except FileNotFoundError:
        cwe_data = {}

    for bug in vulnerabilities:
        bug_type = bug.get("type")
        if bug_type in cwe_data:
            bug["cwe_id"] = cwe_data[bug_type].get("id")
            bug["description"] = cwe_data[bug_type].get("desc")
    
    return vulnerabilities
