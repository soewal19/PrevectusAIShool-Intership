
# Project Memory: Claude Code Analytics Platform

## Core Vision
Build an AI-native analytics platform for Claude Code telemetry that generates actionable product insights, not just charts.

## Tech Stack
- **Programming Language**: Python 3.12
- **Architecture**: Hexagonal (Ports & Adapters)
- **API Framework**: FastAPI + Uvicorn
- **Data Storage**: DuckDB
- **Data Processing**: Polars, Pandas
- **Dashboard**: Streamlit + Plotly
- **Validation**: Pydantic v2
- **Testing**: pytest
- **Code Quality**: ruff (linting), pyright (type checking)
- **Containerization**: Docker + Docker Compose

## Project Structure
```
/
├── ai-agent/           # AI Operating System (prompts, skills, memory)
├── src/
│   ├── domain/         # Domain models and ports
│   ├── application/    # Use cases
│   ├── infrastructure/ # Adapters (DuckDB, ingestion)
│   └── presentation/   # API and Dashboard
├── data/               # DuckDB database
├── output/             # Generated telemetry data
├── tests/              # pytest tests
├── docker-compose.yml
└── README.md
```

## Key Components
1. **Data Ingestion**: Ingest JSONL telemetry logs + CSV employee data
2. **Analytics Service**: Compute metrics (daily active users, token efficiency, cost by practice, etc.)
3. **Dashboard**: Interactive Streamlit dashboard for visualizing insights
4. **API**: FastAPI endpoints for programmatic access to analytics

## Critical Principles
- Always launchable with one command: `docker-compose up`
- Strict typing with Pydantic v2 for all data models
- Hexagonal architecture for maintainability
- Reproducible AI workflow with committed agent setup

