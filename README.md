# AI QUANT TRADER — Fresh MVP

Standalone fresh project. Extract to **D:\AIQuantTrader_MVP**. All venv, database, logs and runtime data stay inside this folder.

## Install / run
```powershell
Set-Location D:\AIQuantTrader_MVP
.\install.ps1
Copy-Item .env.example .env
.\start.ps1
```
Open http://127.0.0.1:8000. Run tests with:
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Included
- FastAPI dashboard and API.
- Bybit public market candles (no API keys).
- RSS news ingestion.
- Optional local Ollama planner; deterministic fallback clearly labeled.
- Risk sizing from stop distance; Crypto max leverage 3x, Forex/Metals 5x.
- Internal SQLite Paper Trading positions, SL/TP monitoring and event log.
- No real-order API, no exchange credentials, no Bybit Demo execution.

## Current scope
This MVP's live market-data adapter is Crypto/Bybit only. Forex and Metals are represented in the domain/risk model but do not yet have live data connectors. The agent requires a valid SL for an opening trade so position risk can be calculated. This is a technical MVP, not a profitability claim.
Ollama is optional; set `OLLAMA_MODEL` in `.env` to a model already installed locally (e.g. qwen3:8b).
