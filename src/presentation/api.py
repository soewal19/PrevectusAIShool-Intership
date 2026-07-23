
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from src.infrastructure.duckdb_repository import DuckDBTelemetryRepository
from src.infrastructure.analytics_service import DuckDBAnalyticsService
from src.infrastructure.insight_service import OpenAIInsightService
from src.infrastructure.logger import configure_logging, get_logger
from src.application.use_cases import IngestTelemetryData

load_dotenv()
configure_logging()
logger = get_logger(__name__)

app = FastAPI(title="Claude Code Analytics API")

repository = DuckDBTelemetryRepository()
analytics_service = DuckDBAnalyticsService()

# Initialize insight service (if API key is available)
insight_service = None
try:
    insight_service = OpenAIInsightService()
    logger.info("Insight service initialized successfully")
except Exception as e:
    logger.warning("Could not initialize insight service: %s", e)

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


@app.get("/insights/summary")
def get_executive_summary() -> dict[str, str]:
    logger.info("Request received: /insights/summary")
    if not insight_service:
        raise HTTPException(status_code=501, detail="Insight service not configured (check OPENAI_API_KEY)")
    
    # Collect all analytics data
    analytics_data = {
        "daily_metrics": analytics_service.get_daily_metrics().to_dict(orient="records") if not analytics_service.get_daily_metrics().empty else [],
        "event_distribution": analytics_service.get_event_distribution().to_dict(orient="records") if not analytics_service.get_event_distribution().empty else [],
        "user_role_distribution": analytics_service.get_user_role_distribution().to_dict(orient="records") if not analytics_service.get_user_role_distribution().empty else [],
        "model_usage": analytics_service.get_model_usage().to_dict(orient="records") if not analytics_service.get_model_usage().empty else [],
        "tool_usage": analytics_service.get_tool_usage().to_dict(orient="records") if not analytics_service.get_tool_usage().empty else [],
        "cost_by_practice": analytics_service.get_cost_by_practice().to_dict(orient="records") if not analytics_service.get_cost_by_practice().empty else [],
        "cache_usage": analytics_service.get_cache_usage().to_dict(orient="records") if not analytics_service.get_cache_usage().empty else [],
        "cache_efficiency": analytics_service.get_cache_efficiency().to_dict(orient="records") if not analytics_service.get_cache_efficiency().empty else []
    }
    
    summary = insight_service.generate_executive_summary(analytics_data)
    return {"summary": summary}


@app.get("/insights/anomalies")
def get_anomalies() -> list[dict[str, Any]]:
    logger.info("Request received: /insights/anomalies")
    if not insight_service:
        raise HTTPException(status_code=501, detail="Insight service not configured (check OPENAI_API_KEY)")
    
    analytics_data = {
        "daily_metrics": analytics_service.get_daily_metrics().to_dict(orient="records") if not analytics_service.get_daily_metrics().empty else [],
        "event_distribution": analytics_service.get_event_distribution().to_dict(orient="records") if not analytics_service.get_event_distribution().empty else [],
        "user_role_distribution": analytics_service.get_user_role_distribution().to_dict(orient="records") if not analytics_service.get_user_role_distribution().empty else [],
        "model_usage": analytics_service.get_model_usage().to_dict(orient="records") if not analytics_service.get_model_usage().empty else [],
        "tool_usage": analytics_service.get_tool_usage().to_dict(orient="records") if not analytics_service.get_tool_usage().empty else [],
        "cost_by_practice": analytics_service.get_cost_by_practice().to_dict(orient="records") if not analytics_service.get_cost_by_practice().empty else [],
        "cache_usage": analytics_service.get_cache_usage().to_dict(orient="records") if not analytics_service.get_cache_usage().empty else [],
        "cache_efficiency": analytics_service.get_cache_efficiency().to_dict(orient="records") if not analytics_service.get_cache_efficiency().empty else []
    }
    
    return insight_service.detect_anomalies(analytics_data)


@app.get("/insights/users")
def get_user_insights() -> list[dict[str, Any]]:
    logger.info("Request received: /insights/users")
    if not insight_service:
        raise HTTPException(status_code=501, detail="Insight service not configured (check OPENAI_API_KEY)")
    
    analytics_data = {
        "daily_metrics": analytics_service.get_daily_metrics().to_dict(orient="records") if not analytics_service.get_daily_metrics().empty else [],
        "event_distribution": analytics_service.get_event_distribution().to_dict(orient="records") if not analytics_service.get_event_distribution().empty else [],
        "user_role_distribution": analytics_service.get_user_role_distribution().to_dict(orient="records") if not analytics_service.get_user_role_distribution().empty else [],
        "model_usage": analytics_service.get_model_usage().to_dict(orient="records") if not analytics_service.get_model_usage().empty else [],
        "tool_usage": analytics_service.get_tool_usage().to_dict(orient="records") if not analytics_service.get_tool_usage().empty else [],
        "cost_by_practice": analytics_service.get_cost_by_practice().to_dict(orient="records") if not analytics_service.get_cost_by_practice().empty else [],
        "cache_usage": analytics_service.get_cache_usage().to_dict(orient="records") if not analytics_service.get_cache_usage().empty else [],
        "cache_efficiency": analytics_service.get_cache_efficiency().to_dict(orient="records") if not analytics_service.get_cache_efficiency().empty else [],
        "top_cache_users": analytics_service.get_top_cache_users().to_dict(orient="records") if not analytics_service.get_top_cache_users().empty else []
    }
    
    return insight_service.generate_user_insights(analytics_data)
