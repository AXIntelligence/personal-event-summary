"""Main entry point for running event_style_scraper as a module."""

from dotenv import load_dotenv
from event_style_scraper.cli import cli

if __name__ == "__main__":
    # Load .env before invoking CLI
    load_dotenv()
    cli()
