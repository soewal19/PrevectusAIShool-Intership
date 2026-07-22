
# Requirements

## Functional Requirements
1. **Data Ingestion**: Ingest telemetry data from CSV files
2. **Data Validation & Cleaning**: Validate schema, handle missing values, remove duplicates, normalize formats
3. **Analytics Layer**: Compute product-focused metrics (retention, engagement, token efficiency, session quality, user segmentation)
4. **Insight Generation**: Use AI to generate executive summaries, detect anomalies, cluster users
5. **API**: Expose analytics via REST API
6. **Dashboard**: Interactive, actionable dashboard that answers product questions
7. **AI Workflow**: Reproducible agent setup (skills, prompts, rules) committed to the repo

## Non-Functional Requirements
1. **Launchable with one command**: `docker compose up`
2. **Strict typing**: Use Pydantic v2 for all data models
3. **Validation**: Validate all incoming and outgoing data
4. **Maintainable architecture**: Follow Hexagonal (Ports & Adapters) architecture
5. **Testable**: Have unit tests for core components
6. **Well-documented**: README, architecture docs, AI setup docs
