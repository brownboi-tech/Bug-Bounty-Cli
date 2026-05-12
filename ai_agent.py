import subprocess
import os
import shutil
import google.generativeai as genai

class ToolManager:
    def __init__(self):
        self.tool_registry = {
            "nmap": "apt-get install -y nmap",
            "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "nuclei": "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
            "whatweb": "apt-get install -y whatweb",
            "ffuf": "apt-get install -y ffuf",
            "dirsearch": "pip install dirsearch",
            "sqlmap": "apt-get install -y sqlmap",
            "nikto": "apt-get install -y nikto",
            "amass": "apt-get install -y amass"
        }

    def ensure_tool(self, tool_name):
        if shutil.which(tool_name):
            return True
        print(f"[AI Agent] Installing missing tool: {tool_name}...")
        install_cmd = self.tool_registry.get(tool_name)
        if not install_cmd: return False
        try:
            subprocess.run(install_cmd, shell=True, check=True, capture_output=True)
            return True
        except:
            return False

    def run_tool(self, tool_name, args):
        if self.ensure_tool(tool_name):
            full_cmd = [tool_name] + args
            result = subprocess.run(full_cmd, capture_output=True, text=True)
            return result.stdout
        return ""

def analyze_with_llm(data_context):
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        # Explicitly configure stable v1 API version
        genai.configure(api_key=api_key, transport='rest', client_options={'api_version': 'v1'})
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analyze this security data for high-impact logic vulnerabilities or misconfigurations. Return a detailed assessment:\n{data_context}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LLM Analysis skipped (Error: {str(e)})"

def analyze_findings(recon_data, http_results):
    print("[AI Agent] Initiating autonomous analysis phase...")
    tm = ToolManager()
    vulnerabilities = []

    if recon_data.get("open_ports"):
        ports = ",".join(map(str, recon_data["open_ports"]))
        tm.run_tool("nmap", ["-sV", "-p", ports, recon_data["ip_address"]])

    if http_results.get("endpoints"):
        print("[AI Agent] Launching LLM Deep Logic Analysis...")
        llm_report = analyze_with_llm(str(http_results))
        vulnerabilities.append({"type": "LLM Insight", "severity": "Variable", "location": "Logic Analysis", "details": llm_report})

    return vulnerabilitiesdef analyze_findings(recon_data, http_results):
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
