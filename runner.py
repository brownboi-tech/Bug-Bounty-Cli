from app.services.scan_service import execute_scan_pipeline


def run_scan(target: str, fast_mode: bool, output_dir: str):
    return execute_scan_pipeline(target, fast_mode, output_dir)
