"""Fetch all TopScore events and load into a pandas DataFrame for exploration."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from src.config.settings import settings
from src.integrations.topscore.client import TopScoreClient
import pandas as pd

client = TopScoreClient(
    base_url=settings.TOPSCORE_BASE_URL,
    client_id=settings.TOPSCORE_CLIENT_ID,
    client_secret=settings.TOPSCORE_CLIENT_SECRET,
    csrf_token=settings.TOPSCORE_CSRF_TOKEN,
    timeout=settings.SCRAPER_TIMEOUT,
)

print("Fetching events from TopScore...")
events = client.get_events()
print(f"Fetched {len(events)} events")

df = pd.DataFrame(events)

print(f"\nShape: {df.shape}")
print(f"\nColumns:\n{df.columns.tolist()}")
print(f"\nSample data:\n{df.head(10).to_string()}")

type_cols = [c for c in df.columns if "type" in c.lower() or "kind" in c.lower() or "category" in c.lower()]
if type_cols:
    print(f"\nType-related columns: {type_cols}")
    print(df[type_cols].value_counts().to_string())