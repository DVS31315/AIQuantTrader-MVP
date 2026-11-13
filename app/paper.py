from app import db
from app.config import settings

def _costs(notional):
    return notional*settings.taker_fee_pct/100, notional*settings.slippage_pct/100

def open_position(symbol,sized):
    notional=sized['qty']*sized['entry']; fee,slip=_costs(notional)
    p={"symbol":symbol.upper(),**sized,"entry_fee":fee,"entry_slippage_cost":slip}
    pid=db.add_position(p)
    db.log_event("PAPER_POSITION_OPENED",{"id":pid,**p,"cost_assumptions":{"taker_fee_pct":settings.taker_fee_pct,"slippage_pct":settings.slippage_pct}})
    return {"id":pid,**p,"status":"open"}

def monitor(symbol,price):
    closed=[]
    if not isinstance(price,(int,float)) or price<=0: return closed
    for p in db.get_positions(True):
        if p['symbol']!=symbol.upper(): continue
        long=p['side']=='long'
        sl_hit=price<=p['stop_loss'] if long else price>=p['stop_loss']
        tp=p['take_profit']; tp_hit=tp is not None and (price>=tp if long else price<=tp)
        if not (sl_hit or tp_hit): continue
        if sl_hit:
            # A stop is a trigger, not a guaranteed fill: account for a gap through it.
            raw_exit=min(price,p['stop_loss']) if long else max(price,p['stop_loss'])
        else:
            # A take-profit is treated as a limit fill at its trigger, never improved by a gap.
            raw_exit=tp
        exit_price=raw_exit
        gross=(exit_price-p['entry'])*p['qty']*(1 if long else -1)
        exit_notional=exit_price*p['qty']; fee,slip=_costs(exit_notional)
        if db.close_position(p['id'],exit_price,gross,fee,slip):
            net=gross-float(p.get('fees') or 0)-float(p.get('slippage_cost') or 0)-fee-slip
            item={"id":p['id'],"exit_price":exit_price,"gross_pnl":gross,"fees":float(p.get('fees') or 0)+fee,"slippage_cost":float(p.get('slippage_cost') or 0)+slip,"pnl":net,"reason":"STOP_LOSS" if sl_hit else "TAKE_PROFIT"}
            db.log_event("PAPER_POSITION_CLOSED",item); closed.append(item)
    return closed
