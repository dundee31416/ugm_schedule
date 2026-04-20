# Feature Specification: Schedule Scraper and Display System

**Feature Branch**: `001-schedule-scraper`
**Created**: 2026-04-07
**Status**: Draft
**Input**: User description: "The website should be very modern looking and show schedules and results in a neat display that can be easily filtered or searched. There should be a config file with a list of urls such as https://montrealultimate.ca/fr_ca/e/ligues-recreatives-hiver-2025-2026. And each URL must be scraped for the 'schedule' section to extract schedule, teams, scores, fields, location, and all available information. This should be gathered in a SQL Alchemy database. The scrapping should occur once per day."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View and Filter Schedules (Priority: P1)

A user visits the website to view upcoming games and past results for their league. They want to quickly find games for a specific team, at a particular field, or on a certain date without scrolling through everything.

**Why this priority**: This is the core value proposition - users need to access schedule information easily. Without this, there's no point to the application.

**Independent Test**: Can be fully tested by loading pre-populated schedule data into the database, opening the website, and verifying that filtering by team, date, field, and search functionality all work correctly.

**Acceptance Scenarios**:

1. **Given** the database contains schedules from multiple leagues, **When** a user opens the website, **Then** they see a modern display of all upcoming games with team names, dates, times, and locations
2. **Given** a user is viewing the schedule, **When** they type a team name in the search box, **Then** the display updates to show only games involving that team
3. **Given** a user is viewing the schedule, **When** they select a date range filter, **Then** only games within that date range are displayed
4. **Given** a user is viewing the schedule, **When** they select a specific field from the filter dropdown, **Then** only games at that field are shown
5. **Given** a user is viewing past games, **When** they look at completed games, **Then** they see the final scores displayed alongside the game information
6. **Given** multiple filters are active, **When** a user clears all filters, **Then** the full schedule is displayed again

---

### User Story 2 - Automated Daily Data Updates (Priority: P2)

The system automatically checks configured league websites once per day and updates the database with any new or changed schedule information, ensuring users always see current data.

**Why this priority**: Data freshness is critical for a schedule system. Manual updates would make the system impractical. This must work reliably before launch.

**Independent Test**: Can be tested by setting up the scheduled task, configuring one source URL, running the scraper manually, and verifying that schedule data is correctly extracted and stored in the database.

**Acceptance Scenarios**:

1. **Given** the system is running and the daily scrape time has arrived, **When** the automated task executes, **Then** each configured URL is scraped and new schedule data is stored in the database
2. **Given** a league website has updated game times, **When** the next daily scrape runs, **Then** the database reflects the updated times
3. **Given** a new game has been added to a league website, **When** the daily scrape runs, **Then** the new game appears in the database and on the website
4. **Given** a scraping attempt fails due to network issues, **When** the error occurs, **Then** the system logs the error and continues attempting to scrape other configured URLs
5. **Given** the daily scrape completes, **When** a user views the schedule, **Then** they see data that was updated within the last 24 hours

---

### User Story 3 - Configure Data Sources (Priority: P3)

An administrator can add, remove, or modify the list of league websites that should be scraped for schedule data through a configuration file.

**Why this priority**: Allows the system to scale to multiple leagues and adapt to changing data sources without code changes. Nice-to-have for initial launch but essential for maintainability.

**Independent Test**: Can be tested by editing the configuration file to add/remove URLs, restarting the system, and verifying that only the configured sources are scraped during the next update.

**Acceptance Scenarios**:

1. **Given** an administrator wants to add a new league, **When** they add a new URL to the configuration file and restart the scraper service, **Then** the next daily scrape includes that new source
2. **Given** a league is no longer active, **When** the administrator removes its URL from the configuration file, **Then** that source is no longer scraped
3. **Given** a league website URL has changed, **When** the administrator updates the URL in the configuration file, **Then** the scraper uses the new URL on the next run
4. **Given** the configuration file is edited, **When** the file contains a syntax error or invalid URL format, **Then** the system logs a clear error message indicating which entry is problematic

---

### Edge Cases

- What happens when a league website changes its HTML structure, breaking the scraper?
- How does the system handle duplicate games (same teams, date, time) from multiple scrapes?
- What happens when a configured URL returns a 404 or is unreachable?
- How are games with TBD (to be determined) times, locations, or opponents displayed?
- What happens when a game is cancelled or rescheduled on the source website?
- How does the system handle very large schedules (100+ games)?
- What happens if the daily scrape takes longer than 24 hours to complete?
- How are games in different timezones handled and displayed?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display schedules in a modern, visually appealing interface with clear typography and responsive layout
- **FR-002**: System MUST allow users to filter schedules by team name, field/location, and date range
- **FR-003**: System MUST provide a search function that finds games by team name, field, or location
- **FR-004**: System MUST display both upcoming games (with date/time/location) and completed games (with final scores)
- **FR-005**: System MUST read data source URLs from a configuration file
- **FR-006**: System MUST scrape the schedule section from each configured URL automatically once per day
- **FR-007**: System MUST extract and store: team names, game dates/times, field names, locations, scores (if available), and any other available game information
- **FR-008**: System MUST persist all scraped data in a database
- **FR-009**: System MUST update existing game records when information changes on the source website
- **FR-010**: System MUST handle scraping failures gracefully without crashing and log errors for debugging
- **FR-011**: System MUST prevent duplicate game entries in the database
- **FR-012**: System MUST display data that is no older than 24 hours since the last successful scrape
- **FR-013**: Filters MUST be combinable (e.g., show Team A games at Field B in March)
- **FR-014**: Search results MUST update in real-time as the user types
- **FR-015**: System MUST indicate on the UI when data was last updated

### Key Entities

- **League**: Represents a sports league/competition with a name and source URL. Each league is scraped independently.
- **Team**: Represents a team participating in games. Has a name and belongs to one or more leagues.
- **Game**: Represents a single scheduled game. Includes date, time, home team, away team, field, location, status (upcoming/completed), and optionally scores.
- **Field**: Represents a physical location where games are played. Has a name and may have address/location details.
- **ScrapeLog**: Tracks scraping operations including timestamp, source URL, success/failure status, and any error messages.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can find a specific team's games within 10 seconds of opening the website
- **SC-002**: The website loads and displays schedules in under 3 seconds on standard broadband connections
- **SC-003**: 95% of daily scraping operations complete successfully without manual intervention
- **SC-004**: Users can view schedules on mobile devices (phones and tablets) with the same functionality as desktop
- **SC-005**: The system successfully handles schedules containing at least 500 games without performance degradation
- **SC-006**: Filter and search operations return results in under 1 second
- **SC-007**: Schedule data is automatically refreshed within 24 hours of being published on source websites

## Assumptions

- The target league websites (like montrealultimate.ca) have a consistent "schedule" section with structured HTML that can be reliably scraped
- Users will primarily access the website during daytime hours (scraping can occur during off-peak times)
- The website does not require user authentication - all schedule data is publicly viewable
- The scraping frequency of once per day is sufficient (real-time updates are not required)
- The configuration file will be manually edited by someone with basic technical knowledge (no web-based admin UI required for v1)
- Source websites will not implement aggressive anti-scraping measures (rate limiting, CAPTCHAs, etc.)
- All games within a league use the same timezone for display purposes
- The system will run on a server with reliable internet connectivity and sufficient resources for daily scraping tasks
- Mobile responsiveness is required, but native mobile apps are out of scope for v1
