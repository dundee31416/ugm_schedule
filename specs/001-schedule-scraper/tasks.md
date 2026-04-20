# Tasks: Schedule Scraper and Display System

**Input**: Design documents from `/specs/001-schedule-scraper/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Per Constitution Principle III (Test-First Development), this feature includes comprehensive test tasks before implementation. TDD workflow is mandatory.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend tests: `backend/tests/`
- Frontend tests: `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure: backend/src/{api,models,schemas,services,database,config,utils}
- [ ] T002 Create frontend directory structure: frontend/src/{components,pages,services,stores,types,composables,router,assets}
- [ ] T003 [P] Create backend/requirements.txt with FastAPI, SQLAlchemy, Pydantic, psycopg2, alembic, beautifulsoup4, requests, apscheduler, slowapi
- [ ] T004 [P] Create backend/requirements-dev.txt with pytest, pytest-asyncio, httpx, black, flake8, mypy
- [ ] T005 [P] Create frontend/package.json with Vue 3, Vue Router, Pinia, Axios, Tailwind CSS dependencies
- [ ] T006 [P] Create frontend/package.json dev dependencies: Vite, TypeScript, Vitest, @vue/test-utils, Playwright, ESLint
- [ ] T007 [P] Create docker-compose.yml orchestrating postgres, backend, frontend services
- [ ] T008 [P] Create backend/Dockerfile for Python 3.11 FastAPI application
- [ ] T009 [P] Create frontend/Dockerfile for Node.js Vite build
- [ ] T010 [P] Create .env.example with DATABASE_URL, API_HOST, API_PORT, CORS_ORIGINS, VITE_API_BASE_URL templates
- [ ] T011 [P] Create backend/pyproject.toml for Python project metadata and tool configuration
- [ ] T012 [P] Create frontend/vite.config.ts for Vite configuration
- [ ] T013 [P] Create frontend/tsconfig.json for TypeScript strict mode
- [ ] T014 [P] Create frontend/tailwind.config.js for Tailwind CSS configuration
- [ ] T015 [P] Create README.md with project overview and quick start link to specs/001-schedule-scraper/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T016 Create backend/src/config/settings.py with environment variable loading and validation
- [ ] T017 Create backend/src/utils/logger.py with structured logging configuration
- [ ] T018 Create backend/src/database/session.py with SQLAlchemy engine and session factory
- [ ] T019 Initialize Alembic in backend/src/database/migrations/ for database migration management
- [ ] T020 Create backend/src/api/main.py with FastAPI app initialization, CORS middleware, and health check endpoint
- [ ] T021 Create backend/src/api/dependencies.py with database session dependency injection
- [ ] T022 [P] Create frontend/src/main.ts with Vue app initialization
- [ ] T023 [P] Create frontend/src/App.vue as root component with router-view
- [ ] T024 [P] Create frontend/src/router/index.ts with Vue Router configuration
- [ ] T025 Create frontend/src/services/api.ts with Axios client, base URL, and error interceptors
- [ ] T026 Create frontend/src/types/api.ts with basic TypeScript type definitions for API responses
- [ ] T027 Create backend/src/config/sources.yaml as configuration file template for league URLs
- [ ] T028 Run initial Alembic migration to create empty database schema
- [ ] T029 Verify backend starts successfully at http://localhost:8000
- [ ] T030 Verify frontend starts successfully at http://localhost:5173

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Filter Schedules (Priority: P1) 🎯 MVP

**Goal**: Users can view games and filter by team, field, and date range with real-time search

**Independent Test**: Load sample games into database, open frontend, verify filtering and search work correctly

### Tests for User Story 1 (TDD Mandatory) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T031 [P] [US1] Contract test for GET /api/v1/games endpoint in backend/tests/contract/test_game_api.py
- [ ] T032 [P] [US1] Contract test for GET /api/v1/teams endpoint in backend/tests/contract/test_team_api.py
- [ ] T033 [P] [US1] Contract test for GET /api/v1/fields endpoint in backend/tests/contract/test_field_api.py
- [ ] T034 [P] [US1] Contract test for GET /api/v1/leagues endpoint in backend/tests/contract/test_league_api.py
- [ ] T035 [P] [US1] Integration test for filter flow in backend/tests/integration/test_filter_flow.py
- [ ] T036 [P] [US1] Component test for GameList.vue in frontend/tests/unit/components/GameList.spec.ts
- [ ] T037 [P] [US1] Component test for FilterPanel.vue in frontend/tests/unit/components/FilterPanel.spec.ts
- [ ] T038 [P] [US1] Component test for SearchBar.vue in frontend/tests/unit/components/SearchBar.spec.ts

### Backend Implementation for User Story 1

- [ ] T039 [P] [US1] Create League model in backend/src/models/league.py with SQLAlchemy schema per data-model.md
- [ ] T040 [P] [US1] Create Team model in backend/src/models/team.py with normalized_name field and relationships
- [ ] T041 [P] [US1] Create Field model in backend/src/models/field.py with name, address, city fields
- [ ] T042 [US1] Create Game model in backend/src/models/game.py with relationships to League, Team, Field (depends on T039, T040, T041)
- [ ] T043 [P] [US1] Create League Pydantic schemas in backend/src/schemas/league.py for request/response validation
- [ ] T044 [P] [US1] Create Team Pydantic schemas in backend/src/schemas/team.py with TeamSummary and TeamResponse
- [ ] T045 [P] [US1] Create Field Pydantic schemas in backend/src/schemas/field.py with FieldSummary and FieldResponse
- [ ] T046 [US1] Create Game Pydantic schemas in backend/src/schemas/game.py with GameResponse, GameListResponse, GameFilters (depends on T043, T044, T045)
- [ ] T047 [US1] Create Alembic migration for League, Team, Field, Game tables with indexes and foreign keys
- [ ] T048 [US1] Apply migration to create database schema: alembic upgrade head
- [ ] T049 [US1] Create GameService in backend/src/services/game_service.py with get_games, get_game_by_id, apply_filters methods
- [ ] T050 [US1] Implement GET /api/v1/games endpoint in backend/src/api/routes/games.py with filtering support
- [ ] T051 [US1] Implement GET /api/v1/games/{id} endpoint in backend/src/api/routes/games.py
- [ ] T052 [P] [US1] Implement GET /api/v1/teams endpoint in backend/src/api/routes/teams.py
- [ ] T053 [P] [US1] Implement GET /api/v1/teams/{id} endpoint in backend/src/api/routes/teams.py
- [ ] T054 [P] [US1] Implement GET /api/v1/fields endpoint in backend/src/api/routes/fields.py
- [ ] T055 [P] [US1] Implement GET /api/v1/leagues endpoint in backend/src/api/routes/leagues.py
- [ ] T056 [US1] Register all route modules in backend/src/api/main.py with /api/v1 prefix
- [ ] T057 [US1] Create sample data seed script in backend/scripts/seed_data.py with 50+ games for testing
- [ ] T058 [US1] Run seed script to populate database with test data

### Frontend Implementation for User Story 1

- [ ] T059 [US1] Generate TypeScript types from OpenAPI schema in frontend/src/types/api.ts
- [ ] T060 [US1] Create Pinia game store in frontend/src/stores/gameStore.ts with state, actions, getters for games, filters, search
- [ ] T061 [P] [US1] Create useFilters composable in frontend/src/composables/useFilters.ts for filter logic
- [ ] T062 [P] [US1] Create useSearch composable in frontend/src/composables/useSearch.ts for debounced search
- [ ] T063 [P] [US1] Create GameCard component in frontend/src/components/GameCard.vue displaying game details
- [ ] T064 [P] [US1] Create GameList component in frontend/src/components/GameList.vue rendering list of GameCard components
- [ ] T065 [P] [US1] Create FilterPanel component in frontend/src/components/FilterPanel.vue with team, field, date filters
- [ ] T066 [P] [US1] Create SearchBar component in frontend/src/components/SearchBar.vue with real-time search input
- [ ] T067 [P] [US1] Create DateRangePicker component in frontend/src/components/DateRangePicker.vue for date range selection
- [ ] T068 [US1] Create ScheduleView page in frontend/src/pages/ScheduleView.vue integrating all components
- [ ] T069 [US1] Add ScheduleView route to frontend/src/router/index.ts as default route
- [ ] T070 [US1] Implement API calls in gameStore fetchGames action using api.ts client
- [ ] T071 [US1] Add Tailwind CSS styling to components for modern, responsive design
- [ ] T072 [US1] Implement "last updated" timestamp display in ScheduleView page
- [ ] T073 [US1] Add clear filters button to FilterPanel component

### Verification for User Story 1

- [ ] T074 [US1] Run backend tests: pytest backend/tests/ - verify all tests pass
- [ ] T075 [US1] Run frontend component tests: npm run test - verify all tests pass
- [ ] T076 [US1] Manual test: Open http://localhost:5173, verify games display correctly
- [ ] T077 [US1] Manual test: Filter by team name, verify results update
- [ ] T078 [US1] Manual test: Filter by field, verify results update
- [ ] T079 [US1] Manual test: Filter by date range, verify results update
- [ ] T080 [US1] Manual test: Search for team, verify real-time results
- [ ] T081 [US1] Manual test: Combine multiple filters, verify all work together
- [ ] T082 [US1] Manual test: Clear filters, verify full schedule displays

**Checkpoint**: User Story 1 (MVP) complete and independently testable

---

## Phase 4: User Story 2 - Automated Daily Data Updates (Priority: P2)

**Goal**: System automatically scrapes configured league websites daily and updates database

**Independent Test**: Configure one source URL, trigger manual scrape, verify data extracted and stored correctly

### Tests for User Story 2 (TDD Mandatory) ⚠️

- [ ] T083 [P] [US2] Unit test for scraper service in backend/tests/unit/test_scraper.py with mock HTML responses
- [ ] T084 [P] [US2] Unit test for scheduler service in backend/tests/unit/test_scheduler.py
- [ ] T085 [P] [US2] Integration test for complete scraper flow in backend/tests/integration/test_scraper_flow.py
- [ ] T086 [P] [US2] Contract test for POST /api/admin/trigger-scrape endpoint in backend/tests/contract/test_admin_api.py
- [ ] T087 [P] [US2] Contract test for GET /api/v1/scrape-logs endpoint in backend/tests/contract/test_scrape_log_api.py

### Backend Implementation for User Story 2

- [ ] T088 [US2] Create ScrapeLog model in backend/src/models/scrape_log.py with league_id, status, timestamps, error tracking
- [ ] T089 [US2] Create ScrapeLog Pydantic schemas in backend/src/schemas/scrape_log.py
- [ ] T090 [US2] Create Alembic migration for ScrapeLog table
- [ ] T091 [US2] Apply migration: alembic upgrade head
- [ ] T092 [US2] Implement parse_schedule_html function in backend/src/services/scraper.py using BeautifulSoup to extract games
- [ ] T093 [US2] Implement scrape_league function in backend/src/services/scraper.py with HTTP requests, HTML parsing, error handling
- [ ] T094 [US2] Implement upsert_game logic in backend/src/services/scraper.py to handle create/update based on external_id
- [ ] T095 [US2] Implement get_or_create_team helper in backend/src/services/scraper.py for team deduplication
- [ ] T096 [US2] Implement get_or_create_field helper in backend/src/services/scraper.py for field deduplication
- [ ] T097 [US2] Add scrape logging to ScrapeLog table in backend/src/services/scraper.py
- [ ] T098 [US2] Implement run_daily_scrape function in backend/src/services/scheduler.py to scrape all active leagues
- [ ] T099 [US2] Configure APScheduler in backend/src/services/scheduler.py for daily execution at 2 AM
- [ ] T100 [US2] Integrate scheduler startup with FastAPI lifespan events in backend/src/api/main.py
- [ ] T101 [P] [US2] Implement POST /api/admin/trigger-scrape endpoint in backend/src/api/routes/admin.py for manual scraping
- [ ] T102 [P] [US2] Implement GET /api/v1/scrape-logs endpoint in backend/src/api/routes/scrape_logs.py
- [ ] T103 [US2] Add rate limiting to admin trigger endpoint using SlowAPI: 5 requests/hour
- [ ] T104 [US2] Add user-agent header configuration to scraper requests in backend/src/config/settings.py

### Verification for User Story 2

- [ ] T105 [US2] Run scraper unit tests: pytest backend/tests/unit/test_scraper.py - verify all pass
- [ ] T106 [US2] Run scraper integration tests: pytest backend/tests/integration/ - verify all pass
- [ ] T107 [US2] Manual test: Trigger scrape via POST /api/admin/trigger-scrape, verify response 202
- [ ] T108 [US2] Manual test: Check scrape logs via GET /api/v1/scrape-logs, verify entry created
- [ ] T109 [US2] Manual test: Verify games created in database after scrape
- [ ] T110 [US2] Manual test: Trigger second scrape, verify games updated (not duplicated)
- [ ] T111 [US2] Manual test: Verify scheduler runs at configured time (or wait for next 2 AM)
- [ ] T112 [US2] Manual test: Verify error handling by using invalid URL in sources.yaml

**Checkpoint**: User Story 2 complete - automated scraping functional

---

## Phase 5: User Story 3 - Configure Data Sources (Priority: P3)

**Goal**: Administrators can manage league URLs via configuration file

**Independent Test**: Edit sources.yaml to add/remove URLs, restart system, verify only configured sources scraped

### Tests for User Story 3 (TDD Mandatory) ⚠️

- [ ] T113 [P] [US3] Unit test for config loader in backend/tests/unit/test_config.py
- [ ] T114 [P] [US3] Unit test for config validation in backend/tests/unit/test_config.py with invalid YAML scenarios

### Backend Implementation for User Story 3

- [ ] T115 [US3] Implement load_sources_config function in backend/src/config/settings.py to parse sources.yaml
- [ ] T116 [US3] Implement validate_source_entry function in backend/src/config/settings.py to check URL format, required fields
- [ ] T117 [US3] Add config validation on app startup in backend/src/api/main.py
- [ ] T118 [US3] Implement sync_leagues_from_config function in backend/src/services/scraper.py to create/update League records
- [ ] T119 [US3] Add error logging for invalid config entries in backend/src/config/settings.py
- [ ] T120 [US3] Update scraper to filter by is_active flag from League model
- [ ] T121 [US3] Create example sources.yaml with multiple leagues (active and inactive examples)
- [ ] T122 [US3] Document sources.yaml format in backend/src/config/sources.yaml with comments

### Verification for User Story 3

- [ ] T123 [US3] Run config unit tests: pytest backend/tests/unit/test_config.py - verify all pass
- [ ] T124 [US3] Manual test: Edit sources.yaml to add new league, restart backend, verify league created in database
- [ ] T125 [US3] Manual test: Set league enabled=false in sources.yaml, restart, verify scraper skips it
- [ ] T126 [US3] Manual test: Add invalid URL to sources.yaml, restart, verify clear error message in logs
- [ ] T127 [US3] Manual test: Remove league from sources.yaml, restart, verify database unchanged (no deletion)

**Checkpoint**: User Story 3 complete - configuration management functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T128 [P] Add rate limiting to all API endpoints using SlowAPI: 100 requests/minute
- [ ] T129 [P] Configure CORS with explicit origin allowlist from environment variables
- [ ] T130 [P] Add request ID tracking to all API responses via X-Request-ID header
- [ ] T131 [P] Add comprehensive error logging with request context in backend/src/utils/logger.py
- [ ] T132 [P] Implement pagination for GET /api/v1/games with limit/offset query parameters
- [ ] T133 [P] Add database indexes optimization based on query patterns from data-model.md
- [ ] T134 [P] Implement frontend loading states for API calls in gameStore
- [ ] T135 [P] Add frontend error toast notifications for failed API requests
- [ ] T136 [P] Implement frontend skeleton loaders for GameList while loading
- [ ] T137 [P] Add backend type checking: mypy backend/src/ - fix any type errors
- [ ] T138 [P] Add backend linting: flake8 backend/src/ - fix any linting errors
- [ ] T139 [P] Add backend code formatting: black backend/src/ tests/
- [ ] T140 [P] Add frontend type checking: npm run type-check - fix any errors
- [ ] T141 [P] Add frontend linting: npm run lint - fix any errors
- [ ] T142 [P] Add frontend formatting: npm run format
- [ ] T143 [P] Create E2E test for complete user journey in frontend/tests/e2e/schedule.spec.ts using Playwright
- [ ] T144 [P] Run E2E tests: npm run test:e2e - verify pass
- [ ] T145 [P] Measure backend test coverage: pytest --cov=src - target 80%+
- [ ] T146 [P] Measure frontend test coverage: npm run test:coverage - target 80%+
- [ ] T147 [P] Optimize bundle size: npm run build - verify <500KB initial bundle
- [ ] T148 [P] Add meta tags and title to frontend for SEO
- [ ] T149 [P] Add favicon to frontend
- [ ] T150 Validate quickstart.md by following setup instructions from scratch
- [ ] T151 Update README.md with architecture diagram and feature completion status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion (can run parallel to US1)
- **User Story 3 (Phase 5)**: Depends on Foundational phase completion (can run parallel to US1/US2)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories ✅ MVP
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent from US1 (but requires Game/League/Team/Field models)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent from US1/US2

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Models before schemas
- Schemas before services
- Services before API routes
- Backend routes before frontend implementation
- Frontend components before page integration
- Implementation before verification

### Parallel Opportunities

**Setup Phase (can all run in parallel)**:
- T003-T015 all marked [P]

**Foundational Phase (some parallel)**:
- T022-T027 all marked [P] (frontend setup independent from backend)

**User Story 1 - Models (can run in parallel)**:
- T039, T040, T041 (League, Team, Field models)

**User Story 1 - Schemas (can run in parallel)**:
- T043, T044, T045 (after models complete)

**User Story 1 - Routes (can run in parallel)**:
- T052-T055 (teams, fields, leagues endpoints)

**User Story 1 - Frontend Components (can run in parallel)**:
- T063-T067 (GameCard, GameList, FilterPanel, SearchBar, DateRangePicker)

**User Story 2 - Tests (can run in parallel)**:
- T083-T087

**User Story 2 - Routes (can run in parallel)**:
- T101-T102

**Polish Phase (most can run in parallel)**:
- T128-T149 all marked [P]

**Different User Stories Can Run in Parallel**:
- After Foundational phase completes, teams can work on US1, US2, US3 simultaneously

---

## Parallel Example: User Story 1

```bash
# Launch all model tasks together:
Task T039: Create League model
Task T040: Create Team model
Task T041: Create Field model

# After models complete, launch all schema tasks together:
Task T043: Create League schemas
Task T044: Create Team schemas
Task T045: Create Field schemas

# After routes complete, launch all frontend components together:
Task T063: Create GameCard component
Task T064: Create GameList component
Task T065: Create FilterPanel component
Task T066: Create SearchBar component
Task T067: Create DateRangePicker component
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T015)
2. Complete Phase 2: Foundational (T016-T030)
3. Complete Phase 3: User Story 1 (T031-T082)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Demo: Users can view and filter schedules
6. Deploy MVP if ready

**MVP Deliverable**: Working schedule viewer with filters and search (no automated scraping yet)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! 🎯)
3. Add User Story 2 → Test independently → Deploy/Demo (automated updates added)
4. Add User Story 3 → Test independently → Deploy/Demo (config management added)
5. Add Polish tasks → Final testing → Production deploy

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T030)
2. Once Foundational is done:
   - **Developer A**: User Story 1 frontend (T059-T073)
   - **Developer B**: User Story 1 backend (T031-T058)
   - **Developer C**: User Story 2 (T083-T112)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD enforced**: Verify tests fail before implementing (Constitution Principle III)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All file paths are exact per plan.md structure
- Tests must achieve 80%+ coverage per Constitution requirements

---

## Task Summary

**Total Tasks**: 151
**Setup Phase**: 15 tasks
**Foundational Phase**: 15 tasks
**User Story 1 (MVP)**: 51 tasks
**User Story 2**: 30 tasks
**User Story 3**: 15 tasks
**Polish Phase**: 24 tasks
**Verification Tasks**: 1 task

**Parallel Opportunities**: 60+ tasks can run in parallel within their phases

**MVP Scope**: Phases 1-3 (T001-T082) = 81 tasks for working schedule viewer

**Independent Test Criteria**:
- US1: Load games → open frontend → verify filters work
- US2: Configure URL → trigger scrape → verify data stored
- US3: Edit sources.yaml → restart → verify config applied

**Ready for Implementation**: ✅ All tasks follow checklist format, include file paths, and are organized by user story priority.
