import time
import httpx
from app.config import settings

INTERVAL_MS={"1":60_000,"3":180_000,"5":300_000,"15":900_000,"30":1_800_000,"60":3_600_000,"120":7_200_000,"240":14_400_000,"360":21_600_000,"720":43_200_000,"D":86_400_000,"W":604_800_000,"M":2_592_000_000}

async def candles(symbol, interval, limit=None):
    if interval not in INTERVAL_MS: raise ValueError(f"Unsupported interval: {interval}")
    params={"category":settings.bybit_category,"symbol":symbol.upper(),"interval":interval,"limit":min(limit or settings.candle_limit,1000)}
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        r=await client.get(settings.bybit_base_url+"/v5/market/kline",params=params); r.raise_for_status(); data=r.json()
    if data.get("retCode")!=0: raise RuntimeError(data.get("retMsg","Bybit API error"))
    now=int(time.time()*1000)
    rows=data.get("result",{}).get("list",[])
    out=[]
    for x in reversed(rows):
        ts=int(x[0])
        if ts+INTERVAL_MS[interval] > now: continue
        o,h,l,cl,vol=map(float,x[1:6])
        if not all(map(__import__('math').isfinite,(o,h,l,cl,vol))) or min(o,h,l,cl)<=0 or h<max(o,cl,l) or l>min(o,cl,h): continue
        out.append({"timestamp":ts,"open":o,"high":h,"low":l,"close":cl,"volume":vol})
    if len(out)<50: raise RuntimeError(f"Not enough closed candles returned: {len(out)}")
    return out

def snapshot(cs):
    if len(cs)<50: raise ValueError("At least 50 closed candles are required")
    closes=[x["close"] for x in cs]; last=closes[-1]
    return {"last":last,"sma20":sum(closes[-20:])/20,"sma50":sum(closes[-50:])/50,
      "momentum_5_candles_pct":(last/closes[-6]-1)*100,"change_pct":(last/closes[0]-1)*100,
      "recent_high":max(x["high"] for x in cs[-20:]),"recent_low":min(x["low"] for x in cs[-20:]),"candles":len(cs),"last_closed_candle_ts":cs[-1].get("timestamp")}

async def latest_price(symbol):
    params={"category":settings.bybit_category,"symbol":symbol.upper()}
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        r=await client.get(settings.bybit_base_url+"/v5/market/tickers",params=params); r.raise_for_status(); data=r.json()
    if data.get("retCode")!=0: raise RuntimeError(data.get("retMsg","Bybit ticker error"))
    rows=data.get("result",{}).get("list",[])
    if not rows: raise RuntimeError(f"No ticker for {symbol}")
    price=float(rows[0]["lastPrice"])
    if not __import__('math').isfinite(price) or price<=0:
        raise RuntimeError(f"Invalid ticker price for {symbol}")
    return price
