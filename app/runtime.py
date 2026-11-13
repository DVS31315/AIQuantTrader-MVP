import asyncio
from app import db
from app.config import settings
from app.market import latest_price
from app.paper import monitor

class PaperMonitor:
    def __init__(self): self.task=None; self.stopping=False
    async def start(self):
        self.stopping=False
        self.task=asyncio.create_task(self._loop(),name="paper-position-monitor")
    async def stop(self):
        self.stopping=True
        if self.task:
            self.task.cancel()
            try: await self.task
            except asyncio.CancelledError: pass
    async def _loop(self):
        db.log_event("PAPER_MONITOR_STARTED",{"interval_seconds":settings.market_poll_seconds})
        while not self.stopping:
            symbols=sorted({p['symbol'] for p in db.get_positions(True)})
            for symbol in symbols:
                try:
                    price=await latest_price(symbol)
                    closed=monitor(symbol,price)
                    if closed: db.log_event("MONITOR_CYCLE_CLOSED",{"symbol":symbol,"closed":closed})
                except asyncio.CancelledError: raise
                except Exception as exc: db.log_event("MONITOR_DATA_ERROR",f"{symbol}: {type(exc).__name__}: {exc}","WARNING")
            await asyncio.sleep(settings.market_poll_seconds)

monitor_service=PaperMonitor()
