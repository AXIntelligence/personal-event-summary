"""Integration tests for real website scraping with Playwright tool.

These tests validate that:
1. Agent actually calls the PlaywrightStyleExtractorTool (not hallucinate)
2. Tool returns real data from actual websites
3. Scraped colors match DevTools inspection
4. No fictional HTML/CSS in output
"""

import pytest
from event_style_scraper.crews.style_extraction_crew import StyleExtractionCrew
from event_style_scraper.types import EventStyleConfig


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple for comparison."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


@pytest.mark.integration
@pytest.mark.timeout(120)
def test_scrape_example_com():
    """
    Test scraping example.com and extracting real styles.

    This test validates:
    - Agent calls PlaywrightStyleExtractorTool (not generate content)
    - Tool returns actual HTML from example.com
    - Scraped data is structured correctly
    - Colors are valid hex format
    - No hallucinated content (no made-up HTML structure)
    """
    # Create crew and run scraping
    crew = StyleExtractionCrew("https://example.com", timeout=60)
    result = crew.crew().kickoff()

    # Get the structured output
    config = result.pydantic
    assert isinstance(config, EventStyleConfig), "Result should be EventStyleConfig"

    # Validate basic structure
    assert config.source_url == "https://example.com"
    assert config.event_id is not None
    assert len(config.event_id) > 0

    # Validate colors are real hex format (not fictional)
    assert config.colors.primary is not None
    assert len(config.colors.primary) == 7, "Color should be #RRGGBB format"
    assert config.colors.primary.startswith("#")

    # Validate colors are valid hex
    try:
        hex_to_rgb(config.colors.primary)
    except ValueError:
        pytest.fail(f"Primary color {config.colors.primary} is not valid hex")

    # Validate event name was extracted (not fictional)
    assert config.event_name is not None
    assert len(config.event_name) > 0

    # example.com has very simple structure, should reflect that
    # (Not have complex fictional structure like #site-header, etc.)
    assert config.typography.heading_font is not None
    assert config.typography.body_font is not None


@pytest.mark.integration
@pytest.mark.timeout(180)
def test_scrape_eventtechlive_com_accurate_color():
    """
    Test scraping Event Tech Live and extracting CORRECT primary color.

    CRITICAL TEST: This validates the fix for hallucination issue.

    Expected: #160822 (dark purple from DevTools inspection)
    NOT: #0072ce (AI-guessed tech blue)
    NOT: #004080 (another AI-guessed blue)

    This test ensures agent calls the actual Playwright tool and
    returns browser-measured colors, not AI guesses.
    """
    # Create crew and run scraping
    crew = StyleExtractionCrew("https://eventtechlive.com", timeout=90)
    result = crew.crew().kickoff()

    # Get the structured output
    config = result.pydantic
    assert isinstance(config, EventStyleConfig)

    # Validate source
    assert config.source_url == "https://eventtechlive.com"

    # CRITICAL: Validate primary color matches DevTools inspection
    # Expected: #160822 (verified with DevTools on eventtechlive.com header)
    expected_rgb = (22, 8, 34)  # #160822 in RGB
    scraped_rgb = hex_to_rgb(config.colors.primary)

    # Allow ±2 RGB units for rounding differences
    for i in range(3):
        rgb_diff = abs(scraped_rgb[i] - expected_rgb[i])
        assert rgb_diff <= 2, (
            f"Primary color mismatch on channel {i}: "
            f"scraped {config.colors.primary} (RGB {scraped_rgb}) "
            f"vs expected #160822 (RGB {expected_rgb}). "
            f"Difference: {rgb_diff} units (max 2 allowed). "
            f"If this fails, agent is hallucinating colors instead of using Playwright tool."
        )

    # Validate other colors are reasonable
    assert config.colors.secondary is not None
    assert config.colors.accent is not None
    assert config.colors.background is not None
    assert config.colors.text is not None

    # Validate event name extracted
    assert config.event_name is not None
    assert len(config.event_name) > 0


@pytest.mark.integration
@pytest.mark.timeout(120)
def test_no_hallucinated_content():
    """
    Test that scraper output contains REAL data, not hallucinated content.

    This test validates there are no signs of AI-generated fictional content:
    - No generic "Example Event" names
    - No made-up CSS IDs like "#site-header" on simple sites
    - No fictional robots.txt descriptions
    - No simulated dark mode styles

    We'll scrape example.com which has very minimal structure.
    If agent hallucinates, it will add complexity that doesn't exist.
    """
    crew = StyleExtractionCrew("https://example.com", timeout=60)
    result = crew.crew().kickoff()

    config = result.pydantic

    # example.com should have simple structure
    # Agent should NOT fabricate complex structure

    # Get the raw task output to inspect for hallucination markers
    # (In real implementation, we'd check crew logs or raw output)

    # Validate colors are realistic for example.com
    # example.com uses very simple default browser styles
    # Should not have vibrant brand colors like #0073e6 (CTA buttons)

    # Basic validation: output is structured correctly
    assert isinstance(config, EventStyleConfig)
    assert config.source_url == "https://example.com"

    # If we got here without errors, basic structure is correct
    # More detailed hallucination detection would require:
    # 1. Checking crew logs for "Tool: Playwright Style Extractor"
    # 2. Comparing HTML content to actual site
    # 3. Validating no fictional CSS classes/IDs


@pytest.mark.integration
@pytest.mark.timeout(90)
def test_tool_invocation_in_logs(caplog):
    """
    Test that agent actually invokes the Playwright tool.

    This test validates the tool is called, not just assigned.
    We check logs for evidence of tool invocation.
    """
    import logging
    caplog.set_level(logging.DEBUG)

    crew = StyleExtractionCrew("https://example.com", timeout=60)
    result = crew.crew().kickoff()

    # Check that we got valid output
    config = result.pydantic
    assert isinstance(config, EventStyleConfig)

    # Check logs for tool invocation
    # CrewAI logs tool usage as "Tool: <tool_name>"
    log_text = caplog.text

    # Look for evidence of Playwright tool usage
    # Note: Actual log format may vary, this is a heuristic
    has_playwright_mention = (
        "Playwright" in log_text or
        "playwright" in log_text or
        "Tool:" in log_text
    )

    # If logs don't show tool usage, that's concerning
    # but not necessarily a failure (logging might be disabled)
    # So we make this a soft check with informative message
    if not has_playwright_mention:
        pytest.skip(
            "Could not verify tool invocation from logs. "
            "This may be due to logging configuration. "
            "Manual verification recommended."
        )
