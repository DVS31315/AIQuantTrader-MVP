import sqlite3
from app import db
from app.config import settings

def test_migrates_legacy_database(tmp_path,monkeypatch):
    path=tmp_path/'legacy.db'
    c=sqlite3.connect(path)
    c.executescript('''
      CREATE TABLE account(id INTEGER PRIMARY KEY CHECK(id=1),equity REAL);
      INSERT INTO account VALUES(1,1234.5);
      CREATE TABLE positions(id INTEGER PRIMARY KEY,symbol TEXT,side TEXT,qty REAL,entry REAL,stop_loss REAL,take_profit REAL,leverage INTEGER,status TEXT,opened_at TEXT,closed_at TEXT,exit_price REAL,pnl REAL);
      CREATE TABLE events(id INTEGER PRIMARY KEY,ts TEXT,level TEXT,event TEXT,details TEXT);
    '''); c.commit(); c.close()
    monkeypatch.setattr(settings,'database_path',str(path))
    db.init_db()
    assert db.get_equity()==1234.5
    with db.connect() as c:
        pcols={r[1] for r in c.execute('PRAGMA table_info(positions)')}
        acols={r[1] for r in c.execute('PRAGMA table_info(account)')}
    assert {'market','fees','slippage_cost','gross_pnl'} <= pcols
    assert 'starting_equity' in acols
