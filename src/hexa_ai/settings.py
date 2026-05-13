from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(dotenv_path: str = '.env') -> None:
    path = Path(dotenv_path)
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = ''
    api_host: str = '0.0.0.0'
    api_port: int = 8080
    database_url: str = 'postgresql://postgres:postgres@db:5432/hexa_ai'
    scan_output_dir: str = 'results'



def get_settings() -> Settings:
    _load_dotenv()
    return Settings(
        openai_api_key=os.getenv('OPENAI_API_KEY', ''),
        api_host=os.getenv('HEXA_AI_HOST', '0.0.0.0'),
        api_port=int(os.getenv('HEXA_AI_PORT', '8080')),
        database_url=os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/hexa_ai'),
        scan_output_dir=os.getenv('HEXA_AI_OUTPUT_DIR', 'results'),
    )
