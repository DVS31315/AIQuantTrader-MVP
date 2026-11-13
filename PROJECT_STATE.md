# PROJECT STATE — Fresh MVP

- New standalone project intended for `D:\AIQuantTrader_MVP`; old project is not modified.
- Implemented: FastAPI dashboard/API, Bybit public klines, RSS news, optional Ollama planner, labeled deterministic fallback, risk sizing, leverage limits, SQLite event log/account/positions, internal Paper Trading and SL/TP closure.
- Safety: no real-order adapter, no private keys, no Bybit Demo execution; crypto max 3x, forex/metals max 5x.
- Not yet verified on user's Windows PC. No claim of successful local run.
- Current data adapter is Crypto/Bybit only; Forex and Metals connectors are pending.
- Next: extract to D:, install, run tests, start app and perform first end-to-end run.

---

## 2026-11-13 — MVP implementation package prepared (not yet applied locally)

### Implemented in the prepared patch
- Replaced broken SQLite and LLM modules with syntactically valid implementations.
- Added SQLite WAL mode, migration-safe columns for market/fees/slippage, JSON event details, and atomic close/account updates.
- Added OpenAI-compatible HTTP provider and Ollama provider selection through `LLM_PROVIDER`.
- Added strict Pydantic plan validation and fail-safe HOLD on provider errors or invalid output.
- Strengthened risk checks, hard leverage caps, stop/target direction checks, finite numeric validation, and risk-based quantity sizing.
- Added Bybit closed-candle filtering for all supported intervals and public ticker polling.
- Added RSS fetch timeouts and per-feed error isolation.
- Added background paper position monitor for open symbols.
- Added configurable paper fee/slippage assumptions and net realized P&L accounting.
- Replaced unsafe dashboard rendering with escaped text and a dark petrol/glass UI with a locally rendered candle chart.
- Added a launcher that reads APP_HOST/APP_PORT from settings and does not start automatically.
- Forex/Metals remain blocked until verified quote adapters are configured; TradingView remains explicitly not a live API integration.

### Files in package
`app/config.py`, `app/db.py`, `app/models.py`, `app/market.py`, `app/news.py`, `app/llm.py`, `app/risk.py`, `app/paper.py`, `app/agent.py`, `app/runtime.py`, `app/main.py`, `app/run.py`, `app/__init__.py`, `tests/test_risk.py`, `tests/test_models.py`, `tests/test_market.py`, `scripts/run.ps1`, `.env.example`, `README_MVP.md`.

### Validation status
- Package syntax and automated tests must be run after applying to the user's local project environment.
- No local server has been started.
- No local project files have been modified by the assistant; package awaits user-side application.

### Remaining limitations
- Forex and Metals quote adapters are not implemented; requests are rejected instead of using synthetic prices.
- TradingView API is not claimed; candle chart uses Bybit public data.
- RSS news quality and source availability depend on configured feeds.
- Fee/slippage defaults are configurable simulation assumptions (0.055% taker fee and 0.02% slippage per side), not guaranteed venue costs.
- No real order execution, private exchange API credentials, or Bybit testnet order routing exists.


## Актуальный статус — 13.11.2026

- Патч MVP успешно установлен локально.
- Резервная копия: `.backups\mvp_patch_20261113_050557`.
- `app/` содержит все 13 модулей приложения.
- Локальная компиляция: `python -m compileall -q app tests` — успешно.
- Локальные автоматические тесты: **11 passed in 1.42s**.
- Сервер не запускался.
- Старый проект `D:\AIQuantTrader` не изменялся.
- Следующий этап: техническая проверка конфигурации, API, базы данных и внешних подключений до первого запуска.
- Ограничения сохраняются: только внутренний Paper Trading; Forex/Metals заблокированы до подключения проверенных источников котировок; TradingView не заявляется как готовая API-интеграция.

## 13.11.2026 — Technical audit correction package prepared

The first local installation and 11-test run were confirmed by the user. A follow-up audit identified gaps not covered by the initial tests. This correction package addresses them:
- Simulated entry price is refreshed from the Bybit public ticker immediately before a paper fill; model-generated entry prices are never used as fills.
- Stop-loss gap handling uses the worse observed ticker price; take-profit fills are capped at the target.
- Position sizing includes estimated entry+stop fees and slippage inside the risk budget.
- New positions are checked against aggregate margin already used by open positions; concurrent agent requests are serialized.
- Leverage caps are now enforced by configuration validation and cannot be raised above crypto 3x / Forex 5x / Metals 5x.
- Invalid RSS-feed placeholders are excluded from the LLM's news context while feed errors remain visible in logs/results.
- Ticker values are checked for finite positive numbers; app port and Ollama timeout are validated.
- Added tests for configuration caps, execution price ownership, stop gaps, take-profit fills, margin availability, and risk-cost budgeting.

Validation performed against this correction package in the preparation environment: compileall successful; 18 tests passed. This is not yet a claim about the user's local installation. Apply the correction package, then repeat compileall and pytest locally. Server remains stopped.

