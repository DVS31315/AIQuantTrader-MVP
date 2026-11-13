from typing import Literal
from pydantic import BaseModel, Field, field_validator

class RunRequest(BaseModel):
    objective: str = Field(default="Analyze BTCUSDT using current market data and recent news. Stay flat if evidence is insufficient.",min_length=5,max_length=2000)
    symbol: str = Field(default="BTCUSDT",min_length=3,max_length=30,pattern=r"^[A-Za-z0-9._-]+$")
    market: Literal["crypto","forex","metals"] = "crypto"
    timeframe: str = "15"

    @field_validator("timeframe")
    @classmethod
    def valid_tf(cls,v):
        if v not in {"1","3","5","15","30","60","120","240","360","720","D","W","M"}:
            raise ValueError("Unsupported Bybit timeframe")
        return v

class AgentPlan(BaseModel):
    action: Literal["hold","open_long","open_short"]
    rationale: str = Field(min_length=5,max_length=2000)
    entry: float | None = None
    stop_loss: float | None = None
    take_profit: float | None = None
    requested_leverage: int = Field(default=1,ge=1,le=5)
    confidence: float = Field(default=0.0,ge=0,le=1)

    @field_validator("entry","stop_loss","take_profit")
    @classmethod
    def positive_if_set(cls,v):
        if v is not None and (not __import__('math').isfinite(v) or v<=0): raise ValueError("Price fields must be finite and positive")
        return v

    @classmethod
    def validate_trade(cls, raw):
        plan=cls.model_validate(raw)
        if plan.action=="hold":
            plan.entry=plan.stop_loss=plan.take_profit=None
        elif plan.entry is None or plan.stop_loss is None:
            raise ValueError("Trade plan requires entry and stop_loss")
        elif plan.action=="open_long":
            if plan.stop_loss>=plan.entry: raise ValueError("Long stop loss must be below entry")
            if plan.take_profit is not None and plan.take_profit<=plan.entry: raise ValueError("Long take profit must be above entry")
        else:
            if plan.stop_loss<=plan.entry: raise ValueError("Short stop loss must be above entry")
            if plan.take_profit is not None and plan.take_profit>=plan.entry: raise ValueError("Short take profit must be below entry")
        return plan
