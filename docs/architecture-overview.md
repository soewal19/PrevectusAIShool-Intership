
# Architecture Overview: Claude Code Analytics Platform

## Introduction
This document provides a high-level overview of the architecture for the Claude Code Analytics Platform, complementing the C4 model diagrams.

## Core Architectural Principles
1. **Hexagonal Architecture (Ports & Adapters)**: Separates core business logic from external concerns
2. **Testability**: Easy to test core domain logic in isolation
3. **Maintainability**: Clear separation of concerns between layers
4. **Reproducibility**: Full Docker Compose setup for one-command deployment
5. **Type Safety**: Strict Pydantic v2 validation for all data models

## Architecture Layers

### 1. Domain Layer (src/domain/)
- **Purpose**: Contains core business logic, models, and interface definitions
- **Components**:
  - Domain models (TelemetryEvent, Employee, ClaudeEventType, etc.)
  - Port interfaces (AnalyticsService, TelemetryRepository)
  - No external dependencies!

### 2. Application Layer (src/application/)
- **Purpose**: Contains use cases that orchestrate domain objects
- **Components**:
  - UseCases (IngestTelemetryData)
  - Orchestrates data flow between domain and infrastructure

### 3. Infrastructure Layer (src/infrastructure/)
- **Purpose**: Implements adapters for external systems
- **Components**:
  - DuckDB Repository (implements TelemetryRepository)
  - DuckDB Analytics Service (implements AnalyticsService)
  - JSONL Ingestor (parses raw telemetry logs)
  - Data Validator (validates incoming data)

### 4. Presentation Layer (src/presentation/)
- **Purpose**: User-facing interfaces
- **Components**:
  - FastAPI Backend (REST API)
  - Streamlit Dashboard (interactive visualizations)

## Tech Stack
- **Programming Language**: Python 3.12
- **Architecture**: Hexagonal (Ports & Adapters)
- **API Framework**: FastAPI + Uvicorn
- **Data Storage**: DuckDB
- **Data Processing**: Polars, Pandas
- **Dashboard**: Streamlit + Plotly
- **Validation**: Pydantic v2
- **Containerization**: Docker + Docker Compose

## Data Flow
1. **Raw Data Ingestion**: telemetry_logs.jsonl + employees.csv
2. **Validation**: Data validated against Pydantic models
3. **Storage**: Processed data stored in DuckDB
4. **Analytics**: Analytics service runs queries on DuckDB
5. **Presentation**: Dashboard and API serve analytics to users

## Key Decisions
- **DuckDB over PostgreSQL/BigQuery**: File-based, fast for analytical queries, no server needed
- **Hexagonal Architecture**: Maintainability and testability
- **Streamlit over custom frontend**: Rapid development for data apps
- **Pydantic v2**: Strict type safety and validation
