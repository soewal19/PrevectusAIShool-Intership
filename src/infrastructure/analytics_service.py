
import duckdb
from src.domain.ports import AnalyticsService
import pandas as pd


class DuckDBAnalyticsService(AnalyticsService):
    def __init__(self, db_path: str = "data/claude_analytics.duckdb"):
        self.db_path = db_path

    def get_daily_metrics(self) -> pd.DataFrame:
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    DATE_TRUNC('day', STRPTIME(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')) AS date,
                    COUNT(DISTINCT user_id) AS active_users,
                    COUNT(DISTINCT session_id) AS sessions,
                    COUNT(*) AS total_events,
                    SUM(input_tokens + output_tokens) AS total_tokens,
                    SUM(cost_usd) AS total_cost_usd
                FROM telemetry_events
                WHERE timestamp IS NOT NULL
                GROUP BY date
                ORDER BY date;
            """).df()

    def get_event_distribution(self) -> pd.DataFrame:
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    event_type,
                    COUNT(*) AS count
                FROM telemetry_events
                WHERE event_type IS NOT NULL
                GROUP BY event_type
                ORDER BY count DESC;
            """).df()

    def get_user_role_distribution(self) -> pd.DataFrame:
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    user_practice AS practice,
                    COUNT(DISTINCT user_id) AS users
                FROM telemetry_events
                WHERE user_practice IS NOT NULL
                GROUP BY user_practice
                ORDER BY users DESC;
            """).df()

    def get_language_distribution(self) -> pd.DataFrame:
        # Since we don't have language data in real telemetry, return empty
        return pd.DataFrame([{"language": "N/A", "count": 0}])

    def get_task_type_distribution(self) -> pd.DataFrame:
        # Since we don't have task type data in real telemetry, return empty
        return pd.DataFrame([{"task_type": "N/A", "count": 0, "avg_tokens": 0}])

    def get_model_usage(self) -> pd.DataFrame:
        """Get model usage by events, tokens, cost"""
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    model,
                    COUNT(*) AS event_count,
                    SUM(input_tokens + output_tokens) AS total_tokens,
                    SUM(cost_usd) AS total_cost,
                    AVG(cost_usd) AS avg_cost_per_request
                FROM telemetry_events
                WHERE model IS NOT NULL
                GROUP BY model
                ORDER BY total_cost DESC;
            """).df()

    def get_tool_usage(self) -> pd.DataFrame:
        """Get most used tools"""
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    tool_name,
                    COUNT(*) AS count,
                    SUM(CASE WHEN success THEN 1 ELSE 0 END) AS success_count,
                    AVG(duration_ms) AS avg_duration_ms
                FROM telemetry_events
                WHERE tool_name IS NOT NULL
                GROUP BY tool_name
                ORDER BY count DESC;
            """).df()

    def get_cost_by_practice(self) -> pd.DataFrame:
        """Get cost by engineering practice"""
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    user_practice AS practice,
                    COUNT(DISTINCT user_id) AS users,
                    SUM(cost_usd) AS total_cost,
                    AVG(cost_usd) AS avg_cost_per_user
                FROM telemetry_events
                WHERE user_practice IS NOT NULL AND cost_usd IS NOT NULL
                GROUP BY user_practice
                ORDER BY total_cost DESC;
            """).df()

    def get_cache_usage(self) -> pd.DataFrame:
        """Get cache read/write statistics"""
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    SUM(cache_read_tokens) AS total_cache_read,
                    SUM(cache_creation_tokens) AS total_cache_create,
                    AVG(cache_read_tokens) AS avg_cache_read,
                    AVG(cache_creation_tokens) AS avg_cache_create
                FROM telemetry_events
                WHERE model IS NOT NULL;
            """).df()
    
    def get_cache_efficiency(self) -> pd.DataFrame:
        """Get cache efficiency metrics (read vs create ratio)"""
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    SUM(cache_read_tokens) AS total_cache_read,
                    SUM(cache_creation_tokens) AS total_cache_create,
                    CASE 
                        WHEN SUM(cache_creation_tokens) > 0 
                        THEN SUM(cache_read_tokens) / SUM(cache_creation_tokens) 
                        ELSE 0 
                    END AS cache_read_to_create_ratio,
                    COUNT(*) AS total_api_requests,
                    SUM(CASE WHEN cache_read_tokens > 0 THEN 1 ELSE 0 END) AS requests_with_cache_read,
                    SUM(CASE WHEN cache_creation_tokens > 0 THEN 1 ELSE 0 END) AS requests_with_cache_create
                FROM telemetry_events
                WHERE model IS NOT NULL;
            """).df()
    
    def get_top_cache_users(self, limit: int = 10) -> pd.DataFrame:
        """Get top users by cache usage"""
        with duckdb.connect(self.db_path) as conn:
            return conn.execute(f"""
                SELECT
                    user_id,
                    user_email,
                    user_practice,
                    SUM(cache_read_tokens) AS total_cache_read,
                    SUM(cache_creation_tokens) AS total_cache_create,
                    SUM(cache_read_tokens + cache_creation_tokens) AS total_cache_usage,
                    CASE 
                        WHEN SUM(cache_creation_tokens) > 0 
                        THEN SUM(cache_read_tokens) / SUM(cache_creation_tokens) 
                        ELSE 0 
                    END AS cache_efficiency_ratio
                FROM telemetry_events
                WHERE model IS NOT NULL
                GROUP BY user_id, user_email, user_practice
                ORDER BY total_cache_usage DESC
                LIMIT {limit};
            """).df()
    
    def get_cache_by_model(self) -> pd.DataFrame:
        """Get cache usage statistics by model"""
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    model,
                    SUM(cache_read_tokens) AS total_cache_read,
                    SUM(cache_creation_tokens) AS total_cache_create,
                    AVG(cache_read_tokens) AS avg_cache_read,
                    AVG(cache_creation_tokens) AS avg_cache_create,
                    CASE 
                        WHEN SUM(cache_creation_tokens) > 0 
                        THEN SUM(cache_read_tokens) / SUM(cache_creation_tokens) 
                        ELSE 0 
                    END AS cache_read_to_create_ratio,
                    COUNT(*) AS total_requests
                FROM telemetry_events
                WHERE model IS NOT NULL
                GROUP BY model
                ORDER BY total_cache_read DESC;
            """).df()
    
    def get_daily_cache_metrics(self) -> pd.DataFrame:
        """Get daily cache metrics over time"""
        with duckdb.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT
                    DATE_TRUNC('day', STRPTIME(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')) AS date,
                    SUM(cache_read_tokens) AS total_cache_read,
                    SUM(cache_creation_tokens) AS total_cache_create,
                    AVG(cache_read_tokens) AS avg_cache_read,
                    AVG(cache_creation_tokens) AS avg_cache_create,
                    CASE 
                        WHEN SUM(cache_creation_tokens) > 0 
                        THEN SUM(cache_read_tokens) / SUM(cache_creation_tokens) 
                        ELSE 0 
                    END AS daily_cache_efficiency
                FROM telemetry_events
                WHERE model IS NOT NULL AND timestamp IS NOT NULL
                GROUP BY date
                ORDER BY date;
            """).df()
