import pytest
from app.models import AgentPlan

def test_hold_plan():
    p=AgentPlan.validate_trade({'action':'hold','rationale':'No valid setup; wait.','confidence':.2})
    assert p.action=='hold' and p.entry is None

def test_long_plan_requires_correct_stop():
    with pytest.raises(ValueError): AgentPlan.validate_trade({'action':'open_long','rationale':'Setup invalid stop','entry':100,'stop_loss':101,'requested_leverage':2})

def test_trade_plan_valid():
    p=AgentPlan.validate_trade({'action':'open_long','rationale':'Defined long setup','entry':100,'stop_loss':98,'take_profit':104,'requested_leverage':3,'confidence':.7})
    assert p.take_profit==104
