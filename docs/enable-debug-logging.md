# Enable Debug Logging for CrewAI

## Quick Setup

### 1. Environment Variables

Add these to your `.env` file or export them:

```bash
# CrewAI verbosity
CREWAI_VERBOSE=True

# OpenAI API debugging
OPENAI_LOG=debug
OPENAI_LOG_LEVEL=debug

# Python logging level
LOG_LEVEL=DEBUG

# Show full HTTP requests/responses
HTTPX_LOG_LEVEL=DEBUG
```

### 2. Test Locally with Full Logging

```bash
cd python

# Load environment variables
export $(cat .env | xargs)

# Enable all debug logging
export CREWAI_VERBOSE=True
export OPENAI_LOG=debug
export LOG_LEVEL=DEBUG
export HTTPX_LOG_LEVEL=DEBUG

# Run scraper with debug output
PYTHONPATH=./src python -c "
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import after logging is configured
from event_style_scraper.flows.style_scraping_flow import StyleScrapingFlow

flow = StyleScrapingFlow('https://example.com', timeout=180)
config = flow.start()
print(f'✅ Success: {config.event_id}')
" 2>&1 | tee debug_output.log
```

### 3. Add Detailed Logging to CLI

Edit `python/src/event_style_scraper/cli.py`:

```python
"""CLI interface for event style scraper."""

import click
import sys
import logging  # ADD THIS
from pathlib import Path
from dotenv import load_dotenv

from event_style_scraper.flows.style_scraping_flow import StyleScrapingFlow


@click.group()
def cli():
    """Event Style Scraper - Extract styles and brand voice from event websites."""
    # Load environment variables from .env file
    load_dotenv()

    # ADD THIS: Configure logging based on environment
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
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
@click.option(  # ADD THIS
    "--debug",
    is_flag=True,
    help="Enable debug logging"
)
def scrape(url: str, timeout: int, debug: bool):  # ADD debug parameter
    """
    Scrape an event website to extract styles and brand voice.
    """
    # ADD THIS: Set debug logging if flag is enabled
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug logging enabled")

    try:
        # ... rest of function unchanged
```

### 4. Enable Logging in Crew Configuration

Edit `python/src/event_style_scraper/crews/style_extraction_crew/style_extraction_crew.py`:

```python
@crew
def crew(self) -> Crew:
    """Create crew with all agents and tasks."""
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True,  # Already set
        full_output=True,  # ADD THIS - get full details
        memory=False,
        # ADD THIS: Enable detailed step logging
        step_callback=lambda step: print(f"🔍 Step: {step}"),
        task_callback=lambda task: print(f"📋 Task completed: {task.description[:50]}...")
    )
```

### 5. Monitor OpenAI API Calls

Create a wrapper to log all API calls:

```python
# Add to python/src/event_style_scraper/utils/api_monitor.py

import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)

def monitor_api_call(func):
    """Decorator to monitor and log API calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"🌐 API Call: {func.__name__}")
        logger.debug(f"   Args: {args}")
        logger.debug(f"   Kwargs: {kwargs}")

        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"✅ API Call completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(f"❌ API Call failed after {duration:.2f}s: {e}")
            raise
    return wrapper
```

## GitHub Actions Logging

### 6. Update Workflow for Debug Logs

Edit `.github/workflows/scrape-and-deploy.yml`:

```yaml
- name: Scrape event websites
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    CREWAI_VERBOSE: "True"           # ADD THIS
    OPENAI_LOG: "debug"               # ADD THIS
    LOG_LEVEL: "DEBUG"                # ADD THIS
  run: |
    cd python

    # Determine which events to scrape
    if [ "${{ inputs.events_to_scrape }}" == "all" ] || [ -z "${{ inputs.events_to_scrape }}" ]; then
      EVENTS=("eventtechlive.com" "example.com")
    else
      IFS=',' read -ra EVENTS <<< "${{ inputs.events_to_scrape }}"
    fi

    echo "Scraping events: ${EVENTS[@]}"

    for event in "${EVENTS[@]}"; do
      echo "Scraping $event..."
      echo "=== Starting scrape at $(date -u +"%Y-%m-%dT%H:%M:%SZ") ===="  # ADD THIS

      PYTHONPATH=./src python -m event_style_scraper scrape \
        --url "https://$event" \
        --timeout 90 \
        --debug || echo "⚠️ Failed to scrape $event"  # ADD --debug flag

      echo "=== Finished scrape at $(date -u +"%Y-%m-%dT%H:%M:%SZ") ===="  # ADD THIS
    done
```

## Interpreting Logs

### What to Look For

**Successful API Call:**
```
2025-11-08 03:35:45 - openai - DEBUG - Request to OpenAI API
2025-11-08 03:35:46 - openai - DEBUG - Response status: 200
2025-11-08 03:35:46 - openai - INFO - Tokens used: 1234
```

**Connection Timeout:**
```
2025-11-08 03:35:45 - openai - DEBUG - Request to OpenAI API
[13 minutes of silence]
2025-11-08 03:48:45 - openai - ERROR - Connection error: timeout
```

**Rate Limit:**
```
2025-11-08 03:35:45 - openai - ERROR - Rate limit exceeded
2025-11-08 03:35:45 - openai - INFO - Retrying in 20s...
```

**API Key Invalid:**
```
2025-11-08 03:35:45 - openai - ERROR - Authentication failed: Invalid API key
```

## Quick Test Command

Run this to test with full logging enabled:

```bash
cd python
export $(cat .env | xargs)
export CREWAI_VERBOSE=True OPENAI_LOG=debug LOG_LEVEL=DEBUG

# Run with all debugging enabled
time PYTHONPATH=./src python -m event_style_scraper scrape \
  --url https://example.com \
  --timeout 180 \
  --debug 2>&1 | tee scrape_debug.log

# View the log
less scrape_debug.log
```

## Troubleshooting

### Issue: No debug logs appearing

**Solution:** Python logging must be configured BEFORE importing libraries.

```python
# ❌ WRONG ORDER
from crewai import Crew
logging.basicConfig(level=logging.DEBUG)

# ✅ CORRECT ORDER
logging.basicConfig(level=logging.DEBUG)
from crewai import Crew
```

### Issue: Logs truncated in GitHub Actions

**Solution:** Add flush statements:

```python
import sys

print("Log message", flush=True)  # Force immediate output
sys.stdout.flush()  # Flush stdout buffer
sys.stderr.flush()  # Flush stderr buffer
```

### Issue: OpenAI debug logs not showing

**Solution:** OpenAI uses httpx for requests. Enable httpx logging:

```python
import logging

logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger("openai").setLevel(logging.DEBUG)
```

## Related Files

- `python/src/event_style_scraper/cli.py` - CLI entry point
- `python/src/event_style_scraper/crews/style_extraction_crew/style_extraction_crew.py` - Crew config
- `python/src/event_style_scraper/flows/style_scraping_flow.py` - Flow orchestration
- `.github/workflows/scrape-and-deploy.yml` - CI/CD workflow
