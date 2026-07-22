
# Architecture Specification

## Hexagonal Architecture

Ports:
- Data Ingestion Port
- Analytics Query Port
- Dashboard Port

Adapters:
- CSV Ingestion Adapter
- DuckDB Storage Adapter
- Streamlit Dashboard Adapter

## Folder Structure

```
src/
├── domain/           # Domain models and logic
├── application/      # Use cases
├── infrastructure/   # Adapters (storage, etc.)
└── presentation/     # Dashboard
```

