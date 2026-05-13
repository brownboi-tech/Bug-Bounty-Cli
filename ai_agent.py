import json
import os
import shutil
import subprocess
from typing import Any, Dict, List

from openai import OpenAI


class ToolManager:
    def __init__(self) -> None:
        self.tool_registry = {
            "nmap": "apt-get install -y nmap",
            "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "nuclei": "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
            "whatweb": "apt-get install -y whatweb",
            "ffuf": "apt-get install -y ffuf",
            "dirsearch": "pip install dirsearch",
            "sqlmap": "apt-get install -y sqlmap",
            "nikto": "apt-get install -y nikto",
            "amass": "apt-get install -y amass",
        }

    def ensure_tool(self, tool_name: str) -> bool:
        if shutil.which(tool_name):
            return True

        print(f"[AI Agent] Installing missing tool: {tool_name}...")
        install_cmd = self.tool_registry.get(tool_name)
        if not install_cmd:
            return False

        try:
            subprocess.run(install_cmd, shell=True, check=True, capture_output=True)
            return True
        except subprocess.SubprocessError:
            return False

    def run_tool(self, tool_name: str, args: List[str]) -> str:
        if not self.ensure_tool(tool_name):
            return ""

        full_cmd = [tool_name] + args
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout


def analyze_with_llm(data_context: Dict[str, Any]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "LLM analysis skipped: OPENAI_API_KEY is not set."

    try:
        client = OpenAI(api_key=api_key)
        prompt = (
            "You are a senior offensive security analyst. Analyze the following recon + HTTP discovery data "
            "for likely vulnerabilities, exploitation paths, and severity. Return concise bullet points with risk "
            "reasoning and remediation hints.\n\n"
            f"Input data:\n{json.dumps(data_context, indent=2)}"
        )

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            max_output_tokens=700,
        )
        return response.output_text.strip()
    except Exception as exc:  # best-effort external API call
        return f"LLM analysis skipped (OpenAI error: {exc})"


def analyze_findings(recon_data: Dict[str, Any], http_results: Dict[str, Any]) -> List[Dict[str, str]]:
    print("[AI Agent] Initiating autonomous analysis phase...")
    tm = ToolManager()
    vulnerabilities: List[Dict[str, str]] = []

    if recon_data.get("open_ports") and recon_data.get("ip_address"):
        ports = ",".join(map(str, recon_data["open_ports"]))
        tm.run_tool("nmap", ["-sV", "-p", ports, recon_data["ip_address"]])

    sensitive_patterns = [".env", "config", "backup", "admin"]
    for url in http_results.get("endpoints", []):
        if any(pattern in url.lower() for pattern in sensitive_patterns):
            vulnerabilities.append(
                {
                    "type": "Potential Sensitive File Exposure",
                    "severity": "High",
                    "location": url,
                    "details": f"Sensitive path accessible: {url}",
                }
            )

    risky_ports = {21: "FTP", 22: "SSH", 23: "Telnet"}
    for port in recon_data.get("open_ports", []):
        if port in risky_ports:
            vulnerabilities.append(
                {
                    "type": "Exposed Management Service",
                    "severity": "Medium",
                    "location": f"Port {port} ({risky_ports[port]})",
                    "details": f"Service {risky_ports[port]} exposed on port {port}",
                }
            )

    if http_results.get("endpoints"):
        print("[AI Agent] Launching OpenAI analysis...")
        llm_report = analyze_with_llm({"recon": recon_data, "web": http_results})
        vulnerabilities.append(
            {
                "type": "LLM Insight",
                "severity": "Variable",
                "location": "Logic Analysis",
                "details": llm_report,
            }
        )

    print(f"[AI Agent] Analysis complete. Identified {len(vulnerabilities)} issues.")
    return vulnerabilities
