import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from recon import perform_recon
from http_capture import capture_traffic
from ai_agent import analyze_findings
from enrichment import enrich_findings
from reporting import generate_report
from app.db.models import ScanJob


def execute_scan_pipeline(target: str, fast_mode: bool, output_dir: str) -> dict:
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
        "vulnerabilities": vulnerabilities,
    }

    safe_target = target.replace('/', '_').replace(':', '_')
    report_path = os.path.join(output_dir, f"{safe_target}_report.json")

    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=4)

    generate_report(report_path)
    report_data["report_path"] = report_path
    return report_data


def create_scan_job(db: Session, target: str, fast_mode: bool = False, output_dir: str = "results") -> ScanJob:
    job = ScanJob(target=target, fast_mode=fast_mode, output_dir=output_dir, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def run_scan_job(db: Session, job_id: int) -> ScanJob:
    job = db.get(ScanJob, job_id)
    if not job:
        raise ValueError(f"Scan job {job_id} not found")

    job.status = "running"
    job.started_at = datetime.utcnow()
    db.commit()

    try:
        results = execute_scan_pipeline(job.target, job.fast_mode, job.output_dir)
        job.findings_json = results
        job.status = "completed"
        job.completed_at = datetime.utcnow()
    except Exception as exc:
        job.status = "failed"
        job.error_message = str(exc)
        job.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(job)
    return job
