
from typing import Any
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.infrastructure.duckdb_repository import DuckDBTelemetryRepository
from src.infrastructure.analytics_service import DuckDBAnalyticsService
from src.infrastructure.logger import configure_logging, get_logger
from src.application.use_cases import IngestTelemetryData

configure_logging()
logger = get_logger(__name__)

app = FastAPI(title="Claude Code Analytics API")

repository = DuckDBTelemetryRepository()
analytics_service = DuckDBAnalyticsService()
logger.info("API application initialized")


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check() -> dict[str, str]:
    logger.debug("Health check requested")
    return {"status": "ok"}


@app.get("/metrics/daily")
def get_daily_metrics() -> list[dict[str, Any]]:
    logger.info("Request received: /metrics/daily")
    df = analytics_service.get_daily_metrics()
    return df.to_dict(orient="records")  # type: ignore


@app.get("/metrics/events")
def get_event_distribution() -> list[dict[str, Any]]:
    logger.info("Request received: /metrics/events")
    df = analytics_service.get_event_distribution()
    return df.to_dict(orient="records")  # type: ignore


@app.get("/metrics/roles")
def get_user_role_distribution() -> list[dict[str, Any]]:
    logger.info("Request received: /metrics/roles")
    df = analytics_service.get_user_role_distribution()
    return df.to_dict(orient="records")  # type: ignore


@app.post("/ingest")
def ingest_data(
    jsonl_path: str = "output/telemetry_logs.jsonl",
    csv_path: str = "output/employees.csv",
) -> dict[str, Any]:
    logger.info("Request received: /ingest jsonl_path=%s csv_path=%s", jsonl_path, csv_path)
    use_case = IngestTelemetryData(repository)
    errors = use_case.execute(jsonl_path, csv_path)
    if errors:
        logger.warning("Ingestion finished with %d validation/loading errors", len(errors))
    else:
        logger.info("Ingestion finished successfully")
    return {"status": "ingested", "errors": errors}
