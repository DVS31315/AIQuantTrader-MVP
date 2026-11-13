# CHAT HANDOFF

Continue with fresh standalone package at `D:\AIQuantTrader_MVP`; do not alter or delete old `D:\AIQuantTrader`.
All runtime files/venv/database/logs must stay on D:.
Paper Trading only. No real orders, API keys or Bybit Demo execution.
Leverage caps: Crypto 3x; Forex/Metals 5x. Do not invent daily PnL lockouts.
Current package: FastAPI UI, Bybit public market data, RSS news, optional local Ollama planner, labeled fallback, risk sizing, SQLite and internal paper positions.
Windows install/test/run is still unverified. Forex/Metals live feeds are not implemented.
Immediate next step: install.ps1, pytest, start.ps1, then one agent run.

---

## Handoff — 2026-11-13 MVP package

Current target remains `D:\AIQuantTrader_MVP\AIQuantTrader_MVP`. Do not touch `D:\AIQuantTrader`.

A replacement package has been prepared as a patch archive. It must be applied from the target project root using the supplied PowerShell installer. The installer backs up overwritten files into a timestamped `.backups` folder, then copies the replacement modules and appends this handoff plus the project-state entry. It does not launch the server.

Architecture: FastAPI app; SQLite WAL store; Bybit public REST for closed candles and ticker prices; RSS news via bounded HTTP requests; OpenAI-compatible and Ollama LLM provider; Pydantic plan validation; risk-based sizing; local paper position book; background SL/TP monitor; browser dashboard.

Safety constraints: paper only; no private exchange keys; no live order endpoints; crypto leverage <=3x; Forex/Metals <=5x in Risk Engine but unavailable until verified feeds are integrated; no fabricated quotes; fail-safe HOLD if LLM fails; no invented daily limits.

After patch application: run compileall and pytest only (do not start the server until tests are reviewed). Then report exact test output. The launcher is `scripts\run.ps1` or `python -m app.run` and reads APP_HOST/APP_PORT. Server launch requires user authorization/instruction.



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

## Handoff update — 13.11.2026 technical audit corrections

Target: `D:\AIQuantTrader_MVP\AIQuantTrader_MVP`. Never modify `D:\AIQuantTrader`.

A follow-up correction patch is ready. It makes the simulated fill price come from a fresh Bybit public ticker immediately before opening; model-generated entry prices are ignored. It improves stop-gap fills, includes estimated fees/slippage in the per-trade risk budget, checks aggregate used margin, serializes concurrent agent runs, hard-validates leverage caps, filters failed RSS placeholders from LLM context, and validates ticker values. Tests were expanded.

Preparation-environment validation: `compileall` succeeded and 18 tests passed. This result must be repeated locally after applying the correction package. No server has been started. Paper Trading only; no real orders. Forex/Metals remain blocked. TradingView is not a live API integration. Do not create `.env` or start the server without the user's explicit instruction.

