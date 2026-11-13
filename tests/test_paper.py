from app import paper


def test_stop_gap_uses_worse_observed_fill(monkeypatch):
    position = {
        'id': 7, 'symbol': 'BTCUSDT', 'side': 'long', 'qty': 1.0,
        'entry': 100.0, 'stop_loss': 98.0, 'take_profit': 105.0,
        'fees': 0.0, 'slippage_cost': 0.0,
    }
    monkeypatch.setattr(paper.db, 'get_positions', lambda open_only=False: [position])
    closed = {}
    def close_position(pid, price, gross_pnl, exit_fee, exit_slippage_cost):
        closed.update(price=price, gross=gross_pnl)
        return True
    monkeypatch.setattr(paper.db, 'close_position', close_position)
    monkeypatch.setattr(paper.db, 'log_event', lambda *args, **kwargs: None)
    result = paper.monitor('BTCUSDT', 96.0)
    assert closed['price'] == 96.0
    assert closed['gross'] == -4.0
    assert result[0]['reason'] == 'STOP_LOSS'


def test_take_profit_does_not_fill_better_than_limit(monkeypatch):
    position = {
        'id': 8, 'symbol': 'BTCUSDT', 'side': 'long', 'qty': 1.0,
        'entry': 100.0, 'stop_loss': 98.0, 'take_profit': 105.0,
        'fees': 0.0, 'slippage_cost': 0.0,
    }
    monkeypatch.setattr(paper.db, 'get_positions', lambda open_only=False: [position])
    closed = {}
    def close_position(pid, price, gross_pnl, exit_fee, exit_slippage_cost):
        closed.update(price=price, gross=gross_pnl)
        return True
    monkeypatch.setattr(paper.db, 'close_position', close_position)
    monkeypatch.setattr(paper.db, 'log_event', lambda *args, **kwargs: None)
    paper.monitor('BTCUSDT', 108.0)
    assert closed['price'] == 105.0
    assert closed['gross'] == 5.0
