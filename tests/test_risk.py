import pytest
from app.risk import size_position,RiskRejected

def test_crypto_sizing_and_risk_invariant():
    x=size_position({"action":"open_long","entry":100,"stop_loss":98,"requested_leverage":3},"crypto",10000,.5)
    assert x['qty'] < 25
    assert x['risk_amount']==pytest.approx(50)
    assert x['gross_risk_amount'] < x['risk_budget']
    assert x['estimated_fees'] > 0 and x['estimated_slippage'] > 0

def test_market_leverage_caps():
    for market,lev in [('crypto',4),('forex',6),('metals',6)]:
        with pytest.raises(RiskRejected): size_position({"action":"open_long","entry":100,"stop_loss":98,"requested_leverage":lev},market,10000,.5)

def test_invalid_values_rejected():
    for entry,sl,equity in [(100,101,10000),(100,98,float('nan')),(0,1,10000),(100,98,-1)]:
        with pytest.raises(RiskRejected): size_position({"action":"open_long","entry":entry,"stop_loss":sl,"requested_leverage":1},"crypto",equity,.5)

def test_short_tp_and_stop_direction():
    p={"action":"open_short","entry":100,"stop_loss":102,"take_profit":95,"requested_leverage":2}
    assert size_position(p,'crypto',10000,.5)['side']=='short'
    with pytest.raises(RiskRejected): size_position({**p,'take_profit':105},'crypto',10000,.5)

def test_hold_never_opens():
    assert size_position({'action':'hold'},'crypto',10000,.5) is None


def test_existing_positions_reduce_available_margin():
    plan = {"action": "open_long", "entry": 100, "stop_loss": 98, "requested_leverage": 3}
    with pytest.raises(RiskRejected):
        size_position(plan, "crypto", 10000, .5, available_margin=1)


def test_boolean_take_profit_is_rejected():
    plan = {"action": "open_long", "entry": 100, "stop_loss": 98, "take_profit": True, "requested_leverage": 2}
    with pytest.raises(RiskRejected):
        size_position(plan, "crypto", 10000, .5)
