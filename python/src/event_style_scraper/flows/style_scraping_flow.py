"""Flow orchestration for web scraping and style extraction."""

import json
from pathlib import Path
from typing import Optional, Literal
from pydantic import BaseModel, Field

from event_style_scraper.types import EventStyleConfig
from event_style_scraper.tools import WebScraperTool, SecurityError
from event_style_scraper.crews.style_extraction_crew import StyleExtractionCrew


class StyleScrapingState(BaseModel):
    """State model for style scraping flow."""

    url: str = Field(..., description="URL to scrape")
    status: Literal["pending", "scraping", "completed", "failed"] = Field(
        default="pending",
        description="Current status of the scraping process"
    )
    result: Optional[EventStyleConfig] = Field(
        default=None,
        description="Extracted style configuration"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if scraping failed"
    )


class StyleScrapingFlow:
    """
    Flow orchestration for style extraction from event websites.

    This flow coordinates the StyleExtractionCrew to scrape websites,
    extract styles, and export JSON configurations.
    """

    def __init__(self, url: str, timeout: int = 60):
        """
        Initialize StyleScrapingFlow.

        Args:
            url: URL of the event website to scrape
            timeout: Maximum time in seconds for scraping operations

        Raises:
            ValueError: If URL fails security validation
        """
        self.url = url
        self.timeout = timeout
        self.output_dir = Path("style-configs")

        # Validate URL using security tool
        scraper_tool = WebScraperTool(timeout=timeout)
        try:
            scraper_tool.validate_url(url)
        except SecurityError as e:
            raise ValueError(f"Invalid URL: {str(e)}") from e

        # Initialize state
        self._state = StyleScrapingState(url=url)

    def get_state(self) -> StyleScrapingState:
        """Get current flow state."""
        return self._state

    def start(self) -> EventStyleConfig:
        """
        Start the style extraction process.

        This method initializes the StyleExtractionCrew and executes
        the scraping workflow.

        Returns:
            EventStyleConfig: Extracted style configuration

        Raises:
            Exception: If scraping fails or JSON parsing fails
        """
        try:
            # Update state to scraping
            self._state.status = "scraping"

            # Initialize and run crew
            crew_instance = StyleExtractionCrew(url=self.url, timeout=self.timeout)
            result = crew_instance.crew().kickoff()

            # Log API token usage for cost tracking
            if hasattr(result, 'token_usage') and result.token_usage:
                tokens = result.token_usage
                estimated_cost = tokens * 0.00002  # Rough estimate: $0.02 per 1K tokens
                print(f"\n💰 API Cost Tracking:")
                print(f"   Tokens used: {tokens:,}")
                print(f"   Estimated cost: ${estimated_cost:.4f}")
            elif hasattr(result, 'usage_metrics') and result.usage_metrics:
                # Alternative attribute name
                print(f"\n💰 API Cost Tracking:")
                print(f"   Usage metrics: {result.usage_metrics}")

            # Get Pydantic output directly from CrewAI (output_pydantic configured on final task)
            if hasattr(result, 'pydantic') and result.pydantic:
                config = result.pydantic
            elif hasattr(result, 'json_dict') and result.json_dict:
                # Fallback: parse from json_dict
                config = EventStyleConfig(**result.json_dict)
            elif hasattr(result, 'raw') and result.raw:
                # Fallback: try parsing raw as JSON
                try:
                    config_data = json.loads(result.raw)
                    config = EventStyleConfig(**config_data)
                except (json.JSONDecodeError, TypeError, ValueError) as parse_error:
                    raise ValueError(f"Failed to parse crew output as JSON: {parse_error}. Output: {result.raw[:500]}")
            else:
                raise ValueError("Crew result has no valid output (no pydantic, json_dict, or raw)")

            # Update state to completed
            self._state.status = "completed"
            self._state.result = config

            return config

        except Exception as e:
            # Update state to failed
            self._state.status = "failed"
            self._state.error = str(e)
            raise

    def export_config(self, config: EventStyleConfig) -> Path:
        """
        Export style configuration to JSON file.

        Args:
            config: EventStyleConfig to export

        Returns:
            Path: Path to the exported JSON file
        """
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from event_id
        filename = f"{config.event_id}.json"
        output_path = self.output_dir / filename

        # Write JSON file with proper formatting
        with open(output_path, 'w') as f:
            json.dump(
                config.model_dump(),
                f,
                indent=2,
                ensure_ascii=False
            )

        return output_path
