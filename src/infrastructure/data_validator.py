
from typing import List, Tuple
import polars as pl
from src.domain.models import TelemetryEvent, UserRole, EventType, TaskType
from datetime import datetime


class DataValidator:
    def __init__(self):
        pass

    def validate_and_clean_df(self, df: pl.DataFrame) -> Tuple[pl.DataFrame, List[str]]:
        """Validate and clean a Polars DataFrame of telemetry data, returning cleaned data and list of issues."""
        issues: List[str] = []
        
        # Make a copy to avoid modifying original
        cleaned_df = df.clone()
        
        # 1. Remove duplicates
        initial_count = len(cleaned_df)
        cleaned_df = cleaned_df.unique(subset=["event_id"])
        if len(cleaned_df) < initial_count:
            issues.append(f"Removed {initial_count - len(cleaned_df)} duplicate events")
        
        # 2. Validate and convert timestamps
        try:
            cleaned_df = cleaned_df.with_columns(
                pl.col("timestamp").str.to_datetime().alias("timestamp")
            )
        except Exception as e:
            issues.append(f"Failed to parse timestamps: {e}")
        
        # 3. Validate tokens_used is non-negative
        negative_tokens = cleaned_df.filter(pl.col("tokens_used") < 0)
        if len(negative_tokens) > 0:
            issues.append(f"Found {len(negative_tokens)} events with negative tokens_used; setting to 0")
            cleaned_df = cleaned_df.with_columns(
                pl.when(pl.col("tokens_used") < 0).then(0).otherwise(pl.col("tokens_used")).alias("tokens_used")
            )
        
        # 4. Validate session_duration_minutes is positive
        invalid_duration = cleaned_df.filter(pl.col("session_duration_minutes") <= 0)
        if len(invalid_duration) > 0:
            issues.append(f"Found {len(invalid_duration)} events with invalid session duration; removing")
            cleaned_df = cleaned_df.filter(pl.col("session_duration_minutes") > 0)
        
        # 5. Validate user_role is in allowed values
        allowed_roles = [role.value for role in UserRole]
        invalid_roles = cleaned_df.filter(~pl.col("user_role").is_in(allowed_roles))
        if len(invalid_roles) > 0:
            issues.append(f"Found {len(invalid_roles)} events with invalid user_role; removing")
            cleaned_df = cleaned_df.filter(pl.col("user_role").is_in(allowed_roles))
        
        # 6. Validate event_type is in allowed values
        allowed_event_types = [et.value for et in EventType]
        invalid_event_types = cleaned_df.filter(~pl.col("event_type").is_in(allowed_event_types))
        if len(invalid_event_types) > 0:
            issues.append(f"Found {len(invalid_event_types)} events with invalid event_type; removing")
            cleaned_df = cleaned_df.filter(pl.col("event_type").is_in(allowed_event_types))
        
        # 7. Validate task_type (if present) is in allowed values
        allowed_task_types = [tt.value for tt in TaskType]
        invalid_task_types = cleaned_df.filter(
            pl.col("task_type").is_not_null() & ~pl.col("task_type").is_in(allowed_task_types)
        )
        if len(invalid_task_types) > 0:
            issues.append(f"Found {len(invalid_task_types)} events with invalid task_type; setting to null")
            cleaned_df = cleaned_df.with_columns(
                pl.when(~pl.col("task_type").is_in(allowed_task_types)).then(None).otherwise(pl.col("task_type")).alias("task_type")
            )
        
        return cleaned_df, issues

    def parse_events_from_df(self, df: pl.DataFrame) -> Tuple[List[TelemetryEvent], List[str]]:
        """Parse cleaned DataFrame into valid TelemetryEvent objects, returning events and issues."""
        events: List[TelemetryEvent] = []
        issues: List[str] = []
        
        for row in df.iter_rows(named=True):
            try:
                event = TelemetryEvent(
                    event_id=row["event_id"],
                    session_id=row["session_id"],
                    user_id=row["user_id"],
                    user_role=UserRole(row["user_role"]),
                    event_type=EventType(row["event_type"]),
                    timestamp=row["timestamp"],
                    tokens_used=row["tokens_used"],
                    language=row.get("language"),
                    task_type=TaskType(row["task_type"]) if row.get("task_type") else None,
                    success=row["success"],
                    session_duration_minutes=row["session_duration_minutes"]
                )
                events.append(event)
            except Exception as e:
                issues.append(f"Failed to parse event {row.get('event_id', 'unknown')}: {e}")
        
        return events, issues
