# CHAT HANDOFF — AI QUANT TRADER MVP

## Project root and boundaries

- Current project: `D:\AIQuantTrader_MVP\AIQuantTrader_MVP`.
- Older project `D:\AIQuantTrader` is separate and must never be changed.
- Do not assume access to the user's local D: drive. Use the connected GitHub repository for source edits.
- Keep all local venv/database/logs on D:.

## Safety

- Paper Trading only. No real orders, no private exchange keys, no Bybit Demo/Testnet order execution.
- Crypto leverage max 3x. Forex/metals max 5x only after verified quote adapters exist.
- No synthetic quotes or invented prices. No invented daily PnL targets/loss limits/trade-count limits.
- Forex and metals API requests currently return unavailable; only crypto/Bybit public market data is implemented.
- TradingView is not currently a live API integration.

## Current architecture

FastAPI dashboard/API; Bybit public candles and ticker; RSS news; Ollama/OpenAI-compatible planner; fail-safe HOLD; Pydantic plan validation; risk sizing; SQLite event/account/position store; internal paper position lifecycle; background ticker polling.

## Repository updates

The GitHub repository now includes:
- `install.ps1`: creates venv, installs requirements, compiles and runs tests; does not start server.
- `start.ps1`: starts server only when explicitly run.
- `.env.example`: safe local configuration; default Ollama model qwen3:4b.
- `.gitignore`: excludes local secrets, venv, DB, logs and backups.
- `.github/workflows/tests.yml`: compileall and pytest on push/PR.
- Updated README with correct nested project path and limitations.

## Audit notes

- Decorative dashboard navigation items are not implemented pages.
- Dashboard currently labels fetched-candle-window return as "24h / sample change"; this needs correction.
- Dashboard risk label is generic rather than showing configured value.
- Position monitor polls latest ticker; simulated SL/TP behavior is not a guaranteed exchange stop/limit order and can miss intraperiod excursions.
- RSS depends on upstream availability.
- Remote review does not establish Windows end-to-end success.

## Next steps

1. Continue code audit and correct misleading dashboard metrics.
2. Add tests for API, DB, orchestration and monitor behavior.
3. Check GitHub Actions result when available.
4. User can run `Set-Location "D:\AIQuantTrader_MVP\AIQuantTrader_MVP"; .\install.ps1` when ready. This does not start the server.
5. Server startup requires the user's explicit decision via `.\start.ps1`.
