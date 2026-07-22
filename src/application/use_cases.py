
from typing import List, Tuple
from src.domain.models import TelemetryEvent
from src.domain.ports import TelemetryRepository


class IngestTelemetryData:
    def __init__(self, repository: TelemetryRepository):
        self.repository = repository

    def execute(self, jsonl_path: str, csv_path: str) -> List[str]:
        """Ingest telemetry data from JSONL and CSV, validate, clean, and save to storage. Returns issues."""
        # Check if repository has ingest_from_files (for DuckDB repo specifically)
        if hasattr(self.repository, "ingest_from_files"):
            return self.repository.ingest_from_files(jsonl_path, csv_path)  # type: ignore
        else:
            raise NotImplementedError("Repository does not support ingestion from these files")
