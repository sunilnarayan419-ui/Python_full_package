"""
10_WebSockets.py

Real-time WebSocket communication for scientific analysis job status, using
FastAPI's WebSocket support.

Architectural distinction from HTTP:
    HTTP:      request -> response (one-shot, stateless per call)
    WebSocket: persistent connection -> bidirectional messages, used here
               to push live progress updates for a long-running analysis
               job without the client polling an HTTP endpoint.

Demonstrates:
    - connection lifecycle (accept / receive / send / disconnect)
    - message validation (malformed client messages are rejected, not
      allowed to crash the connection handler)
    - a lightweight connection manager for broadcast to subscribers of a
      given job
    - graceful handling of WebSocketDisconnect
    - no blocking calls and no uncontrolled infinite loops -- the server
      only pushes updates as they occur, via asyncio.sleep pacing in the
      demo producer, not a busy loop
"""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ClientMessage(BaseModel):
    """The only inbound message shape this endpoint accepts: a
    subscription acknowledgment / keepalive ping. Anything else is
    rejected rather than trusted."""

    type: str


class ProgressUpdate(BaseModel):
    job_id: str
    status: JobStatus
    percent_complete: int


class ConnectionManager:
    """Tracks active WebSocket connections per analysis job so progress
    updates can be broadcast to every subscriber of that job without
    holding a single global list of sockets with no structure."""

    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, job_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections[job_id].add(websocket)
        logger.info("client subscribed job_id=%s active=%d", job_id, len(self._connections[job_id]))

    async def disconnect(self, job_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections[job_id].discard(websocket)
            if not self._connections[job_id]:
                del self._connections[job_id]
        logger.info("client unsubscribed job_id=%s", job_id)

    async def broadcast(self, job_id: str, update: ProgressUpdate) -> None:
        async with self._lock:
            subscribers = list(self._connections.get(job_id, ()))

        stale: list[WebSocket] = []
        for connection in subscribers:
            try:
                await connection.send_json(update.model_dump())
            except Exception:
                # A single broken subscriber must not stop delivery to
                # the others.
                stale.append(connection)

        if stale:
            async with self._lock:
                for connection in stale:
                    self._connections[job_id].discard(connection)


manager = ConnectionManager()


@dataclass(slots=True)
class AnalysisJobRunner:
    """Simulates a long-running computational-biology analysis job that
    reports progress. In production this would be driven by real work
    (e.g. a sequence alignment pipeline), with updates published as each
    stage genuinely completes."""

    job_id: str
    steps: list[str] = field(
        default_factory=lambda: ["preprocessing", "alignment", "variant_calling", "annotation"]
    )

    async def run(self, manager: ConnectionManager) -> None:
        total = len(self.steps)
        await manager.broadcast(
            self.job_id, ProgressUpdate(job_id=self.job_id, status=JobStatus.RUNNING, percent_complete=0)
        )
        for index, _step in enumerate(self.steps, start=1):
            await asyncio.sleep(0.5)  # stand-in for real, awaited work
            percent = round(index / total * 100)
            await manager.broadcast(
                self.job_id,
                ProgressUpdate(job_id=self.job_id, status=JobStatus.RUNNING, percent_complete=percent),
            )
        await manager.broadcast(
            self.job_id,
            ProgressUpdate(job_id=self.job_id, status=JobStatus.COMPLETED, percent_complete=100),
        )


app = FastAPI(title="Analysis Job Progress WebSocket API")


@app.websocket("/ws/analyses/{job_id}")
async def analysis_progress_socket(websocket: WebSocket, job_id: str) -> None:
    await manager.connect(job_id, websocket)
    try:
        while True:
            raw_message = await websocket.receive_json()
            try:
                message = ClientMessage.model_validate(raw_message)
            except ValidationError:
                await websocket.send_json({"error": "invalid_message", "detail": "unrecognized message shape"})
                continue

            if message.type == "ping":
                await websocket.send_json({"type": "pong"})
            else:
                await websocket.send_json({"error": "unsupported_message_type", "type": message.type})
    except WebSocketDisconnect:
        await manager.disconnect(job_id, websocket)
    except Exception:
        logger.exception("unexpected error on analysis websocket job_id=%s", job_id)
        await manager.disconnect(job_id, websocket)


@app.post("/analyses/{job_id}/simulate", status_code=202)
async def simulate_job(job_id: str) -> dict[str, str]:
    """Kicks off a background job whose progress is pushed to any client
    currently subscribed on /ws/analyses/{job_id}. Scheduled as a task so
    the HTTP request returns immediately (202 Accepted) rather than
    blocking on the full job duration."""
    runner = AnalysisJobRunner(job_id=job_id)
    asyncio.create_task(runner.run(manager))
    return {"job_id": job_id, "status": "started"}
