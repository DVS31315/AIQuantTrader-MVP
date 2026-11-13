from app import db
from app.config import settings
from app.market import candles,snapshot,latest_price
from app.news import recent_news
from app.llm import create_plan,fallback_plan
from app.models import AgentPlan
from app.risk import size_position,RiskRejected
from app.paper import open_position,monitor
import asyncio

_run_lock=asyncio.Lock()

async def run(objective,symbol,market,timeframe):
    # Serialize agent runs so simultaneous requests cannot spend the same free margin.
    async with _run_lock:
        return await _run_once(objective,symbol,market,timeframe)

async def _run_once(objective,symbol,market,timeframe):
    symbol=symbol.upper()
    if market!="crypto":
        raise ValueError("No verified live quote adapter is configured for Forex/Metals. Trading is blocked rather than using fabricated prices.")
    db.log_event("TASK_ACCEPTED",{"objective":objective,"symbol":symbol,"market":market,"timeframe":timeframe})
    cs=await candles(symbol,timeframe); snap=snapshot(cs)
    current_price=await latest_price(symbol)
    snap["current_price"]=current_price
    db.log_event("MARKET_DATA_LOADED",{"symbol":symbol,"snapshot":snap,"source":"Bybit public market data","closed_candles_only":True})
    closed=monitor(symbol,current_price)
    news=await recent_news()
    usable_news=[item for item in news if not item.get("error")]
    feed_errors=[item for item in news if item.get("error")]
    db.log_event("NEWS_LOADED",{"count":len(usable_news),"items":usable_news,"feed_errors":feed_errors})
    try:
        raw,source=await create_plan(objective,snap,usable_news,current_price)
        plan=AgentPlan.validate_trade(raw).model_dump()
    except Exception as exc:
        source="fail_safe"
        plan=fallback_plan(snap)
        db.log_event("PLANNER_FAILED",f"{type(exc).__name__}: {exc}; no trade will be opened","WARNING")
    plan.update({"symbol":symbol,"source":source})
    db.log_event("PLAN_CREATED",plan)
    result={"mode":"paper","real_orders_enabled":False,"market_snapshot":snap,"news":news,"plan":plan,"closed_positions":closed,"opened_position":None}
    if plan['action']!="hold":
        try:
            # Refresh immediately before the paper fill; do not execute at the older analysis quote.
            execution_price=await latest_price(symbol)
            plan=AgentPlan.validate_trade({**plan,"entry":execution_price}).model_dump()
            plan.update({"symbol":symbol,"source":source})
            db.log_event("PAPER_FILL_PRICE_REFRESHED",{"symbol":symbol,"execution_price":execution_price})
            result["plan"]=plan
            equity=db.get_equity()
            open_positions=db.get_positions(True)
            used_margin=sum((float(p['qty'])*float(p['entry']))/max(1,int(p['leverage'])) for p in open_positions)
            available_margin=max(0.0,equity-used_margin)
            sized=size_position(plan,market,equity,available_margin=available_margin)
            result['risk']={k:v for k,v in sized.items() if k not in {'qty'}}
            result['opened_position']=open_position(symbol,sized)
        except (RiskRejected,KeyError,TypeError,ValueError) as exc:
            result['risk_rejection']=str(exc); db.log_event("RISK_REJECTED",str(exc),"WARNING")
    else: result['risk']={"status":"not_required","reason":"HOLD"}
    db.log_event("TASK_COMPLETED",{"action":plan['action'],"planner":source,"opened":bool(result['opened_position'])})
    return result
