
import duckdb
from typing import List, Tuple
from src.domain.models import TelemetryEvent, Employee
from src.domain.ports import TelemetryRepository
from src.infrastructure.jsonl_ingestor import JSONLIngestor
import pandas as pd


class DuckDBTelemetryRepository(TelemetryRepository):
    def __init__(self, db_path: str = "data/claude_analytics.duckdb"):
        self.db_path = db_path
        self.ingestor = JSONLIngestor()
        self._init_db()

    def _init_db(self):
        with duckdb.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_events (
                    event_id VARCHAR PRIMARY KEY,
                    event_type VARCHAR,
                    session_id VARCHAR,
                    user_id VARCHAR,
                    user_email VARCHAR,
                    user_practice VARCHAR,
                    timestamp VARCHAR,
                    model VARCHAR,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    cache_read_tokens INTEGER,
                    cache_creation_tokens INTEGER,
                    cost_usd DOUBLE,
                    duration_ms INTEGER,
                    tool_name VARCHAR,
                    decision VARCHAR,
                    success BOOLEAN,
                    prompt_length INTEGER,
                    terminal_type VARCHAR,
                    service_version VARCHAR,
                    os_type VARCHAR
                );
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    email VARCHAR PRIMARY KEY,
                    full_name VARCHAR,
                    practice VARCHAR,
                    level VARCHAR,
                    location VARCHAR
                );
            """)

    def save_events(self, events: List[TelemetryEvent]):
        if not events:
            return

        rows = []
        for i, event in enumerate(events):
            event_id = f"evt_{i}_{event.attributes.get('event.timestamp', '')}"
            attrs = event.attributes
            row = {
                "event_id": event_id,
                "event_type": event.body.value if event.body else None,
                "session_id": attrs.get("session.id"),
                "user_id": attrs.get("user.id"),
                "user_email": attrs.get("user.email"),
                "user_practice": event.resource.user_practice.value if hasattr(event.resource, 'user_practice') and event.resource.user_practice else None,
                "timestamp": attrs.get("event.timestamp"),
                "model": attrs.get("model"),
                "input_tokens": int(attrs["input_tokens"]) if attrs.get("input_tokens") else None,
                "output_tokens": int(attrs["output_tokens"]) if attrs.get("output_tokens") else None,
                "cache_read_tokens": int(attrs["cache_read_tokens"]) if attrs.get("cache_read_tokens") else None,
                "cache_creation_tokens": int(attrs["cache_creation_tokens"]) if attrs.get("cache_creation_tokens") else None,
                "cost_usd": float(attrs["cost_usd"]) if attrs.get("cost_usd") else None,
                "duration_ms": int(attrs["duration_ms"]) if attrs.get("duration_ms") else None,
                "tool_name": attrs.get("tool_name"),
                "decision": attrs.get("decision"),
                "success": attrs.get("success").lower() == "true" if attrs.get("success") else None,
                "prompt_length": int(attrs["prompt_length"]) if attrs.get("prompt_length") else None,
                "terminal_type": attrs.get("terminal.type"),
                "service_version": event.resource.service_version if hasattr(event.resource, 'service_version') else None,
                "os_type": event.resource.os_type if hasattr(event.resource, 'os_type') else None,
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        with duckdb.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO telemetry_events SELECT * FROM df")

    def save_employees(self, employees: List[Employee]):
        if not employees:
            return

        rows = []
        for emp in employees:
            row = {
                "email": emp.email,
                "full_name": emp.full_name,
                "practice": emp.practice.value if hasattr(emp, 'practice') and emp.practice else None,
                "level": emp.level.value if hasattr(emp, 'level') and emp.level else None,
                "location": emp.location
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        with duckdb.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO employees SELECT * FROM df")

    def ingest_from_files(self, jsonl_path: str, csv_path: str) -> List[str]:
        events, employees, errors = self.ingestor.ingest_all(jsonl_path, csv_path)
        self.save_events(events)
        self.save_employees(employees)
        return errors

    def get_all_events(self) -> List[TelemetryEvent]:
        # For now, just return an empty list since we don't need to reconstruct full events
        with duckdb.connect(self.db_path) as conn:
            conn.execute("SELECT * FROM telemetry_events")
        return []
