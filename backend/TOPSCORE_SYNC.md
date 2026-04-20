# TopScore Integration Guide

This application integrates with the TopScore API (https://usetopscore.com) to automatically sync sports league schedules.

## Setup

### 1. Get TopScore Credentials

1. Log in to your TopScore account at https://aum.usetopscore.com
2. Navigate to the Developer Panel
3. Copy the following credentials:
   - **Client ID** (labeled as `auth_token`)
   - **Client Secret**
   - **CSRF Token** (labeled as `api_csrf`)

### 2. Configure Environment Variables

Create or update your `.env` file in the backend directory:

```bash
# TopScore API Integration
TOPSCORE_BASE_URL=https://aum.usetopscore.com
TOPSCORE_CLIENT_ID=your_client_id_here
TOPSCORE_CLIENT_SECRET=your_client_secret_here
TOPSCORE_CSRF_TOKEN=your_csrf_token_here
```

**Important:** Never commit these credentials to version control!

## Usage

There are three ways to sync data from TopScore:

### Option 1: CLI Command (Recommended for Manual Sync)

Run the sync script from inside the Docker container:

```bash
docker-compose exec backend python -m src.cli.sync_topscore
```

This will:
- Fetch all events (leagues) from TopScore
- Fetch all games for each event
- Fetch all teams and locations
- Save everything to the database
- Show a detailed sync report

### Option 2: API Endpoint (Background)

Trigger a background sync via HTTP POST:

```bash
curl -X POST http://localhost:8000/api/v1/sync/topscore
```

Returns immediately with:
```json
{
  "status": "started",
  "message": "TopScore sync has been started in the background"
}
```

### Option 3: API Endpoint (Immediate)

Trigger an immediate sync (blocks until complete):

```bash
curl -X POST http://localhost:8000/api/v1/sync/topscore/immediate
```

Returns when complete with statistics:
```json
{
  "status": "completed",
  "message": "TopScore sync completed successfully",
  "stats": {
    "leagues": 5,
    "teams": 42,
    "fields": 8,
    "games": 156,
    "errors": []
  }
}
```

## What Gets Synced?

### Events → Leagues
TopScore events are mapped to leagues in our database:
- Event name → League name
- Event URL → League source_url
- Event status → League is_active

### Games → Games
TopScore games are synced with full details:
- Home/away teams
- Date and time
- Scores (when available)
- Game status (upcoming/completed/cancelled)
- Location (field)
- External ID for tracking

### Teams → Teams
Team names are automatically normalized to avoid duplicates.

### Locations → Fields
TopScore locations become fields with:
- Name
- Address (if available)
- City (if available)

## Data Model Mapping

| TopScore | Our Database | Notes |
|----------|--------------|-------|
| Event | League | Stored with source URL |
| Game | Game | Includes external_id for tracking |
| Team | Team | Auto-normalized name |
| Location | Field | Includes address/city |
| Standing | - | Not currently synced |

## Scheduling Automatic Syncs

To run syncs automatically, you can:

1. **Add to crontab** (if running natively):
   ```bash
   0 2 * * * cd /path/to/backend && python -m src.cli.sync_topscore >> /var/log/topscore-sync.log 2>&1
   ```

2. **Use Docker cron** (if using Docker):
   Create a separate service in `docker-compose.yml` or use a job scheduler like APScheduler (already in requirements.txt).

## Troubleshooting

### "TopScore credentials not configured"
- Make sure you've set the environment variables in `.env`
- Restart the backend after updating `.env`

### "Failed to obtain access token"
- Verify your CLIENT_ID and CLIENT_SECRET are correct
- Check that your TopScore account has API access enabled

### "Rate limit exceeded"
- TopScore may rate-limit API requests
- The client automatically retries with exponential backoff
- Consider reducing sync frequency

### Games not showing up
- Check that the events are marked as "active" in TopScore
- Verify game dates are set correctly in TopScore
- Check backend logs for specific error messages

## Logs

View sync logs:
```bash
docker-compose logs -f backend | grep -i "topscore\|sync"
```

Each sync creates a `ScrapeLog` entry in the database tracking:
- When the sync started/completed
- Number of games found/added
- Any error messages
- Status (running/completed/failed)
