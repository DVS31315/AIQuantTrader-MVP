import json, sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from app.config import settings

@contextmanager
def connect():
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(settings.db_path, timeout=15)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    try:
        yield c
        c.commit()
    except Exception:
        c.rollback()
        raise
    finally:
        c.close()

def now_iso(): return datetime.now(timezone.utc).isoformat()

def init_db():
    with connect() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS account(id INTEGER PRIMARY KEY CHECK(id=1), equity REAL NOT NULL, starting_equity REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS positions(
          id INTEGER PRIMARY KEY, symbol TEXT NOT NULL, market TEXT NOT NULL DEFAULT 'crypto', side TEXT NOT NULL,
          qty REAL NOT NULL, entry REAL NOT NULL, stop_loss REAL NOT NULL, take_profit REAL,
          leverage INTEGER NOT NULL, status TEXT NOT NULL, opened_at TEXT NOT NULL, closed_at TEXT,
          exit_price REAL, gross_pnl REAL, fees REAL NOT NULL DEFAULT 0, slippage_cost REAL NOT NULL DEFAULT 0, pnl REAL);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, ts TEXT NOT NULL, level TEXT NOT NULL, event TEXT NOT NULL, details TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS ix_positions_status_symbol ON positions(status,symbol);
        CREATE INDEX IF NOT EXISTS ix_events_id ON events(id DESC);
        ''')
        account_cols={r[1] for r in c.execute("PRAGMA table_info(account)")}
        if "starting_equity" not in account_cols:
            c.execute("ALTER TABLE account ADD COLUMN starting_equity REAL NOT NULL DEFAULT 10000.0")
        cols={r[1] for r in c.execute("PRAGMA table_info(positions)")}
        migrations={"market":"TEXT NOT NULL DEFAULT 'crypto'","gross_pnl":"REAL","fees":"REAL NOT NULL DEFAULT 0","slippage_cost":"REAL NOT NULL DEFAULT 0"}
        for name, decl in migrations.items():
            if name not in cols: c.execute(f"ALTER TABLE positions ADD COLUMN {name} {decl}")
        c.execute("INSERT OR IGNORE INTO account(id,equity,starting_equity) VALUES(1,?,?)",(settings.starting_equity,settings.starting_equity))

def log_event(event, details, level="INFO"):
    payload = details if isinstance(details,str) else json.dumps(details,ensure_ascii=False,default=str)
    with connect() as c: c.execute("INSERT INTO events(ts,level,event,details) VALUES(?,?,?,?)",(now_iso(),level,event,payload))

def get_events(n=100):
    with connect() as c: return [dict(x) for x in c.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?",(max(1,min(int(n),500)),))]

def get_equity():
    with connect() as c: return float(c.execute("SELECT equity FROM account WHERE id=1").fetchone()["equity"])

def get_positions(open_only=False):
    q="SELECT * FROM positions"+(" WHERE status='open'" if open_only else "")+" ORDER BY id DESC"
    with connect() as c: return [dict(x) for x in c.execute(q)]

def add_position(p):
    with connect() as c:
        cur=c.execute('''INSERT INTO positions(symbol,market,side,qty,entry,stop_loss,take_profit,leverage,status,opened_at,fees,slippage_cost)
          VALUES(?,?,?,?,?,?,?,?,'open',?,?,?)''',
          (p['symbol'],p.get('market','crypto'),p['side'],p['qty'],p['entry'],p['stop_loss'],p.get('take_profit'),p['leverage'],now_iso(),p.get('entry_fee',0),p.get('entry_slippage_cost',0)))
        return cur.lastrowid

def close_position(pid, price, gross_pnl, exit_fee, exit_slippage_cost):
    with connect() as c:
        row=c.execute("SELECT fees,slippage_cost FROM positions WHERE id=? AND status='open'",(pid,)).fetchone()
        if row is None: return False
        total_fees=float(row['fees'])+exit_fee
        total_slip=float(row['slippage_cost'])+exit_slippage_cost
        net=float(gross_pnl)-total_fees-total_slip
        cur=c.execute("UPDATE positions SET status='closed',closed_at=?,exit_price=?,gross_pnl=?,fees=?,slippage_cost=?,pnl=? WHERE id=? AND status='open'",
          (now_iso(),price,gross_pnl,total_fees,total_slip,net,pid))
        if cur.rowcount:
            c.execute("UPDATE account SET equity=equity+? WHERE id=1",(net,))
            return True
        return False
