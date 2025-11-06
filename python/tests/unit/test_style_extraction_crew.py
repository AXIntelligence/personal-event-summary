"""Tests for StyleExtractionCrew."""

import pytest
from unittest.mock import Mock, patch
from event_style_scraper.types import EventStyleConfig
from event_style_scraper.crews.style_extraction_crew.style_extraction_crew import (
    StyleExtractionCrew,
)


class TestStyleExtractionCrew:
    """Tests for StyleExtractionCrew initialization and configuration."""

    def test_crew_initializes_with_url(self):
        """Test crew can be initialized with a URL."""
        crew = StyleExtractionCrew(url="https://example.com")
        assert crew.url == "https://example.com"

    def test_crew_has_agent_methods(self):
        """Test crew has required agent methods."""
        crew = StyleExtractionCrew(url="https://example.com")

        # Should have 4 agent methods
        assert hasattr(crew, "web_scraper_agent")
        assert hasattr(crew, "style_analyst_agent")
        assert hasattr(crew, "voice_analyst_agent")
        assert hasattr(crew, "compiler_agent")

        # Methods should be callable
        assert callable(crew.web_scraper_agent)
        assert callable(crew.style_analyst_agent)
        assert callable(crew.voice_analyst_agent)
        assert callable(crew.compiler_agent)

    def test_crew_has_task_methods(self):
        """Test crew has required task methods."""
        crew = StyleExtractionCrew(url="https://example.com")

        # Should have 4 task methods
        assert hasattr(crew, "scrape_website")
        assert hasattr(crew, "extract_styles")
        assert hasattr(crew, "analyze_voice")
        assert hasattr(crew, "compile_config")

        # Methods should be callable
        assert callable(crew.scrape_website)
        assert callable(crew.extract_styles)
        assert callable(crew.analyze_voice)
        assert callable(crew.compile_config)

    def test_crew_loads_config_files(self):
        """Test crew loads agents.yaml and tasks.yaml."""
        crew = StyleExtractionCrew(url="https://example.com")

        # Config should be loaded
        assert hasattr(crew, "agents_config")
        assert hasattr(crew, "tasks_config")
        assert crew.agents_config is not None
        assert crew.tasks_config is not None

    def test_crew_validates_url(self):
        """Test crew validates URL before processing."""
        with pytest.raises(ValueError, match="Invalid URL"):
            StyleExtractionCrew(url="not-a-valid-url")

    def test_crew_rejects_localhost(self):
        """Test crew rejects localhost URLs."""
        with pytest.raises(ValueError, match="not allowed"):
            StyleExtractionCrew(url="http://localhost:8080")

    def test_crew_rejects_private_ips(self):
        """Test crew rejects private IP addresses."""
        with pytest.raises(ValueError, match="not allowed"):
            StyleExtractionCrew(url="http://192.168.1.1")

    def test_crew_method_returns_crew_instance(self):
        """Test crew() method returns a Crew instance."""
        crew_obj = StyleExtractionCrew(url="https://example.com")

        # The crew() method should return a Crew instance
        crew_instance = crew_obj.crew()
        assert crew_instance is not None
        assert hasattr(crew_instance, "kickoff")

    def test_crew_with_timeout(self):
        """Test crew respects timeout configuration."""
        crew = StyleExtractionCrew(url="https://example.com", timeout=30)
        assert crew.timeout == 30

    def test_crew_default_timeout(self):
        """Test crew has default timeout."""
        crew = StyleExtractionCrew(url="https://example.com")
        assert crew.timeout == 60  # Default 60 seconds
