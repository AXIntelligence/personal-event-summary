"""Tests for StyleScrapingFlow - Flow orchestration for style extraction."""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from pydantic import ValidationError
import tempfile
import shutil

from event_style_scraper.flows.style_scraping_flow import (
    StyleScrapingFlow,
    StyleScrapingState,
)
from event_style_scraper.types import EventStyleConfig, ColorPalette, Typography, BrandVoice, LayoutConfig


def create_test_config(event_id="test"):
    """Helper function to create a test EventStyleConfig."""
    return EventStyleConfig(
        event_id=event_id,
        event_name="Test Event",
        source_url="https://example.com",
        colors=ColorPalette(
            primary="#667eea",
            secondary="#764ba2",
            accent="#f093fb",
            background="#ffffff",
            text="#1a202c"
        ),
        typography=Typography(
            heading_font="Inter, sans-serif",
            body_font="system-ui, sans-serif"
        ),
        brand_voice=BrandVoice(
            tone="professional",
            style="modern",
            keywords=["test"]
        )
    )


class TestStyleScrapingState:
    """Test suite for StyleScrapingState Pydantic model."""

    def test_state_initializes_with_url(self):
        """Test that state can be created with just a URL."""
        state = StyleScrapingState(url="https://example.com")

        assert state.url == "https://example.com"
        assert state.status == "pending"
        assert state.result is None
        assert state.error is None

    def test_state_validates_url_format(self):
        """Test that state validates URL format."""
        # Valid URLs should work
        state = StyleScrapingState(url="https://example.com")
        assert state.url == "https://example.com"

        state = StyleScrapingState(url="http://test.org")
        assert state.url == "http://test.org"

    def test_state_status_transitions(self):
        """Test that state can transition through valid statuses."""
        state = StyleScrapingState(url="https://example.com")

        # Start as pending
        assert state.status == "pending"

        # Can transition to scraping
        state.status = "scraping"
        assert state.status == "scraping"

        # Can transition to completed
        state.status = "completed"
        assert state.status == "completed"

        # Can transition to failed
        state.status = "failed"
        assert state.status == "failed"

    def test_state_stores_result(self):
        """Test that state can store EventStyleConfig result."""
        config = EventStyleConfig(
            event_id="test-event",
            event_name="Test Event",
            source_url="https://example.com",
            colors=ColorPalette(
                primary="#667eea",
                secondary="#764ba2",
                accent="#f093fb",
                background="#ffffff",
                text="#1a202c"
            ),
            typography=Typography(
                heading_font="Inter, sans-serif",
                body_font="system-ui, sans-serif"
            ),
            brand_voice=BrandVoice(
                tone="professional, energetic",
                style="modern",
                keywords=["innovation", "technology"]
            )
        )

        state = StyleScrapingState(
            url="https://example.com",
            status="completed",
            result=config
        )

        assert state.result is not None
        assert state.result.event_id == "test-event"
        assert state.result.colors.primary == "#667eea"

    def test_state_stores_error(self):
        """Test that state can store error messages."""
        state = StyleScrapingState(
            url="https://example.com",
            status="failed",
            error="Connection timeout"
        )

        assert state.error == "Connection timeout"
        assert state.status == "failed"


class TestStyleScrapingFlow:
    """Test suite for StyleScrapingFlow orchestration."""

    def test_flow_initializes_with_url(self):
        """Test that flow can be created with a URL."""
        flow = StyleScrapingFlow(url="https://example.com")

        assert flow.url == "https://example.com"
        assert flow.timeout == 60  # Default timeout

    def test_flow_initializes_with_custom_timeout(self):
        """Test that flow accepts custom timeout."""
        flow = StyleScrapingFlow(
            url="https://example.com",
            timeout=120
        )

        assert flow.timeout == 120

    def test_flow_validates_url_on_init(self):
        """Test that flow validates URL during initialization."""
        # Valid URLs should work
        flow = StyleScrapingFlow(url="https://example.com")
        assert flow.url == "https://example.com"

        # Invalid URLs should raise ValueError
        with pytest.raises(ValueError, match="Invalid URL"):
            StyleScrapingFlow(url="file:///etc/passwd")

        with pytest.raises(ValueError, match="not allowed"):
            StyleScrapingFlow(url="http://localhost:8080")

    def test_flow_creates_initial_state(self):
        """Test that flow creates initial state correctly."""
        flow = StyleScrapingFlow(url="https://example.com")
        state = flow.get_state()

        assert state.url == "https://example.com"
        assert state.status == "pending"
        assert state.result is None
        assert state.error is None

    def test_flow_has_output_directory(self):
        """Test that flow has output directory configured."""
        flow = StyleScrapingFlow(url="https://example.com")

        assert hasattr(flow, "output_dir")
        assert isinstance(flow.output_dir, Path)
        assert flow.output_dir.name == "style-configs"

    @patch("event_style_scraper.flows.style_scraping_flow.StyleExtractionCrew")
    def test_start_method_exists(self, mock_crew_class):
        """Test that flow has a start() method."""
        flow = StyleScrapingFlow(url="https://example.com")

        assert hasattr(flow, "start")
        assert callable(flow.start)

    @patch("event_style_scraper.flows.style_scraping_flow.StyleExtractionCrew")
    def test_start_updates_state_to_scraping(self, mock_crew_class):
        """Test that start() updates state to 'scraping'."""
        config = create_test_config()

        mock_crew_instance = Mock()
        mock_crew_obj = Mock()
        mock_result = Mock()
        mock_result.pydantic = config
        mock_crew_obj.kickoff.return_value = mock_result
        mock_crew_instance.crew.return_value = mock_crew_obj
        mock_crew_class.return_value = mock_crew_instance

        flow = StyleScrapingFlow(url="https://example.com")

        # State should start as pending
        assert flow.get_state().status == "pending"

        # After calling start, state should transition
        flow.start()

        # Verify crew was initialized with correct URL
        mock_crew_class.assert_called_once_with(
            url="https://example.com",
            timeout=60
        )

    @patch("event_style_scraper.flows.style_scraping_flow.StyleExtractionCrew")
    def test_start_calls_crew_kickoff(self, mock_crew_class):
        """Test that start() calls crew.kickoff()."""
        config = create_test_config()

        mock_crew_instance = Mock()
        mock_crew_obj = Mock()
        mock_result = Mock()
        mock_result.pydantic = config
        mock_crew_obj.kickoff.return_value = mock_result
        mock_crew_instance.crew.return_value = mock_crew_obj
        mock_crew_class.return_value = mock_crew_instance

        flow = StyleScrapingFlow(url="https://example.com")
        flow.start()

        # Verify crew() and kickoff() were called
        mock_crew_instance.crew.assert_called_once()
        mock_crew_obj.kickoff.assert_called_once()

    @patch("event_style_scraper.flows.style_scraping_flow.StyleExtractionCrew")
    def test_start_returns_event_style_config(self, mock_crew_class):
        """Test that start() returns EventStyleConfig on success."""
        config = create_test_config(event_id="example-com")

        mock_crew_instance = Mock()
        mock_crew_obj = Mock()
        mock_result = Mock()
        mock_result.pydantic = config
        mock_crew_obj.kickoff.return_value = mock_result
        mock_crew_instance.crew.return_value = mock_crew_obj
        mock_crew_class.return_value = mock_crew_instance

        flow = StyleScrapingFlow(url="https://example.com")
        result = flow.start()

        assert isinstance(result, EventStyleConfig)
        assert result.event_id == "example-com"
        assert result.colors.primary == "#667eea"

    @patch("event_style_scraper.flows.style_scraping_flow.StyleExtractionCrew")
    def test_start_updates_state_on_success(self, mock_crew_class):
        """Test that start() updates state to 'completed' on success."""
        config = create_test_config()

        mock_crew_instance = Mock()
        mock_crew_obj = Mock()
        mock_result = Mock()
        mock_result.pydantic = config
        mock_crew_obj.kickoff.return_value = mock_result
        mock_crew_instance.crew.return_value = mock_crew_obj
        mock_crew_class.return_value = mock_crew_instance

        flow = StyleScrapingFlow(url="https://example.com")
        result = flow.start()

        state = flow.get_state()
        assert state.status == "completed"
        assert state.result is not None
        assert state.error is None

    @patch("event_style_scraper.flows.style_scraping_flow.StyleExtractionCrew")
    def test_start_handles_crew_failure(self, mock_crew_class):
        """Test that start() handles crew failures gracefully."""
        mock_crew_instance = Mock()
        mock_crew_obj = Mock()
        mock_crew_obj.kickoff.side_effect = Exception("Connection timeout")
        mock_crew_instance.crew.return_value = mock_crew_obj
        mock_crew_class.return_value = mock_crew_instance

        flow = StyleScrapingFlow(url="https://example.com")

        with pytest.raises(Exception, match="Connection timeout"):
            flow.start()

        state = flow.get_state()
        assert state.status == "failed"
        assert "Connection timeout" in state.error

    @patch("event_style_scraper.flows.style_scraping_flow.StyleExtractionCrew")
    def test_start_handles_invalid_json(self, mock_crew_class):
        """Test that start() handles invalid JSON from crew."""
        mock_crew_instance = Mock()
        mock_crew_obj = Mock()
        mock_result = Mock()
        # No pydantic, no json_dict, only invalid raw
        mock_result.pydantic = None
        mock_result.json_dict = None
        mock_result.raw = "not valid json"
        mock_crew_obj.kickoff.return_value = mock_result
        mock_crew_instance.crew.return_value = mock_crew_obj
        mock_crew_class.return_value = mock_crew_instance

        flow = StyleScrapingFlow(url="https://example.com")

        with pytest.raises(Exception):
            flow.start()

        state = flow.get_state()
        assert state.status == "failed"
        assert state.error is not None


class TestStyleScrapingFlowExport:
    """Test suite for StyleScrapingFlow export functionality."""

    def test_export_config_method_exists(self):
        """Test that flow has an export_config() method."""
        flow = StyleScrapingFlow(url="https://example.com")

        assert hasattr(flow, "export_config")
        assert callable(flow.export_config)

    def test_export_config_creates_output_directory(self):
        """Test that export_config creates style-configs directory if missing."""
        # Use a temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            test_output_dir = Path(tmpdir) / "style-configs"

            flow = StyleScrapingFlow(url="https://example.com")
            flow.output_dir = test_output_dir

            # Create a test config
            config = EventStyleConfig(
                event_id="test-event",
                event_name="Test Event",
                source_url="https://example.com",
                colors=ColorPalette(
                    primary="#667eea",
                    secondary="#764ba2",
                    accent="#f093fb",
                    background="#ffffff",
                    text="#1a202c"
                ),
                typography=Typography(
                    heading_font="Inter, sans-serif",
                    body_font="system-ui, sans-serif"
                ),
                brand_voice=BrandVoice(
                    tone="professional",
                    style="modern",
                    keywords=["test"]
                )
            )

            # Directory shouldn't exist yet
            assert not test_output_dir.exists()

            # Export should create it
            flow.export_config(config)

            # Directory should now exist
            assert test_output_dir.exists()
            assert test_output_dir.is_dir()

    def test_export_config_writes_json_file(self):
        """Test that export_config writes JSON file with correct name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_output_dir = Path(tmpdir) / "style-configs"

            flow = StyleScrapingFlow(url="https://example.com")
            flow.output_dir = test_output_dir

            config = EventStyleConfig(
                event_id="test-event",
                event_name="Test Event",
                source_url="https://example.com",
                colors=ColorPalette(
                    primary="#667eea",
                    secondary="#764ba2",
                    accent="#f093fb",
                    background="#ffffff",
                    text="#1a202c"
                ),
                typography=Typography(
                    heading_font="Inter, sans-serif",
                    body_font="system-ui, sans-serif"
                ),
                brand_voice=BrandVoice(
                    tone="professional",
                    style="modern",
                    keywords=["test"]
                )
            )

            output_path = flow.export_config(config)

            # File should exist
            assert output_path.exists()
            assert output_path.is_file()
            assert output_path.name == "test-event.json"
            assert output_path.parent == test_output_dir

    def test_export_config_writes_valid_json(self):
        """Test that exported JSON is valid and complete."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_output_dir = Path(tmpdir) / "style-configs"

            flow = StyleScrapingFlow(url="https://example.com")
            flow.output_dir = test_output_dir

            config = EventStyleConfig(
                event_id="example-com",
                event_name="Example Event",
                source_url="https://example.com",
                colors=ColorPalette(
                    primary="#667eea",
                    secondary="#764ba2",
                    accent="#f093fb",
                    background="#ffffff",
                    text="#1a202c"
                ),
                typography=Typography(
                    heading_font="Inter, sans-serif",
                    body_font="system-ui, sans-serif",
                    heading_size="2rem",
                    body_size="1rem",
                    line_height="1.6"
                ),
                brand_voice=BrandVoice(
                    tone="professional, energetic",
                    style="modern",
                    keywords=["innovation", "technology"]
                )
            )

            output_path = flow.export_config(config)

            # Read and parse JSON
            with open(output_path) as f:
                data = json.load(f)

            # Verify all fields present
            assert data["event_id"] == "example-com"
            assert data["event_name"] == "Example Event"
            assert data["source_url"] == "https://example.com"
            assert data["colors"]["primary"] == "#667eea"
            assert data["typography"]["heading_font"] == "Inter, sans-serif"
            assert data["brand_voice"]["tone"] == "professional, energetic"

    def test_export_config_returns_path(self):
        """Test that export_config returns the output path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_output_dir = Path(tmpdir) / "style-configs"

            flow = StyleScrapingFlow(url="https://example.com")
            flow.output_dir = test_output_dir

            config = EventStyleConfig(
                event_id="test",
                event_name="Test",
                source_url="https://example.com",
                colors=ColorPalette(
                    primary="#667eea",
                    secondary="#764ba2",
                    accent="#f093fb",
                    background="#ffffff",
                    text="#1a202c"
                ),
                typography=Typography(
                    heading_font="Inter, sans-serif",
                    body_font="system-ui, sans-serif"
                ),
                brand_voice=BrandVoice(
                    tone="professional",
                    style="modern",
                    keywords=["test"]
                )
            )

            output_path = flow.export_config(config)

            assert isinstance(output_path, Path)
            assert output_path.exists()

    def test_export_config_overwrites_existing_file(self):
        """Test that export_config overwrites existing config files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_output_dir = Path(tmpdir) / "style-configs"
            test_output_dir.mkdir(parents=True)

            flow = StyleScrapingFlow(url="https://example.com")
            flow.output_dir = test_output_dir

            # Create first config
            config1 = EventStyleConfig(
                event_id="test",
                event_name="Test Version 1",
                source_url="https://example.com",
                colors=ColorPalette(
                    primary="#000000",
                    secondary="#111111",
                    accent="#222222",
                    background="#ffffff",
                    text="#1a202c"
                ),
                typography=Typography(
                    heading_font="Arial, sans-serif",
                    body_font="Arial, sans-serif"
                ),
                brand_voice=BrandVoice(
                    tone="formal",
                    style="traditional",
                    keywords=["old"]
                )
            )

            flow.export_config(config1)

            # Create second config with same event_id
            config2 = EventStyleConfig(
                event_id="test",
                event_name="Test Version 2",
                source_url="https://example.com",
                colors=ColorPalette(
                    primary="#667eea",
                    secondary="#764ba2",
                    accent="#f093fb",
                    background="#ffffff",
                    text="#1a202c"
                ),
                typography=Typography(
                    heading_font="Inter, sans-serif",
                    body_font="system-ui, sans-serif"
                ),
                brand_voice=BrandVoice(
                    tone="professional",
                    style="modern",
                    keywords=["new"]
                )
            )

            output_path = flow.export_config(config2)

            # Read file and verify it has latest data
            with open(output_path) as f:
                data = json.load(f)

            assert data["event_name"] == "Test Version 2"
            assert data["colors"]["primary"] == "#667eea"
            assert data["brand_voice"]["keywords"] == ["new"]
