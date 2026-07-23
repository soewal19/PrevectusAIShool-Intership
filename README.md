
# Claude Code Usage Analytics Platform

## Overview
An end-to-end analytics platform for processing and visualizing Claude Code telemetry data, built with AI-assisted development and following modern software engineering practices.

Key features:
- Hexagonal (Ports & Adapters) architecture for maintainability and testability
- AI Operating System (ai-agent/) with custom skills, rules, and agent team configuration
- Data ingestion, processing, and analytics using DuckDB and Polars
- Interactive dashboard with Streamlit and Plotly
- **AI-powered insights generation** (executive summaries, anomaly detection, user insights) using OpenAI
- FastAPI backend for programmatic access
- Docker Compose for easy deployment
- Comprehensive tests and quality checks
- **CI/CD pipeline** with GitHub Actions (lint, type check, test, Docker build, deploy)

## Tech Stack
- **Language**: Python 3.12
- **Architecture**: Hexagonal (Ports & Adapters)
- **Data Storage**: DuckDB
- **Data Processing**: Polars, Pandas
- **Backend API**: FastAPI + Uvicorn
- **Dashboard**: Streamlit + Plotly
- **Testing**: pytest
- **Code Quality**: ruff (linting), pyright (type checking)
- **Containerization**: Docker + Docker Compose
- **AI-Assisted Dev**: Custom "AI OS" with skills, prompts, and agent rules (see ai-agent/)

## Project Structure

```
.
├── .github/                # GitHub-specific configs
│   └── workflows/          # GitHub Actions CI/CD pipelines
├── ai-agent/                # AI Operating System (agent configuration)
│   ├── prompts/            # Agent prompts (architect, analyst, etc.)
│   ├── skills/             # Custom skills for the agent
│   ├── memory/             # Project memory and knowledge
│   ├── checklists/         # Checklists for reviews and completion
│   ├── specs/              # Specifications (architecture, analytics, dashboard)
│   ├── CLAUDE.md           # Claude Code instructions
│   ├── AGENTS.md           # Agent team configuration
│   ├── PRINCIPLES.md       # Engineering principles
│   ├── DECISIONS.md        # Decision rules
│   ├── QUALITY.md          # Quality standards
│   └── TASK.md             # Mission and goals
├── CI_CD/                  # CI/CD configuration &amp; scripts
│   ├── scripts/            # Helper scripts (lint, type check, test)
│   ├── github/             # GitHub Actions workflows
│   ├── ruff.toml           # Ruff linting config
│   ├── pyproject.toml      # Pyright &amp; Pytest config
│   └── README.md           # CI/CD documentation
├── data/                   # Data files (gitignored)
├── docs/                   # Documentation
│   ├── c4-model.md         # C4 architecture diagrams
│   ├── architecture-overview.md # Architecture overview
│   └── completion_report.md # Assignment completion report
├── src/
│   ├── domain/             # Domain layer (models, ports)
│   ├── application/        # Application layer (use cases)
│   ├── infrastructure/     # Infrastructure layer (adapters: DuckDB, etc.)
│   ├── presentation/       # Presentation layer (API, Dashboard)
│   └── scripts/            # Utility scripts (data generation)
├── tests/                  # Tests (pytest)
├── .env.example            # Example environment variables
├── .gitignore
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── setup.ps1               # Setup script (Windows)
└── README.md
```

## Setup Instructions (Windows)

### Option 1: Local Setup
1. **Run the setup script**:
   ```powershell
   .\setup.ps1
   ```

2. **Start the services**:
   - **API**:
     ```powershell
     .venv\Scripts\Activate.ps1
     uvicorn src.presentation.api:app --reload
     ```
   - **Dashboard**:
     ```powershell
     .venv\Scripts\Activate.ps1
     streamlit run src/presentation/dashboard.py
     ```

### Option 2: Docker Compose
1. **Build and start containers**:
   ```powershell
   docker-compose up --build
   ```
2. **Access the services**:
   - API: http://localhost:8000
   - Dashboard: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## Agent Configuration (ai-agent/)
The AI Operating System includes:
- **Agent Team**: Architect, Data Engineer, Analytics Engineer, Backend Engineer, Dashboard Engineer, QA Engineer, Technical Writer
- **Custom Skills**: Telemetry analysis, dashboard building, data quality, insight generation, architecture review
- **Knowledge Base**: Project memory, dataset information, specifications
- **Quality Checks**: Checklists for code reviews, completion criteria, and more
- **Engineering Principles**: Guidelines for clean, maintainable code

## Architecture
This solution follows **Hexagonal Architecture** (Ports & Adapters):
- **Domain Layer**: Core business logic, models, and port interfaces
- **Application Layer**: Use cases that orchestrate domain objects
- **Infrastructure Layer**: Adapters for external systems (DuckDB, etc.)
- **Presentation Layer**: API and Streamlit dashboard

## Quality Assurance
- **Type Checking**: `pyright`
- **Linting**: `ruff`
- **Testing**: `pytest`
- **Checklists**: Code review and completion checklists in ai-agent/checklists/

## Running Quality Checks

### Option 1: Individual Checks
```powershell
.venv\Scripts\Activate.ps1
# Type check
pyright
# Lint
ruff check
# Tests
pytest
```

### Option 2: All-in-One Script
```powershell
# Windows
CI_CD\scripts\run_all_checks.ps1

# Linux/macOS
chmod +x CI_CD/scripts/run_all_checks.sh
CI_CD/scripts/run_all_checks.sh
```

## CI/CD Pipeline
Full CI/CD pipeline configured with GitHub Actions:
- **CI**: Runs on push/pull request (lint, type check, test, Docker build)
- **CD**: Runs on release (build &amp; push Docker image)
- **PR Title Linter**: Validates Conventional Commits

See [CI_CD/README.md](CI_CD/README.md) for full documentation.

## Optional Enhancements
- Machine learning for predictive analytics and anomaly detection
- Real-time streaming data ingestion
- Advanced statistical analysis
- More API endpoints
- User authentication and authorization

