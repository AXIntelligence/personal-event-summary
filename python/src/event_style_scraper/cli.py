"""CLI interface for event style scraper."""

import click
import sys
from pathlib import Path
from dotenv import load_dotenv

from event_style_scraper.flows.style_scraping_flow import StyleScrapingFlow


@click.group()
def cli():
    """Event Style Scraper - Extract styles and brand voice from event websites."""
    # Load environment variables from .env file
    load_dotenv()
    pass


@cli.command()
@click.option(
    "--url",
    required=True,
    help="URL of the event website to scrape"
)
@click.option(
    "--timeout",
    default=60,
    type=int,
    help="Timeout in seconds for scraping operations (default: 60)"
)
def scrape(url: str, timeout: int):
    """
    Scrape an event website to extract styles and brand voice.

    This command will:
    1. Scrape the website at the given URL
    2. Extract colors, typography, and brand voice
    3. Export the configuration to style-configs/{event-id}.json

    Example:
        python -m event_style_scraper scrape --url https://dearmarkus.ai/
    """
    try:
        # Create flow and run scraping
        click.echo(f"🔍 Scraping website: {url}")
        click.echo(f"⏱️  Timeout: {timeout}s")
        click.echo()

        flow = StyleScrapingFlow(url=url, timeout=timeout)

        click.echo("🤖 Starting style extraction crew...")
        config = flow.start()

        click.echo("✅ Style extraction completed!")
        click.echo()
        click.echo(f"   Event: {config.event_name}")
        click.echo(f"   ID: {config.event_id}")
        click.echo(f"   Colors: {config.colors.primary}, {config.colors.secondary}")
        click.echo()

        click.echo("💾 Exporting configuration...")
        output_path = flow.export_config(config)

        click.echo()
        click.echo(f"✅ Success! Configuration saved to:")
        click.echo(f"   {output_path}")

    except ValueError as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"❌ Scraping failed: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
