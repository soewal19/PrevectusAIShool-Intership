
# Claude Code Analytics Skill

## Purpose
This skill helps with analyzing Claude Code telemetry data, building dashboards, and deriving insights.

## Data Structure Knowledge
The telemetry dataset has the following fields:
- `session_id`: Unique session identifier
- `user_id`: Unique user identifier (anonymized)
- `user_role`: User role (developer, data_scientist, devops, student, product_manager)
- `event_id`: Unique event identifier
- `event_type`: Type of event (code_generation, code_completion, chat_interaction, file_edit, command_execution)
- `timestamp`: Event timestamp (ISO 8601)
- `tokens_used`: Number of tokens used for this event
- `language`: Programming language used (for code-related events)
- `task_type`: Type of task (refactoring, bug_fix, feature_implementation, etc.)
- `success`: Whether the event was successful
- `session_duration_minutes`: Total duration of the session in minutes

## Common Queries & Patterns
1. Daily active users
2. Event type distribution
3. Token usage trends
4. Language popularity
5. Task type analysis
6. User role behavior

## Tools to Use
- DuckDB: For fast analytical queries
- Streamlit: For building interactive dashboards
- Plotly: For visualizations
- Pandas: For data manipulation
