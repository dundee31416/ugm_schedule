# Research: Schedule Scraper Technology Choices

**Feature**: Schedule Scraper and Display System
**Phase**: 0 - Research & Technology Selection
**Date**: 2026-04-07

## Overview

This document captures research findings and decisions for implementing the schedule scraper web application. Each decision includes rationale and alternatives considered.

## Backend Technology Decisions

### Web Scraping Library

**Decision**: Beautiful Soup 4 + Requests (primary), with Scrapy as fallback

**Rationale**:
- Beautiful Soup 4 is lightweight, easy to use, and sufficient for scraping static HTML
- The target website (montrealultimate.ca) appears to serve static HTML schedules
- Requests library is simple for HTTP operations
- Lower complexity than Scrapy for this use case
- Good error handling and debugging capabilities

**Alternatives Considered**:
- **Scrapy**: More powerful framework with built-in scheduling, pipelines, and middleware. However, adds unnecessary complexity for simple daily scraping of a few URLs. Overhead not justified.
- **Selenium/Playwright**: Browser automation tools needed only if JavaScript rendering is required. Initial inspection suggests static HTML is sufficient. Can upgrade later if needed.
- **lxml**: Faster than Beautiful Soup but less forgiving of malformed HTML. Beautiful Soup uses lxml as a parser internally when available.

**Implementation Notes**:
- Use `requests` with retry logic and timeout configuration
- BeautifulSoup with `lxml` parser for speed
- Implement CSS selectors for finding schedule elements
- Add user-agent headers to avoid basic anti-scraping measures

### Task Scheduling

**Decision**: APScheduler (Advanced Python Scheduler)

**Rationale**:
- Pure Python solution, integrates directly with FastAPI application
- Supports cron-style scheduling for daily tasks
- In-process scheduling - no external dependencies
- Persistent job store support if needed later
- Easy to trigger manually for testing

**Alternatives Considered**:
- **Celery + Redis**: Industry standard for distributed task queues. However, adds significant infrastructure complexity (Redis broker, separate worker processes). Overkill for single daily task.
- **Cron + separate script**: Simple but requires server-level configuration. Less portable across environments. Harder to test and monitor.
- **Kubernetes CronJob**: Cloud-native solution but ties deployment to Kubernetes. Not suitable for simple deployments.

**Implementation Notes**:
- Configure daily scrape at 2 AM local time (off-peak)
- Include manual trigger endpoint for testing: `POST /api/admin/trigger-scrape`
- Log all scheduled job executions

### Database Migrations

**Decision**: Alembic

**Rationale**:
- Official migration tool for SQLAlchemy
- Auto-generates migrations from model changes
- Version control for database schema
- Supports rollback and forward migrations
- Well-documented and widely used

**Alternatives Considered**:
- **Manual SQL scripts**: No automation, error-prone, doesn't track model changes
- **Django migrations**: Requires Django ORM, not compatible with SQLAlchemy

**Implementation Notes**:
- Initialize Alembic in `backend/src/database/migrations/`
- Naming convention: `YYYYMMDD_HHMM_description.py`
- Always review auto-generated migrations before applying

## Frontend Technology Decisions

### TypeScript vs JavaScript

**Decision**: TypeScript

**Rationale**:
- Catches type errors at compile time, reducing runtime bugs
- Better IDE support (autocomplete, refactoring)
- Aligns with Constitution Principle IV (Type Safety)
- Interfaces can be generated from OpenAPI schema
- Modern Vue 3 projects strongly favor TypeScript
- Marginal learning curve for team members

**Alternatives Considered**:
- **Plain JavaScript**: Simpler setup, no compile step for type checking. However, loses type safety benefits that align with project constitution. Not recommended given constitution requirements.

**Implementation Notes**:
- Use `strict` mode in `tsconfig.json`
- Generate TypeScript types from OpenAPI schema using `openapi-typescript` or similar tool
- Define types for all component props and emits

### UI Component Library

**Decision**: Custom components with Tailwind CSS (no component library)

**Rationale**:
- Requirements are simple: game cards, filters, search bar, date picker
- Full design control for "modern looking" requirement
- Tailwind provides utility-first CSS without component overhead
- Smaller bundle size
- Learning opportunity for team

**Alternatives Considered**:
- **Vuetify**: Material Design component library. Mature and feature-rich but heavy (large bundle size) and opinionated styling may conflict with "modern" design requirements.
- **PrimeVue**: Comprehensive components including data tables and calendars. However, default themes look dated and would require significant customization.
- **Headless UI (Vue)**: Unstyled components with accessibility built in. Good compromise but still adds dependency for simple requirements.

**Implementation Notes**:
- Install Tailwind CSS with Vue 3 setup
- Create reusable components in `/components` directory
- Use Vue 3 `<script setup>` syntax for cleaner code
- Consider adding a simple date picker library (e.g., VCalendar) if building custom date range picker is too complex

### State Management

**Decision**: Pinia

**Rationale**:
- Official state management for Vue 3 (replaces Vuex)
- Simpler API than Vuex (no mutations, just actions)
- TypeScript support out of the box
- Modular store design
- DevTools integration

**Alternatives Considered**:
- **Vuex**: Older Vue 2 pattern, more verbose, being phased out
- **Composition API only (no store)**: Could use `provide/inject` with reactive objects. Works for small apps but harder to debug and test. Better to use proper state management.

**Implementation Notes**:
- Create `gameStore.ts` with:
  - State: games array, filters (team, field, date range), search query
  - Actions: fetchGames(), applyFilters(), setSearch()
  - Getters: filteredGames, activeFilters

### API Client

**Decision**: Axios

**Rationale**:
- More feature-rich than native `fetch`
- Automatic JSON transformation
- Request/response interceptors for auth and error handling
- Better error handling
- Timeout support
- Widely used and well-documented

**Alternatives Considered**:
- **Native Fetch API**: Modern and no dependencies. However, lacks interceptors, timeout support, and automatic JSON handling. Requires more boilerplate.
- **ky**: Modern fetch wrapper. Smaller and simpler than Axios. However, less mature and fewer features.

**Implementation Notes**:
- Create API client in `/services/api.ts`
- Configure base URL from environment variables
- Add response interceptor for error handling
- Add request interceptor for headers (content-type, etc.)

## Architecture Patterns

### API Design Pattern

**Decision**: RESTful resource-oriented design

**Rationale**:
- Aligns with Constitution Principle I (API-First Architecture)
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Clear resource hierarchy: `/api/v1/games`, `/api/v1/teams`, etc.
- Easy to document with OpenAPI
- Familiar to most developers

**Endpoints**:
```
GET    /api/v1/games              # List games with optional filters
GET    /api/v1/games/{id}         # Get game details
GET    /api/v1/teams              # List all teams
GET    /api/v1/fields             # List all fields
GET    /api/v1/leagues            # List all leagues
POST   /api/admin/trigger-scrape  # Manual scrape trigger (admin only)
GET    /api/health                # Health check
```

**Query Parameters for Filtering**:
- `team_name`: Filter by team name (partial match)
- `field`: Filter by field name
- `start_date`: Filter games after this date (ISO 8601)
- `end_date`: Filter games before this date (ISO 8601)
- `status`: Filter by game status (upcoming/completed)

**Alternatives Considered**:
- **GraphQL**: More flexible querying, single endpoint. However, adds complexity for simple CRUD operations. Overkill for this use case.
- **RPC-style**: Function-oriented endpoints like `/getGames`. Less standard, harder to cache, doesn't leverage HTTP semantics.

### Database Schema Pattern

**Decision**: Normalized relational schema with foreign keys

**Rationale**:
- Clear entity relationships (Game → Team, Game → Field, Game → League)
- Avoid data duplication (team names, field names)
- Easy to query and filter
- PostgreSQL supports complex queries efficiently
- Aligns with SQLAlchemy ORM patterns

**Relationships**:
- Game many-to-one League
- Game many-to-one Field
- Game many-to-one HomeTeam (Team)
- Game many-to-one AwayTeam (Team)
- League one-to-many Games
- Team one-to-many Games (as home or away)

**Alternatives Considered**:
- **Denormalized (embed team/field names in Game)**: Simpler queries but data duplication. Updates require touching multiple records. Not suitable for data that changes (team names might be corrected, field names might change).
- **Document database (MongoDB)**: Flexible schema, easy to store varied scraped data. However, filtering and relationships are less efficient. SQL is better for structured, relational data.

### Scraper Error Handling Pattern

**Decision**: Fail gracefully, log errors, continue with other sources

**Rationale**:
- One failed source shouldn't block others (Constitution Principle V: graceful degradation)
- Detailed logging enables debugging
- Track success/failure in ScrapeLog table
- Alert on repeated failures (future enhancement)

**Error Handling Strategy**:
1. Wrap each URL scrape in try/except
2. Log error with context (URL, timestamp, error type)
3. Continue to next URL
4. Return summary: successes, failures, total
5. Store result in ScrapeLog table

**Alternatives Considered**:
- **Fail fast**: Stop on first error. Simpler but reduces data freshness if one source is down.
- **Retry immediately**: Attempt same URL multiple times. Could work for transient errors but delays other sources. Better to log and retry in next scheduled run.

## Development Workflow Decisions

### Frontend Build Tool

**Decision**: Vite

**Rationale**:
- Official Vue 3 recommendation (replaces Vue CLI)
- Extremely fast hot module replacement (HMR)
- Modern ES modules, optimized production builds
- Built-in TypeScript support
- Simple configuration

**Alternatives Considered**:
- **Webpack**: Older, more complex configuration. Slower dev server. Vite is the modern replacement.
- **Vue CLI**: Being deprecated in favor of Vite.

### Containerization Strategy

**Decision**: Docker + Docker Compose for local development

**Rationale**:
- Consistent environment across developers
- Easy to spin up PostgreSQL for development
- Production-ready containers
- Simple orchestration with docker-compose

**Services**:
- `backend`: FastAPI application (port 8000)
- `frontend`: Vite dev server (port 5173) in dev, Nginx in production
- `postgres`: PostgreSQL database (port 5432)

**Alternatives Considered**:
- **No containers (local setup)**: Requires manual installation of Python, Node, PostgreSQL. Inconsistent environments across developers. Not recommended.
- **Kubernetes**: Overkill for local development. Better suited for production deployment at scale.

### CI/CD Pipeline

**Decision**: GitHub Actions (assumed GitHub repository)

**Rationale**:
- Free for public repositories
- Easy YAML configuration
- Integrated with GitHub
- Supports parallel jobs
- Matrix builds for testing multiple Python/Node versions

**Pipeline Stages**:
1. **Lint**: flake8 (Python), ESLint (TypeScript)
2. **Type Check**: mypy (Python), tsc (TypeScript)
3. **Test**: pytest (backend), Vitest (frontend)
4. **Build**: Docker images
5. **Deploy**: (future) to staging/production

**Alternatives Considered**:
- **GitLab CI**: Excellent but assumes GitLab hosting
- **CircleCI/Travis CI**: Third-party services, less integration with GitHub

## Testing Strategy

### Backend Testing Approach

**Decision**: Pytest with fixtures for database and API testing

**Test Layers**:
1. **Unit Tests**: Test individual functions/classes in isolation
   - Models (validation, relationships)
   - Services (business logic)
   - Utilities
2. **Integration Tests**: Test multiple components together
   - API endpoints with real database (test database)
   - Scraper with mock HTML responses
3. **Contract Tests**: Test API contract compliance
   - Response schemas match OpenAPI spec
   - Status codes correct

**Tools**:
- `pytest`: Test framework
- `pytest-asyncio`: Async test support for FastAPI
- `httpx`: FastAPI test client
- `pytest-mock`: Mocking
- `factory-boy`: Test data factories

### Frontend Testing Approach

**Decision**: Vitest + Vue Test Utils for unit/component tests, Playwright for E2E

**Test Layers**:
1. **Component Tests**: Test Vue components in isolation
   - Props, events, slots
   - User interactions
   - Conditional rendering
2. **E2E Tests**: Test complete user flows
   - View schedule → filter by team → see filtered results
   - Search for team → see matching games
   - Date range filter → see games in range

**Tools**:
- `Vitest`: Fast test runner (Vite-native, replaces Jest)
- `@vue/test-utils`: Vue component testing utilities
- `Playwright`: E2E browser automation (alternative to Cypress, faster and more reliable)

## Security Considerations

### CORS Configuration

**Decision**: Explicit origin allowlist in production, permissive in development

**Rationale**:
- Security best practice: only allow frontend origin
- Prevents unauthorized API access from other domains
- Development mode allows localhost:5173 (Vite default)

**Implementation**:
```python
# backend/src/config/settings.py
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
```

### Input Validation

**Decision**: Pydantic models for all API inputs, SQLAlchemy for database validation

**Rationale**:
- FastAPI automatically validates requests against Pydantic schemas
- Type coercion and validation errors returned as 422 responses
- Prevents injection attacks (SQL, XSS)
- Aligns with Constitution Principle V (Security & Validation)

### Rate Limiting

**Decision**: SlowAPI (FastAPI rate limiting library)

**Rationale**:
- Prevents API abuse
- Simple decorator-based rate limits
- Configurable per-endpoint
- Redis backend optional (can use in-memory for start)

**Configuration**:
- `/api/v1/games`: 100 requests/minute per IP
- `/api/admin/trigger-scrape`: 5 requests/hour per IP (admin only)

## Performance Optimization

### Database Query Optimization

**Decision**: Eager loading for relationships, pagination for large result sets

**Strategies**:
- Use SQLAlchemy `joinedload()` to fetch related entities (teams, fields) in single query
- Implement pagination (limit/offset or cursor-based) for game listings
- Add database indexes on frequently filtered columns (team_id, field_id, game_date)

### Frontend Performance

**Decision**: Virtual scrolling for large lists, debounced search input

**Strategies**:
- Use `vue-virtual-scroller` if game list exceeds 100 items
- Debounce search input (300ms) to reduce API calls
- Cache API responses in Pinia store (invalidate on manual refresh)
- Lazy load images if game cards include team logos

## Summary

All technology choices align with project constitution and best practices for Vue.js + FastAPI web applications. The stack prioritizes:

- **Type Safety**: TypeScript + Pydantic
- **Developer Experience**: Vite, Pinia, pytest, Vitest
- **Simplicity**: Beautiful Soup over Scrapy, APScheduler over Celery
- **Performance**: <3s load time achievable with proper caching and pagination
- **Security**: CORS, input validation, rate limiting

No NEEDS CLARIFICATION items remain. Ready to proceed to Phase 1 (Design & Contracts).
