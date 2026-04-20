# Quickstart Guide: Schedule Scraper Development

**Feature**: Schedule Scraper and Display System
**Date**: 2026-04-07
**Audience**: Developers setting up local development environment

## Prerequisites

**Required Software**:
- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Python** 3.11+
- **Node.js** 18+ with npm or yarn
- **Git**

**Optional** (for non-Docker setup):
- PostgreSQL 14+

**Verify Installation**:
```bash
docker --version
docker-compose --version
python --version
node --version
git --version
```

## Quick Start (Docker Compose)

### 1. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd ugm_schedule

# Checkout feature branch
git checkout 001-schedule-scraper

# Copy environment template
cp .env.example .env

# Edit .env with your values (see Configuration section below)
```

### 2. Start Services

```bash
# Build and start all services (backend, frontend, database)
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

**Services**:
- Backend API: http://localhost:8000
- Frontend: http://localhost:5173
- PostgreSQL: localhost:5432

### 3. Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# (Optional) Load sample data
docker-compose exec backend python scripts/seed_data.py
```

### 4. Verify Setup

**Check Backend**:
```bash
curl http://localhost:8000/api/health
# Expected: {"status":"healthy","timestamp":"...","database":"connected"}
```

**Check Frontend**:
Open http://localhost:5173 in browser - should see schedule display

**Check API Docs**:
Open http://localhost:8000/docs - Swagger UI

### 5. Run Tests

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm run test

# E2E tests (requires services running)
docker-compose exec frontend npm run test:e2e
```

---

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Setup environment variables
cp ../.env.example ../.env
# Edit .env to configure DATABASE_URL, etc.

# Run migrations
alembic upgrade head

# (Optional) Load sample data
python scripts/seed_data.py

# Start development server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend now running** at http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env to set VITE_API_BASE_URL=http://localhost:8000

# Start development server
npm run dev
```

**Frontend now running** at http://localhost:5173

### Database Setup (PostgreSQL)

```bash
# Using psql
psql -U postgres

CREATE DATABASE ugm_schedule_dev;
CREATE USER ugm_schedule WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ugm_schedule_dev TO ugm_schedule;
\q
```

Update `.env`:
```
DATABASE_URL=postgresql://ugm_schedule:your_password@localhost:5432/ugm_schedule_dev
```

---

## Configuration

### Environment Variables

**`.env` file** (root directory):

```bash
# Database
DATABASE_URL=postgresql://ugm_schedule:password@postgres:5432/ugm_schedule_dev
DATABASE_ECHO=false  # Set to true for SQL query logging

# Backend API
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Scraper
SCRAPER_USER_AGENT=UGMScheduleScraper/1.0
SCRAPER_TIMEOUT=30
SCRAPER_SCHEDULE_TIME=02:00  # Daily scrape time (HH:MM)

# Frontend (create frontend/.env)
VITE_API_BASE_URL=http://localhost:8000
```

### Source Configuration

**`backend/src/config/sources.yaml`**:

```yaml
leagues:
  - name: "Ligues Récréatives Hiver 2025-2026"
    url: "https://montrealultimate.ca/fr_ca/e/ligues-recreatives-hiver-2025-2026"
    enabled: true

  - name: "Summer League 2026"
    url: "https://example.com/leagues/summer-2026"
    enabled: false  # Disabled example

# Add more leagues here
```

---

## Development Workflow

### Daily Development

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Make code changes (hot reload enabled for both frontend and backend)

# Run tests before committing
docker-compose exec backend pytest
docker-compose exec frontend npm run test

# Stop services
docker-compose down
```

### Database Migrations

```bash
# After changing SQLAlchemy models, create a migration
docker-compose exec backend alembic revision --autogenerate -m "Add field to Game model"

# Review the generated migration file in backend/src/database/migrations/versions/

# Apply migration
docker-compose exec backend alembic upgrade head

# Rollback if needed
docker-compose exec backend alembic downgrade -1
```

### Testing Scraper

```bash
# Trigger manual scrape (with backend running)
curl -X POST http://localhost:8000/api/admin/trigger-scrape \
  -H "Content-Type: application/json" \
  -d '{"league_id": 1}'

# Check scrape logs
curl http://localhost:8000/api/v1/scrape-logs | jq

# View games
curl http://localhost:8000/api/v1/games | jq
```

### Frontend Development

```bash
# Install new package
docker-compose exec frontend npm install <package-name>

# Run linter
docker-compose exec frontend npm run lint

# Run type checker (if TypeScript)
docker-compose exec frontend npm run type-check

# Build for production (test build)
docker-compose exec frontend npm run build
```

### Backend Development

```bash
# Install new package
docker-compose exec backend pip install <package-name>
docker-compose exec backend pip freeze > requirements.txt

# Run linter
docker-compose exec backend flake8 src/

# Run type checker
docker-compose exec backend mypy src/

# Format code
docker-compose exec backend black src/ tests/
```

---

## Testing

### Backend Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=src --cov-report=html

# Run specific test file
docker-compose exec backend pytest tests/unit/test_models.py

# Run tests matching pattern
docker-compose exec backend pytest -k "test_game"

# View coverage report
open backend/htmlcov/index.html
```

### Frontend Tests

```bash
# Run unit/component tests
docker-compose exec frontend npm run test

# Run with coverage
docker-compose exec frontend npm run test:coverage

# Run in watch mode
docker-compose exec frontend npm run test:watch

# Run E2E tests
docker-compose exec frontend npm run test:e2e

# View coverage report
open frontend/coverage/index.html
```

---

## Troubleshooting

### Database Connection Errors

**Error**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Ensure PostgreSQL container is running
docker-compose ps

# Check logs
docker-compose logs postgres

# Verify DATABASE_URL in .env matches service name:
DATABASE_URL=postgresql://ugm_schedule:password@postgres:5432/ugm_schedule_dev
#                                                   ^^^^^^^^ should be "postgres" (service name)
```

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Rebuild backend container
docker-compose up --build backend

# Or manually install dependencies
docker-compose exec backend pip install -r requirements-dev.txt
```

### Frontend Build Errors

**Error**: `VITE_API_BASE_URL is not defined`

**Solution**:
```bash
# Ensure frontend/.env exists
cp frontend/.env.example frontend/.env

# Verify VITE_API_BASE_URL is set
cat frontend/.env
```

### Scraper Failing

**Error**: Scraper logs show 404 or parsing errors

**Solution**:
```bash
# Manually test URL
curl -A "Mozilla/5.0" https://montrealultimate.ca/fr_ca/e/ligues-recreatives-hiver-2025-2026

# Check HTML structure matches scraper expectations
# Update scraper selectors in backend/src/services/scraper.py if needed

# Check sources.yaml for typos
cat backend/src/config/sources.yaml
```

### Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000  # On Linux/Mac
netstat -ano | findstr :8000  # On Windows

# Kill the process or change port in docker-compose.yml
```

---

## Useful Commands

```bash
# View all running containers
docker-compose ps

# Restart a specific service
docker-compose restart backend

# View logs for all services
docker-compose logs -f

# Execute command in container
docker-compose exec backend <command>

# Access database directly
docker-compose exec postgres psql -U ugm_schedule -d ugm_schedule_dev

# Clean up everything (including volumes)
docker-compose down -v

# Rebuild specific service
docker-compose up -d --build backend

# Check API endpoints
curl http://localhost:8000/docs  # Swagger UI URL
```

---

## Next Steps

After successfully setting up the environment:

1. **Read the specification**: `specs/001-schedule-scraper/spec.md`
2. **Review data model**: `specs/001-schedule-scraper/data-model.md`
3. **Check API contracts**: `specs/001-schedule-scraper/contracts/api-endpoints.md`
4. **Start implementing**: Follow TDD workflow (write tests first!)
5. **Run tests frequently**: `pytest` (backend), `npm test` (frontend)

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Vue 3 Documentation**: https://vuejs.org/guide/introduction.html
- **Pinia Documentation**: https://pinia.vuejs.org/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Pytest Documentation**: https://docs.pytest.org/
- **Vitest Documentation**: https://vitest.dev/

---

## Success Checklist

- [ ] All services start without errors
- [ ] Database migrations run successfully
- [ ] Backend health check returns `200 OK`
- [ ] Frontend loads at http://localhost:5173
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Backend tests pass (`pytest`)
- [ ] Frontend tests pass (`npm test`)
- [ ] Manual scrape trigger works
- [ ] Games display in frontend UI
- [ ] Filters and search work in frontend

If all items are checked, you're ready to start development!
