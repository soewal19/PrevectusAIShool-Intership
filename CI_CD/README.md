
# CI/CD Pipeline: Claude Code Analytics Platform

This directory contains the CI/CD configuration following best DevOps &amp; MLOps practices.

---

## Table of Contents
1. [Structure](#structure)
2. [Local Checks](#local-checks)
3. [GitHub Actions](#github-actions)
4. [Deployment](#deployment)
5. [Best Practices](#best-practices)

---

## Structure
```
CI_CD/
├── scripts/                # Helper scripts for quality checks
│   ├── run_all_checks.ps1 # Windows: Run all checks (lint, typecheck, test)
│   ├── run_all_checks.sh   # Linux: Run all checks
│   ├── run_linting.ps1     # Windows: Ruff linting
│   ├── run_linting.sh      # Linux: Ruff linting
│   ├── run_tests.ps1       # Windows: Pytest
│   ├── run_tests.sh        # Linux: Pytest
│   ├── run_typecheck.ps1   # Windows: Pyright
│   └── run_typecheck.sh    # Linux: Pyright
├── github/
│   └── workflows/
│       ├── ci.yml          # Continuous Integration (PR, Push)
│       ├── cd.yml          # Continuous Deployment (Releases)
│       └── lint-pr-title.yml # Lint PR titles (Conventional Commits)
├── pyproject.toml          # Configuration for Pyright, Pytest
├── ruff.toml               # Configuration for Ruff
└── README.md               # This file
```

---

## Local Checks

### Windows (PowerShell)
```powershell
# Run all checks
CI_CD\scripts\run_all_checks.ps1

# Run individual checks
CI_CD\scripts\run_linting.ps1
CI_CD\scripts\run_typecheck.ps1
CI_CD\scripts\run_tests.ps1
```

### Linux/macOS (Bash)
```bash
# Make scripts executable
chmod +x CI_CD/scripts/*.sh

# Run all checks
CI_CD/scripts/run_all_checks.sh

# Run individual checks
CI_CD/scripts/run_linting.sh
CI_CD/scripts/run_typecheck.sh
CI_CD/scripts/run_tests.sh
```

---

## GitHub Actions

### Setup
To use GitHub Actions workflows, copy them to `.github/workflows/`:

```bash
# Copy workflows to .github/workflows
mkdir -p .github/workflows
cp CI_CD/github/workflows/*.yml .github/workflows/
```

### Workflows
1. **`ci.yml`**: Runs on every push &amp; PR:
   - Linting (Ruff)
   - Type checking (Pyright)
   - Tests (Pytest)
   - Docker build
   - Optional: Code coverage

2. **`cd.yml`**: Runs on new release:
   - Build &amp; push Docker image to Docker Hub
   - Optional: Deploy to your server

3. **`lint-pr-title.yml`**: Validates PR titles follow Conventional Commits

### Secrets
Add these secrets in your GitHub repo settings (`Settings &gt; Secrets and Variables &gt; Actions &gt; New repository secret`):
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password/token
- Optional (for deployment): `SERVER_HOST`, `SERVER_USER`, `SSH_PRIVATE_KEY`

---

## Deployment

### Conventional Commits
Follow Conventional Commits for PR titles:
```
feat: add new feature
fix: fix bug
docs: update documentation
style: format code
refactor: refactor code
perf: improve performance
test: add test
build: update build system/deps
ci: update CI/CD
chore: other changes
revert: revert commit
```

### Release Process
1. Create a new release on GitHub:
   - Go to `Releases &gt; Draft a new release`
   - Tag version: `v1.0.0` (semantic versioning)
   - Click `Publish release`
2. CD pipeline automatically builds &amp; pushes Docker image

### Deploying
Edit `CI_CD/github/workflows/cd.yml` to add your deployment steps (commented in the file).

---

## Best Practices Followed

### DevOps Best Practices
- **GitOps**: All pipeline config in Git
- **Infrastructure as Code**: Docker &amp; Docker Compose
- **Versioning**: Semantic versioning for releases
- **Automated Checks**: Lint, type check, test on every PR/push
- **Caching**: Dependencies &amp; Docker layers in CI
- **Conventional Commits**: Standard commit/PR messages

### MLOps Best Practices
- **Reproducibility**: Docker ensures environment consistency
- **Validation**: Strict Pydantic v2 data validation
- **Test Coverage**: Pytest + optional Codecov integration
- **Continuous Training**: Structure ready for model retraining pipeline (future)
- **Monitoring**: Dashboard for continuous monitoring of usage

---

## Useful Links
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [Pyright Type Checker](https://microsoft.github.io/pyright/)
- [Pytest](https://docs.pytest.org/)
- [Docker Hub](https://hub.docker.com/)

