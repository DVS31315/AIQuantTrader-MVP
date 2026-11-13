# AI QUANT TRADER — Paper Trading MVP

Standalone project. On the user's Windows machine the project root is:
`D:\AIQuantTrader_MVP\AIQuantTrader_MVP`

## Windows setup

Open PowerShell in the project root and run:

```powershell
Set-Location "D:\AIQuantTrader_MVP\AIQuantTrader_MVP"
.\install.ps1
```

The installer creates `.venv`, installs `requirements.txt`, creates `.env` from `.env.example` if needed, compiles the Python modules and runs pytest. **It does not start the server.**

To start the app only when you choose:

```powershell
.\start.ps1
```

Then open http://127.0.0.1:8000. Stop the server with Ctrl+C.

## LLM configuration

Default provider is local Ollama. The example configuration uses `qwen3:4b`; change `OLLAMA_MODEL` in your local `.env` only to a model installed in Ollama. For OpenAI, set `LLM_PROVIDER=openai` and provide `OPENAI_API_KEY` locally. Never commit `.env` or API keys.

## Included

- FastAPI dashboard and JSON API.
- Bybit public REST market candles and ticker prices; no exchange API keys.
- RSS news ingestion with timeouts and per-feed error isolation.
- Ollama / OpenAI-compatible planner; invalid or unavailable model response fails closed to HOLD.
- Pydantic trade-plan validation and risk-based position sizing.
- Hard leverage ceilings: crypto 3x; Forex and metals 5x in the risk model.
- Internal SQLite paper positions, estimated fees/slippage, SL/TP monitoring and event log.
- GitHub Actions compile + pytest workflow.

## Explicit limitations

- **Paper Trading only.** No live order routing, private exchange credentials or Bybit Demo/Testnet order execution.
- Crypto/Bybit is the only implemented live quote adapter. Forex and metals are rejected by the API until verified data adapters are implemented.
- The chart displays Bybit public candles; TradingView is not integrated as a live API.
- RSS availability and quality depend on upstream feeds. Failed feeds are exposed in logs.
- Fees and slippage are configurable simulation assumptions, not guaranteed exchange fills.
- A technically valid MVP is not evidence of profitability. Use paper mode and review every decision.

## API

- `GET /` — dashboard
- `GET /api/status` — app, paper account and recent events
- `POST /api/run` — run one autonomous paper-analysis task
- `GET /api/events` — event log
- `GET /api/positions` — open and historical paper positions
- `GET /api/market/{symbol}?timeframe=15` — public market snapshot and candles

## Tests

```powershell
.\.venv\Scripts\python.exe -m compileall -q app tests
.\.venv\Scripts\python.exe -m pytest -q
```
