from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Vulnerability:
    type: str
    severity: str
    location: str
    details: str
    cwe_id: Optional[str] = None
    description: Optional[str] = None

@dataclass
class ScanResult:
    target: str
    ip_address: Optional[str] = None
    open_ports: List[int] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)
    vulnerabilities: List[Dict] = field(default_factory=list)
