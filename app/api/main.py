from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from app.api.schemas import ScanCreateRequest, ScanJobResponse
from app.db.database import Base, SessionLocal, engine
from app.db.models import ScanJob
from app.services.scan_service import create_scan_job, run_scan_job

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bug Bounty API")
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/scans", response_model=ScanJobResponse)
def create_scan(payload: ScanCreateRequest, background: BackgroundTasks, db: Session = Depends(get_db)):
    job = create_scan_job(db, payload.target, payload.fast_mode, payload.output_dir)
    background.add_task(_run_in_background, job.id)
    return job


def _run_in_background(job_id: int):
    db = SessionLocal()
    try:
        run_scan_job(db, job_id)
    finally:
        db.close()


@app.get("/scans/{scan_id}", response_model=ScanJobResponse)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    job = db.get(ScanJob, scan_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scan not found")
    return job


@app.get("/reports/{scan_id}")
def get_report(scan_id: int, db: Session = Depends(get_db)):
    job = db.get(ScanJob, scan_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scan not found")
    if job.status != "completed":
        raise HTTPException(status_code=409, detail="Scan not complete")
    return {
        "id": job.id,
        "target": job.target,
        "status": job.status,
        "findings": job.findings_json.get("vulnerabilities", []),
        "report": job.findings_json,
    }
