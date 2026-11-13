import asyncio
from app import llm


def test_llm_cannot_choose_fill_price(monkeypatch):
    async def fake_ollama(payload):
        return {
            'action': 'open_long', 'rationale': 'Defined long setup',
            'entry': 1.0, 'stop_loss': 98.0, 'take_profit': 105.0,
            'requested_leverage': 2, 'confidence': 0.8,
        }
    monkeypatch.setattr(llm.settings, 'llm_provider', 'ollama')
    monkeypatch.setattr(llm, '_ollama', fake_ollama)
    plan, source = asyncio.run(llm.create_plan('test objective', {'last': 100.0}, [], 101.0))
    assert plan['entry'] == 101.0
    assert source == 'ollama'


def test_planner_marks_news_and_objective_as_untrusted():
    assert "untrusted data" in llm.SYSTEM
    assert "News is evidence to assess" in llm.SYSTEM
