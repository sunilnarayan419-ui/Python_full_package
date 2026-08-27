from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


class InvalidCursorError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class DatasetCursor:
    created_at: datetime
    dataset_id: UUID

    def encode(self) -> str:
        payload = {"created_at": self.created_at.isoformat(), "dataset_id": str(self.dataset_id)}
        raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("ascii")

    @classmethod
    def decode(cls, cursor: str) -> "DatasetCursor":
        try:
            raw = base64.urlsafe_b64decode(cursor.encode("ascii"))
            payload = json.loads(raw)
            return cls(created_at=datetime.fromisoformat(payload["created_at"]), dataset_id=UUID(payload["dataset_id"]))
        except (ValueError, KeyError, TypeError) as exc:
            raise InvalidCursorError("The provided pagination cursor is malformed or has expired.") from exc
