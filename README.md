# Bug-Bounty-Cli

Autonomous bug bounty CLI for reconnaissance, surface discovery, and AI-assisted triage.

## Highlights
- Modular scan pipeline: recon → HTTP discovery → AI analysis → CWE enrichment → report.
- CLI commands for one-off scans and continuous monitoring.
- OpenAI-powered vulnerability reasoning using `OPENAI_API_KEY`.

## Installation
```bash
pip install -r requirements.txt
```

## Quick start
```bash
python main.py scan example.com --fast --output results
```

Or install as a command:
```bash
pip install .
bugbounty scan example.com
```

## Environment variables
- `OPENAI_API_KEY`: required for AI analysis stage.

## Disclaimer
Use only on assets you own or are explicitly authorized to test.
