
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from src.domain.models import TelemetryEvent, UserRole, EventType, TaskType


def generate_sample_data(num_sessions=1000, output_path="data/sample_telemetry.csv"):
    """Generate sample Claude Code telemetry data using Pydantic models for validation."""
    
    user_roles = list(UserRole)
    event_types = list(EventType)
    languages = ["python", "javascript", "typescript", "java", "go", "rust", "c++", "ruby"]
    task_types = list(TaskType)
    
    data = []
    base_time = datetime.now() - timedelta(days=30)
    
    for session_idx in range(num_sessions):
        user_id = f"user_{random.randint(1000, 9999):04d}"
        user_role = random.choice(user_roles)
        session_start = base_time + timedelta(days=random.randint(0, 29), hours=random.randint(0, 23))
        session_duration = random.uniform(5, 180)
        session_id = f"session_{session_idx:06d}"
        
        num_events = random.randint(1, 50)
        for event_idx in range(num_events):
            event_time = session_start + timedelta(minutes=random.uniform(0, session_duration))
            event_type = random.choice(event_types)
            
            tokens_used = random.randint(10, 5000) if event_type in [EventType.CODE_GENERATION, EventType.CHAT_INTERACTION] else 0
            language = random.choice(languages) if event_type in [EventType.CODE_GENERATION, EventType.CODE_COMPLETION, EventType.FILE_EDIT] else None
            task_type = random.choice(task_types) if event_type == EventType.CODE_GENERATION else None
            success = random.random() > 0.1
            
            # Validate event with Pydantic before adding to data
            event = TelemetryEvent(
                event_id=f"event_{session_idx:06d}_{event_idx:03d}",
                session_id=session_id,
                user_id=user_id,
                user_role=user_role,
                event_type=event_type,
                timestamp=event_time,
                tokens_used=tokens_used,
                language=language,
                task_type=task_type,
                success=success,
                session_duration_minutes=session_duration
            )
            
            data.append(event.model_dump(mode="json"))
    
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Sample data generated: {output_path}")
    print(f"Total events: {len(df)}")
    print(f"Total sessions: {df['session_id'].nunique()}")
    return df


if __name__ == "__main__":
    generate_sample_data()

