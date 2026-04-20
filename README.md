# UGM Schedule Display System

A modern web application that displays sports league schedules from TopScore API in a filterable, searchable interface.

## Features

- 📅 **Schedule Display**: View upcoming games and past results with modern, responsive UI
- 🔍 **Advanced Filtering**: Filter by league, team, field/location, date range, and status
- 🔎 **Real-time Search**: Search for games as you type
- 🔄 **TopScore Integration**: Fetch schedule data from TopScore API
- ⚙️ **Automatic Sync**: Sync data from TopScore on-demand or on a schedule

## Tech Stack

**Frontend**:
- Vue.js 3 with Composition API
- TypeScript
- Pinia (state management)
- Tailwind CSS
- Vite

**Backend**:
- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- TopScore API Client
- APScheduler (task scheduling)

## Quick Start

### Prerequisites

- Docker 20.10+ and Docker Compose 2.0+
- TopScore API credentials (Client ID, Client Secret, CSRF Token)

### Setup

1. **Clone and start services**:
   ```bash
   git clone <repository-url>
   cd ugm_schedule
   
   # Copy environment template
   cp .env.example .env
   
   # Edit .env and add your TopScore credentials:
   # TOPSCORE_CLIENT_ID=your_client_id
   # TOPSCORE_CLIENT_SECRET=your_client_secret
   # TOPSCORE_CSRF_TOKEN=your_csrf_token
   
   # Start all services
   docker-compose up --build
   ```

2. **Run database migrations**:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

3. **Sync data from TopScore**:
   ```bash
   docker-compose exec backend python -m src.cli.sync_topscore
   ```

**Services**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## TopScore Integration

This application uses the TopScore API to fetch schedule data. See [backend/TOPSCORE_SYNC.md](backend/TOPSCORE_SYNC.md) for detailed setup and usage instructions.

### Getting TopScore Credentials

1. Log in to https://aum.usetopscore.com
2. Navigate to the Developer Panel
3. Copy your Client ID, Client Secret, and CSRF Token
4. Add them to your `.env` file

### Syncing Data

**CLI Command** (recommended):
```bash
docker-compose exec backend python -m src.cli.sync_topscore
```

**API Endpoint** (background):
```bash
curl -X POST http://localhost:8000/api/v1/sync/topscore
```

**API Endpoint** (immediate):
```bash
curl -X POST http://localhost:8000/api/v1/sync/topscore/immediate
```

## Project Structure

```
ugm_schedule/
├── backend/               # FastAPI backend application
│   ├── src/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── integrations/ # TopScore API client
│   │   └── cli/          # CLI commands
│   └── tests/            # Backend tests
├── frontend/             # Vue.js frontend application
│   ├── src/
│   │   ├── components/   # Vue components
│   │   ├── views/        # Page views
│   │   ├── stores/       # Pinia stores
│   │   └── services/     # API client
│   └── tests/            # Frontend tests
└── docker-compose.yml
```

## Development

### Running Tests

```bash
# Backend tests (all 21 tests should pass)
docker-compose exec backend pytest -v

# Frontend tests
docker-compose exec frontend npm run test
```

### API Endpoints

- `GET /api/v1/games` - List games with filters
- `GET /api/v1/games/{id}` - Get single game
- `GET /api/v1/teams` - List teams
- `GET /api/v1/fields` - List fields
- `GET /api/v1/leagues` - List leagues
- `POST /api/v1/sync/topscore` - Trigger background sync

See http://localhost:8000/docs for interactive API documentation.

### Database Schema

- **leagues** - Sports leagues/events
- **teams** - Team names (auto-normalized)
- **fields** - Game locations
- **games** - Schedule entries with scores and status
- **scrape_logs** - Sync history and statistics

## Documentation

- [TopScore Sync Guide](backend/TOPSCORE_SYNC.md) - TopScore integration details
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Feature Specification](specs/001-schedule-scraper/spec.md) - Requirements
- [Data Model](specs/001-schedule-scraper/data-model.md) - Database schema

## Environment Variables

Key environment variables (see `.env.example` for all):

```bash
# Database
DATABASE_URL=postgresql://ugm_schedule:password@postgres:5432/ugm_schedule

# TopScore API
TOPSCORE_BASE_URL=https://aum.usetopscore.com
TOPSCORE_CLIENT_ID=your_client_id
TOPSCORE_CLIENT_SECRET=your_client_secret
TOPSCORE_CSRF_TOKEN=your_csrf_token

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## License

[License information]

## Contributing

[Contributing guidelines]
