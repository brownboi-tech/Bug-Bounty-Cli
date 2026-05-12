import json

def enrich_findings(vulnerabilities):
    print("[Enrichment] Mapping findings to CWE database...")
    try:
        with open('/content/cwe_map.json', 'r') as f:
            cwe_data = json.load(f)
    except FileNotFoundError:
        cwe_data = {}

    for bug in vulnerabilities:
        bug_type = bug.get("type")
        if bug_type in cwe_data:
            bug["cwe_id"] = cwe_data[bug_type].get("id")
            bug["description"] = cwe_data[bug_type].get("desc")
    
    return vulnerabilities
