
# Dataset Knowledge: Claude Code Telemetry

## Data Sources
1. **telemetry_logs.jsonl**: Claude Code telemetry batches with log events
2. **employees.csv**: Employee metadata (practice, level, location)

## Telemetry Event Types
- `claude_code.api_request`: API request to Claude models
- `claude_code.tool_decision`: Decision to use a tool
- `claude_code.tool_result`: Result from tool execution
- `claude_code.user_prompt`: User's prompt (redacted)
- `claude_code.api_error`: API error occurred

## Key Entities & Attributes
- **Session**: Unique session ID, timestamp
- **User**: User ID, email, engineering practice, seniority level, location
- **API Request**: Model used, input tokens, output tokens, cache read tokens, cache create tokens, cost, duration
- **Tool**: Tool name, success status, duration, tool result size
- **Cache**: Cache read tokens, cache create tokens (for analyzing efficiency)

## Typical Analytical Tasks
- **Token & Cost Analysis**: Total/avg tokens and cost, cost by model/practice
- **Usage Metrics**: DAU (daily active users), number of sessions, event frequency
- **Cache Analytics**: Cache efficiency (read/create ratio), cache usage trends
- **Tool Analysis**: Most used tools, tool success rates, avg tool durations
- **User Segmentation**: Usage patterns by practice, level, location
- **Trend Analysis**: How usage changes over time
- **Anomaly Detection**: Unusual patterns in cost or usage

## Data Rules
- Always preserve raw data
- Never overwrite original dataset files
- Always validate data with Pydantic models before processing

