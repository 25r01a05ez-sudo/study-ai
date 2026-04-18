from collections import defaultdict
from datetime import UTC, date, datetime

from fastapi import HTTPException, Request, status

from .config import settings

_RATE_COUNTER: dict[tuple[str, date], int] = defaultdict(int)
_INJECTION_PATTERNS = (
    "ignore previous instructions",
    "system prompt",
    "developer message",
    "reveal hidden",
    "bypass safety",
)


def require_api_key(request: Request) -> str:
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != settings.app_secret_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key


def enforce_rate_limit(api_key: str, tier: str) -> None:
    today = date.today()
    key = (api_key, today)
    _RATE_COUNTER[key] += 1
    limit = settings.rate_limit_pro_per_day if tier == "pro" else settings.rate_limit_free_per_day
    if _RATE_COUNTER[key] > limit:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Daily limit exceeded")


def moderate_user_input(text: str) -> None:
    normalized = text.lower()
    if any(pattern in normalized for pattern in _INJECTION_PATTERNS):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt injection-like content detected")
    if len(text.strip()) < 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Idea is too short")


def now_iso() -> str:
    return datetime.now(UTC).isoformat()
