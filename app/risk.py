from math import isfinite
from app.config import settings

class RiskRejected(ValueError): pass

def size_position(plan, market, equity, risk_pct=None, available_margin=None):
    if market not in {"crypto","forex","metals"}: raise RiskRejected("Unsupported market")
    if plan.get("action")=="hold": return None
    if plan.get("action") not in {"open_long","open_short"}: raise RiskRejected("Unsupported action")
    entry,sl=plan.get("entry"),plan.get("stop_loss")
    if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and isfinite(x) and x>0 for x in (entry,sl,equity)):
        raise RiskRejected("Entry, stop loss and equity must be finite positive numbers")
    if equity<=0: raise RiskRejected("Equity must be positive")
    side="long" if plan["action"]=="open_long" else "short"
    if (side=="long" and sl>=entry) or (side=="short" and sl<=entry): raise RiskRejected("Stop loss is on the wrong side of entry")
    tp=plan.get("take_profit")
    if tp is not None and (not isinstance(tp,(int,float)) or isinstance(tp,bool) or not isfinite(tp) or tp<=0 or (side=="long" and tp<=entry) or (side=="short" and tp>=entry)):
        raise RiskRejected("Take profit is invalid or on the wrong side of entry")
    caps={"crypto":settings.crypto_max_leverage,"forex":settings.forex_max_leverage,"metals":settings.metals_max_leverage}
    lev=plan.get("requested_leverage",1)
    if not isinstance(lev,int) or isinstance(lev,bool) or not 1<=lev<=caps[market]: raise RiskRejected(f"Leverage must be between 1x and {caps[market]}x for {market}")
    rp=settings.risk_per_trade_pct if risk_pct is None else risk_pct
    if not isinstance(rp,(int,float)) or not isfinite(rp) or not 0<rp<=5: raise RiskRejected("Risk percentage must be >0 and <=5")
    risk=equity*rp/100
    fee_rate=settings.taker_fee_pct/100
    slippage_rate=settings.slippage_pct/100
    gross_loss_per_unit=abs(entry-sl)
    estimated_cost_per_unit=(entry+sl)*(fee_rate+slippage_rate)
    total_loss_per_unit=gross_loss_per_unit+estimated_cost_per_unit
    qty=risk/total_loss_per_unit
    notional=qty*entry
    margin_required=notional/lev
    margin_available=equity if available_margin is None else available_margin
    if not isinstance(margin_available,(int,float)) or isinstance(margin_available,bool) or not isfinite(margin_available) or margin_available<0:
        raise RiskRejected("Available margin must be a finite non-negative number")
    if not isfinite(qty) or qty<=0 or margin_required>margin_available: raise RiskRejected("Position exceeds available portfolio margin")
    gross_risk=qty*gross_loss_per_unit
    estimated_fees=qty*(entry+sl)*fee_rate
    estimated_slippage=qty*(entry+sl)*slippage_rate
    return {"side":side,"qty":qty,"entry":float(entry),"stop_loss":float(sl),"take_profit":float(tp) if tp is not None else None,"leverage":lev,"risk_amount":gross_risk+estimated_fees+estimated_slippage,"risk_budget":risk,"gross_risk_amount":gross_risk,"estimated_fees":estimated_fees,"estimated_slippage":estimated_slippage,"notional":notional,"margin_required":margin_required,"market":market}
