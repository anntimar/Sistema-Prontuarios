from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import shutil
from pathlib import Path
from threading import RLock
from typing import Any
from uuid import uuid4


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SEED_PATH = DATA_DIR / "local_seed.json"


@dataclass
class LocalResponse:
    data: list[dict[str, Any]]


class LocalJsonClient:
    def __init__(self, *, data_path: Path, storage_path: Path):
        self.data_path = data_path
        self.storage_path = storage_path
        self._lock = RLock()
        self._ensure_data_file()

    def table(self, table_name: str) -> "LocalQuery":
        return LocalQuery(self, table_name)

    @property
    def storage(self) -> "LocalStorage":
        return LocalStorage(self.storage_path)

    def _ensure_data_file(self) -> None:
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        if not self.data_path.exists():
            shutil.copyfile(SEED_PATH, self.data_path)

    def _read(self) -> dict[str, list[dict[str, Any]]]:
        self._ensure_data_file()
        with self.data_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write(self, data: dict[str, list[dict[str, Any]]]) -> None:
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with self.data_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")


class LocalQuery:
    def __init__(self, client: LocalJsonClient, table_name: str):
        self.client = client
        self.table_name = table_name
        self._columns: list[str] | None = None
        self._filters: list[tuple[str, str, Any]] = []
        self._order_column: str | None = None
        self._order_desc = False
        self._range: tuple[int, int] | None = None
        self._operation = "select"
        self._payload: dict[str, Any] | list[dict[str, Any]] | None = None

    def select(self, columns: str) -> "LocalQuery":
        self._columns = None if columns == "*" else [item.strip() for item in columns.split(",")]
        return self

    def eq(self, column: str, value: Any) -> "LocalQuery":
        self._filters.append(("eq", column, value))
        return self

    def in_(self, column: str, values: list[Any]) -> "LocalQuery":
        self._filters.append(("in", column, list(values)))
        return self

    def ilike(self, column: str, pattern: str) -> "LocalQuery":
        self._filters.append(("ilike", column, pattern))
        return self

    def gte(self, column: str, value: Any) -> "LocalQuery":
        self._filters.append(("gte", column, value))
        return self

    def lte(self, column: str, value: Any) -> "LocalQuery":
        self._filters.append(("lte", column, value))
        return self

    def order(self, column: str, desc: bool = False) -> "LocalQuery":
        self._order_column = column
        self._order_desc = desc
        return self

    def range(self, start: int, end: int) -> "LocalQuery":
        self._range = (start, end)
        return self

    def insert(self, payload: dict[str, Any] | list[dict[str, Any]]) -> "LocalQuery":
        self._operation = "insert"
        self._payload = payload
        return self

    def update(self, payload: dict[str, Any]) -> "LocalQuery":
        self._operation = "update"
        self._payload = payload
        return self

    def delete(self) -> "LocalQuery":
        self._operation = "delete"
        return self

    def execute(self) -> LocalResponse:
        with self.client._lock:
            data = self.client._read()
            table = data.setdefault(self.table_name, [])

            if self._operation == "insert":
                rows = self._insert(table)
                self.client._write(data)
                return LocalResponse(self._project(rows))

            if self._operation == "update":
                rows = self._update(table)
                self.client._write(data)
                return LocalResponse(self._project(rows))

            if self._operation == "delete":
                rows = self._delete(table)
                self.client._write(data)
                return LocalResponse(self._project(rows))

            return LocalResponse(self._project(self._apply_read(table)))

    def _insert(self, table: list[dict[str, Any]]) -> list[dict[str, Any]]:
        payload = self._payload if isinstance(self._payload, list) else [self._payload]
        now = _now()
        rows = []
        for item in payload:
            row = deepcopy(item or {})
            row.setdefault("id", str(uuid4()))
            row.setdefault("created_at", now)
            if self.table_name in TABLES_WITH_UPDATED_AT:
                row.setdefault("updated_at", now)
            table.append(row)
            rows.append(deepcopy(row))
        return rows

    def _update(self, table: list[dict[str, Any]]) -> list[dict[str, Any]]:
        payload = deepcopy(self._payload or {})
        if self.table_name in TABLES_WITH_UPDATED_AT:
            payload["updated_at"] = _now()
        rows = []
        for row in table:
            if self._matches(row):
                row.update(payload)
                rows.append(deepcopy(row))
        return rows

    def _delete(self, table: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows = []
        remaining = []
        for row in table:
            if self._matches(row):
                rows.append(deepcopy(row))
            else:
                remaining.append(row)
        table[:] = remaining
        return rows

    def _apply_read(self, table: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows = [deepcopy(row) for row in table if self._matches(row)]
        if self._order_column:
            rows.sort(
                key=lambda row: "" if row.get(self._order_column) is None else str(row.get(self._order_column)),
                reverse=self._order_desc,
            )
        if self._range:
            start, end = self._range
            rows = rows[start : end + 1]
        return rows

    def _matches(self, row: dict[str, Any]) -> bool:
        for operation, column, expected in self._filters:
            actual = row.get(column)
            if operation == "eq" and actual != expected:
                return False
            if operation == "in" and actual not in expected:
                return False
            if operation == "ilike":
                needle = str(expected).strip("%").lower()
                if needle not in str(actual or "").lower():
                    return False
            if operation == "gte" and _comparable(actual) < _comparable(expected):
                return False
            if operation == "lte" and _comparable(actual) > _comparable(expected):
                return False
        return True

    def _project(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if self._columns is None:
            return rows
        return [
            {column: row.get(column) for column in self._columns if column in row}
            for row in rows
        ]


class LocalStorage:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path

    def from_(self, bucket: str) -> "LocalBucket":
        return LocalBucket(self.storage_path, bucket)


class LocalBucket:
    def __init__(self, storage_path: Path, bucket: str):
        self.bucket_path = storage_path / bucket
        self.bucket = bucket

    def upload(self, storage_path: str, content: bytes, options: dict[str, Any] | None = None) -> dict[str, Any]:
        target = self.bucket_path / storage_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and options and options.get("x-upsert") == "false":
            raise FileExistsError(storage_path)
        target.write_bytes(content)
        return {"path": storage_path}

    def remove(self, paths: list[str]) -> list[dict[str, str]]:
        removed = []
        for storage_path in paths:
            target = self.bucket_path / storage_path
            if target.exists():
                target.unlink()
                removed.append({"name": storage_path})
        return removed

    def create_signed_url(
        self,
        storage_path: str,
        expires_in: int,
        options: dict[str, Any] | None = None,
    ) -> dict[str, str]:
        return {
            "signedUrl": f"http://127.0.0.1:8000/local-storage/{self.bucket}/{storage_path}",
        }


TABLES_WITH_UPDATED_AT = {
    "appointments",
    "clinical_attachments",
    "medications",
    "pacientes",
    "users",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _comparable(value: Any) -> str:
    if value is None:
        return ""
    return str(value)
