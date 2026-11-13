# PROJECT STATE — AI QUANT TRADER MVP

## Project boundaries and safety

- Fresh standalone project at `D:\AIQuantTrader_MVP\AIQuantTrader_MVP`.
- Never modify the older project at `D:\AIQuantTrader`.
- All local runtime data, venv, database and logs must remain on D:.
- Paper Trading only: no live orders, private exchange keys or Bybit Demo/Testnet order execution.
- Crypto leverage ceiling 3x. Forex/metals ceiling 5x in risk engine, but these markets remain unavailable until verified quote adapters exist.
- Do not invent prices, daily targets, daily loss limits or trade-count limits.

## Implemented application

- FastAPI dashboard and endpoints in `app/main.py`.
- Bybit public closed-candle and ticker adapter in `app/market.py`.
- RSS ingestion in `app/news.py`.
- Ollama and OpenAI-compatible JSON planner in `app/llm.py`; failures fall back to explicit HOLD. Planner prompt explicitly treats objectives/news as untrusted data and rejects embedded instructions.
- Plan validation in `app/models.py`.
- Risk-based sizing and leverage validation in `app/risk.py`.
- SQLite event/account/position storage in `app/db.py`.
- Paper position open/SL/TP close and fee/slippage accounting in `app/paper.py`.
- Background position polling in `app/runtime.py`.
- Dashboard HTML/CSS/JS is currently embedded in `app/main.py`.

## GitHub repository audit — 2026-11-13

Repository: `DVS31315/AIQuantTrader-MVP`.

### Confirmed source files

Application modules, tests, `requirements.txt`, README, PROJECT_STATE and CHAT_HANDOFF are present in the repository.

### Audit findings and corrections committed

- README previously referred to `install.ps1` and `start.ps1`, but neither existed. Added both scripts.
- README path did not reflect the actual nested Windows project root. Corrected it.
- `.env.example` was missing. Added a safe example configuration; it contains no credentials and defaults Ollama to qwen3:4b. The `Settings` default now matches qwen3:4b.
- `.gitignore` was missing. Added exclusions for venv, .env, database, logs, backups and Python caches.
- Added GitHub Actions workflow to compile and run pytest on pushes and pull requests.
- Installer performs dependency installation, compileall and pytest, and deliberately does not launch the server.
- Start script launches the app only when explicitly invoked by the user.

### Code-review observations (not yet all corrected)

- Dashboard navigation labels Markets, News, Agent, Analytics and Settings are currently decorative; only the Trading workspace is implemented.
- UI displays risk percentage as generic "Configured" rather than the actual configured value.
- News sources are external RSS and may fail; source errors must remain visible. The deprecated Reuters feed was removed from the example configuration.
- The current market snapshot's `change_pct` is the change across the fetched candle window, not a true rolling 24-hour metric; the dashboard label was misleading and must be corrected.
- The monitor evaluates latest ticker snapshots at polling intervals; it is not a guaranteed exchange stop order and can miss intraperiod price excursions.
- Forex/metals remain blocked. TradingView is not an API integration.
- Remote source inspection is not equivalent to running the project on the user's Windows machine.

## Validation history

- Previous local user-confirmed state: compileall successful and 18 pytest tests passed after audit patch.
- Prior API TestClient smoke checks and paper lifecycle checks were performed in an isolated environment as documented in the conversation.
- The new GitHub Actions workflow has been committed but has not yet been observed running to completion.
- The newly added PowerShell scripts have not been executed on the user's PC.
- No server has been started by the assistant.

- Added a unit test that checks the planner's untrusted-news/objective instruction is present. The test is committed but awaits CI execution.

## Next engineering priorities

1. Correct misleading 24h UI label and expose actual risk setting.
2. Expand automated tests for DB lifecycle, agent orchestration, API error paths and runtime monitor.
3. Improve paper monitor semantics/documentation (polling-based trigger simulation, not guaranteed stop execution).
4. Make unsupported dashboard navigation functional or remove/disable it until implemented.
5. End-to-end Windows verification after user runs the installer; only then consider the MVP launch-ready.
