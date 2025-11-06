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

    def test_crew_has_agents(self):
        """Test crew has required agents."""
        crew = StyleExtractionCrew(url="https://example.com")
        agents = crew.agents()

        # Should have 4 agents
        assert len(agents) == 4

        # Check agent roles
        agent_roles = [agent.role for agent in agents]
        assert "Web Content Scraper" in agent_roles
        assert "Style and Design Analyst" in agent_roles
        assert "Brand Voice and Tone Analyst" in agent_roles
        assert "Style Configuration Compiler" in agent_roles

    def test_crew_has_tasks(self):
        """Test crew has required tasks."""
        crew = StyleExtractionCrew(url="https://example.com")
        tasks = crew.tasks()

        # Should have 4 tasks
        assert len(tasks) == 4

        # Check task descriptions contain key actions
        task_descriptions = [task.description for task in tasks]
        descriptions_text = " ".join(task_descriptions)
        assert "scrape" in descriptions_text.lower()
        assert "extract" in descriptions_text.lower() or "color" in descriptions_text.lower()
        assert "voice" in descriptions_text.lower() or "tone" in descriptions_text.lower()
        assert "compile" in descriptions_text.lower()

    def test_crew_loads_config_files(self):
        """Test crew loads agents.yaml and tasks.yaml."""
        crew = StyleExtractionCrew(url="https://example.com")

        # Agents should be loaded from YAML
        agents = crew.agents()
        assert len(agents) > 0

        # Tasks should be loaded from YAML
        tasks = crew.tasks()
        assert len(tasks) > 0

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

    @patch('event_style_scraper.crews.style_extraction_crew.style_extraction_crew.Crew')
    def test_crew_kickoff_returns_result(self, mock_crew_class):
        """Test crew kickoff returns a result."""
        # Mock the Crew class
        mock_crew_instance = Mock()
        mock_crew_instance.kickoff.return_value = Mock(
            raw='{"event_id": "test", "event_name": "Test Event"}'
        )
        mock_crew_class.return_value = mock_crew_instance

        crew = StyleExtractionCrew(url="https://example.com")
        result = crew.kickoff()

        # Should call crew kickoff
        assert result is not None

    def test_crew_with_timeout(self):
        """Test crew respects timeout configuration."""
        crew = StyleExtractionCrew(url="https://example.com", timeout=30)
        assert crew.timeout == 30

    def test_crew_default_timeout(self):
        """Test crew has default timeout."""
        crew = StyleExtractionCrew(url="https://example.com")
        assert crew.timeout == 60  # Default 60 seconds
