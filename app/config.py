from functools import lru_cache
from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_host: str = "127.0.0.1"
    app_port: int = Field(default=8000, ge=1, le=65535)
    app_name: str = "AI QUANT TRADER"
    database_path: str = "./data/agent.db"
    bybit_base_url: str = "https://api.bybit.com"
    bybit_category: str = "linear"
    default_symbol: str = "BTCUSDT"
    default_timeframe: str = "15"
    candle_limit: int = Field(default=200, ge=60, le=1000)
    market_poll_seconds: int = Field(default=10, ge=3, le=300)
    request_timeout_seconds: float = Field(default=12, gt=0, le=60)
    llm_provider: str = "ollama"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4.1-mini"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen3:4b"
    ollama_timeout_seconds: int = Field(default=45, ge=5, le=180)
    starting_equity: float = Field(default=10000.0, gt=0)
    risk_per_trade_pct: float = Field(default=0.5, gt=0, le=5)
    crypto_max_leverage: int = Field(default=3, ge=1, le=3)
    forex_max_leverage: int = Field(default=5, ge=1, le=5)
    metals_max_leverage: int = Field(default=5, ge=1, le=5)
    taker_fee_pct: float = Field(default=0.055, ge=0, le=1)
    slippage_pct: float = Field(default=0.02, ge=0, le=1)
    news_feeds: str = "https://feeds.reuters.com/reuters/businessNews,https://www.coindesk.com/arc/outboundfeeds/rss/"
    news_limit: int = Field(default=12, ge=1, le=50)
    news_timeout_seconds: float = Field(default=8, gt=0, le=30)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("llm_provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in {"ollama", "openai"}:
            raise ValueError("LLM_PROVIDER must be 'ollama' or 'openai'")
        return v

    @property
    def feed_urls(self) -> list[str]:
        return [x.strip() for x in self.news_feeds.split(",") if x.strip()]

    @property
    def db_path(self) -> Path:
        p = Path(self.database_path)
        return p if p.is_absolute() else Path.cwd() / p

@lru_cache

def get_settings() -> Settings:
    return Settings()

settings = get_settings()
