# Bug-Bounty-Cli

Autonomous bug bounty toolkit for reconnaissance, surface discovery, and AI-assisted triage.

## Highlights
- Modular scan pipeline: recon → HTTP discovery → AI analysis → CWE enrichment → report.
- Packaged under `src/hexa_ai` for clean imports and deployment.
- Two executable entrypoints:
  - `hexa-ai` (CLI)
  - `hexa-ai-server` (HTTP API)

## Installation
```bash
pip install -r requirements.txt
pip install .
```

## Configuration (`.env` + env vars)
Create a `.env` file for local Parrot OS runtime:

```bash
OPENAI_API_KEY=your_key_here
HEXA_AI_HOST=0.0.0.0
HEXA_AI_PORT=8080
HEXA_AI_OUTPUT_DIR=results
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hexa_ai
```

## Local run modes

### 1) CLI mode
```bash
hexa-ai scan example.com --fast --output results
hexa-ai monitor example.com --interval 3600
```

### 2) API-only mode
```bash
hexa-ai-server
```
Then call:
```bash
curl -X POST http://localhost:8080/scan \
  -H 'Content-Type: application/json' \
  -d '{"target":"example.com","fast":true}'
```

### 3) Full web platform mode (API + DB)
```bash
docker compose up --build
```
- API: `http://localhost:8080`
- Postgres: `localhost:5432`

## Disclaimer
Use only on assets you own or are explicitly authorized to test.
