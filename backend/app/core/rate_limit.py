"""Lightweight in-memory rate limiter per IP address."""

import time
from collections import defaultdict
from typing import Dict, List
from fastapi import Request

from app.core.config import settings
from app.core.exceptions import RateLimitExceededError


class InMemoryRateLimiter:
    """
    Sliding window rate limiter tracking request timestamps per client IP.
    Note: In multi-worker production setups, a shared store like Redis is recommended.
    """

    def __init__(self, requests_limit: int, window_seconds: int, enabled: bool = True):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.enabled = enabled
        self._clients: Dict[str, List[float]] = defaultdict(list)

    def check(self, request: Request) -> None:
        if not self.enabled:
            return

        client_ip = (
            request.headers.get("x-forwarded-for")
            or (request.client.host if request.client else "unknown")
        ).split(",")[0].strip()

        now = time.time()
        window_start = now - self.window_seconds

        # Prune outdated timestamps
        recent_timestamps = [t for t in self._clients[client_ip] if t > window_start]
        self._clients[client_ip] = recent_timestamps

        if len(recent_timestamps) >= self.requests_limit:
            retry_after = int(self.window_seconds - (now - recent_timestamps[0]))
            raise RateLimitExceededError(
                f"Rate limit exceeded. Maximum {self.requests_limit} requests per "
                f"{self.window_seconds}s. Try again in {max(1, retry_after)} seconds."
            )

        self._clients[client_ip].append(now)


limiter = InMemoryRateLimiter(
    requests_limit=settings.RATE_LIMIT_REQUESTS,
    window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
    enabled=settings.RATE_LIMIT_ENABLED,
)
