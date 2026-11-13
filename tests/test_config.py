import pytest
from pydantic import ValidationError
from app.config import Settings


def test_hard_leverage_caps_cannot_be_raised():
    with pytest.raises(ValidationError):
        Settings(crypto_max_leverage=4)
    with pytest.raises(ValidationError):
        Settings(forex_max_leverage=6)
    with pytest.raises(ValidationError):
        Settings(metals_max_leverage=6)


def test_app_port_is_validated():
    with pytest.raises(ValidationError):
        Settings(app_port=70000)
