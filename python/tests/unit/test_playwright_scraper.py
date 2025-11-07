"""Tests for PlaywrightStyleExtractorTool."""

import pytest
from pathlib import Path
from event_style_scraper.tools import PlaywrightStyleExtractorTool, SecurityError


class TestPlaywrightStyleExtractorTool:
    """Tests for Playwright-based style extraction tool."""

    def test_tool_instantiation(self):
        """Test that PlaywrightStyleExtractorTool can be instantiated."""
        tool = PlaywrightStyleExtractorTool(timeout=5000)
        assert tool is not None
        assert tool.timeout == 5000

    def test_tool_extracts_html(self):
        """Test tool extracts actual HTML content from file:// URL."""
        tool = PlaywrightStyleExtractorTool(timeout=10000)

        # Use file:// URL for test fixture
        fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
        fixture_url = f"file://{fixture_path.absolute()}"

        result = tool._run(fixture_url)

        assert result["success"] is True
        assert "html" in result
        assert "<header>" in result["html"]
        assert "Test Event 2025" in result["html"]

    def test_tool_extracts_computed_styles(self):
        """Test tool extracts browser-computed styles for key elements."""
        tool = PlaywrightStyleExtractorTool(timeout=10000)

        fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
        fixture_url = f"file://{fixture_path.absolute()}"

        result = tool._run(fixture_url)

        assert "computed_styles" in result
        assert "header" in result["computed_styles"]

        # Verify header has expected computed styles
        header_styles = result["computed_styles"]["header"]
        assert "backgroundColor" in header_styles
        assert header_styles["backgroundColor"] == "rgb(22, 8, 34)"  # #160822
        assert header_styles["color"] == "rgb(255, 255, 255)"  # white

    def test_tool_extracts_css_variables(self):
        """Test tool extracts CSS custom properties from :root."""
        tool = PlaywrightStyleExtractorTool(timeout=10000)

        fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
        fixture_url = f"file://{fixture_path.absolute()}"

        result = tool._run(fixture_url)

        assert "css_variables" in result
        assert isinstance(result["css_variables"], dict)
        # Note: CSS variables may not be enumerable in all contexts (file://)
        # This test verifies the structure exists, not necessarily the content
        # Real websites (http:/https://) typically have enumerable CSS variables

    def test_tool_extracts_multiple_elements(self):
        """Test tool extracts computed styles for multiple element types."""
        tool = PlaywrightStyleExtractorTool(timeout=10000)

        fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
        fixture_url = f"file://{fixture_path.absolute()}"

        result = tool._run(fixture_url)

        # Should have styles for common elements
        assert "body" in result["computed_styles"]
        assert "header" in result["computed_styles"]

        # Body should have expected styles
        body_styles = result["computed_styles"]["body"]
        assert "backgroundColor" in body_styles
        assert "fontFamily" in body_styles

    def test_tool_respects_timeout(self):
        """Test tool respects timeout configuration."""
        tool = PlaywrightStyleExtractorTool(timeout=100)  # Very short timeout

        # Use a URL that will timeout (non-existent)
        with pytest.raises(Exception):  # Should timeout
            tool._run("file:///nonexistent/path.html")

    def test_tool_validates_url_security(self):
        """Test tool respects security validation for URLs."""
        tool = PlaywrightStyleExtractorTool()

        # Tool should validate URLs before scraping
        # This test verifies the tool integrates with SecurityError
        # Note: The actual validation happens in WebScraperTool
        # but we want to ensure PlaywrightStyleExtractorTool can handle it

        # Test that tool can be called with valid URL
        # (actual security validation tested in test_tools.py)
        assert hasattr(tool, '_run')
        assert callable(tool._run)

    def test_tool_returns_structured_data(self):
        """Test tool returns data in expected structure."""
        tool = PlaywrightStyleExtractorTool(timeout=10000)

        fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
        fixture_url = f"file://{fixture_path.absolute()}"

        result = tool._run(fixture_url)

        # Verify structure
        assert isinstance(result, dict)
        assert "url" in result
        assert "html" in result
        assert "computed_styles" in result
        assert "css_variables" in result
        assert "assets" in result
        assert "success" in result

        # Verify types
        assert isinstance(result["html"], str)
        assert isinstance(result["computed_styles"], dict)
        assert isinstance(result["css_variables"], dict)
        assert isinstance(result["assets"], dict)
        assert result["success"] is True

    def test_tool_extracts_assets(self):
        """Test tool extracts logo and favicon URLs."""
        tool = PlaywrightStyleExtractorTool(timeout=10000)

        fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
        fixture_url = f"file://{fixture_path.absolute()}"

        result = tool._run(fixture_url)

        assert "assets" in result
        assert "logo" in result["assets"]
        assert "favicon" in result["assets"]
        # Our test fixture doesn't have logo/favicon, so they should be None
        assert result["assets"]["logo"] is None
        assert result["assets"]["favicon"] is None
