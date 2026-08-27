from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

from fastapi import FastAPI, HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class RateLimitBackend(Protocol):
    async def register_request(self, key: str, window_seconds: int, max_requests: int) -> "RateLimitDecision": ...


@dataclass(slots=True)
class RateLimitDecision:
    allowed: bool
    remaining: int
    retry_after_seconds: int
    limit: int


class RedisSlidingWindowRateLimiter:
    """Distributed sliding-window limiter backed by a Redis sorted set.

    Uses ZADD/ZREMRANGEBYSCORE/ZCARD inside a Lua script to avoid race
    conditions between concurrent workers acting on the same client key.
    """

    _LUA_SCRIPT = """
    local key = KEYS[1]
    local now = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
    local max_requests = tonumber(ARGV[3])
    local member = ARGV[4]

    redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
    local current = redis.call('ZCARD', key)

    if current >= max_requests then
        local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
        local retry_after = window
        if oldest[2] ~= nil then
            retry_after = math.ceil((tonumber(oldest[2]) + window) - now)
        end
        return {0, current, retry_after}
    end

    redis.call('ZADD', key, now, member)
    redis.call('EXPIRE', key, window)
    return {1, current + 1, 0}
    """

    def __init__(self, redis_client: "AsyncRedisClient") -> None:
        self._redis = redis_client
        self._script_sha: str | None = None

    async def _ensure_script_loaded(self) -> str:
        if self._script_sha is None:
            self._script_sha = await self._redis.script_load(self._LUA_SCRIPT)
        return self._script_sha

    async def register_request(self, key: str, window_seconds: int, max_requests: int) -> RateLimitDecision:
        script_sha = await self._ensure_script_loaded()
        now = time.time()
        member = f"{now}:{id(self)}"
        allowed, current, retry_after = await self._redis.evalsha(
            script_sha,
            keys=[f"ratelimit:{key}"],
            args=[now, window_seconds, max_requests, member],
        )
        return RateLimitDecision(
            allowed=bool(allowed),
            remaining=max(max_requests - int(current), 0),
            retry_after_seconds=int(retry_after),
            limit=max_requests,
        )


class AsyncRedisClient(Protocol):
    async def script_load(self, script: str) -> str: ...

    async def evalsha(self, sha: str, keys: list[str], args: list[object]) -> tuple[int, int, int]: ...


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        backend: RateLimitBackend,
        *,
        window_seconds: int = 60,
        max_requests: int = 100,
    ) -> None:
        super().__init__(app)
        self._backend = backend
        self._window_seconds = window_seconds
        self._max_requests = max_requests

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_key = request.headers.get("x-api-key") or (request.client.host if request.client else "anonymous")
        decision = await self._backend.register_request(client_key, self._window_seconds, self._max_requests)

        if not decision.allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Reduce request frequency.",
                headers={
                    "Retry-After": str(decision.retry_after_seconds),
                    "X-RateLimit-Limit": str(decision.limit),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(decision.limit)
        response.headers["X-RateLimit-Remaining"] = str(decision.remaining)
        return response
