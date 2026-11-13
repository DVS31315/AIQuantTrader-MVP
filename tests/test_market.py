from app.market import snapshot,INTERVAL_MS

def test_snapshot():
    cs=[{'close':100+i,'high':101+i,'low':99+i} for i in range(60)]
    s=snapshot(cs)
    assert s['last']==159 and s['sma20']>s['sma50']

def test_interval_map_has_supported_periods():
    assert {'1','3','5','15','30','60','120','240','360','720','D','W','M'} <= set(INTERVAL_MS)
