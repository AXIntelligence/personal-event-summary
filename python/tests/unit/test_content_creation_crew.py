"""Tests for ContentCreationCrew - Multi-agent content generation."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import json

from event_style_scraper.crews.content_creation_crew import ContentCreationCrew
from event_style_scraper.types import EventStyleConfig, ColorPalette, Typography, BrandVoice


class TestContentCreationCrew:
    """Test suite for ContentCreationCrew."""

    def test_crew_initializes_with_attendee_and_style(self):
        """Test that crew can be created with attendee data and style config."""
        attendee_data = {
            "id": "1001",
            "firstName": "Jane",
            "lastName": "Doe",
            "sessions": []
        }

        style_config = EventStyleConfig(
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
                keywords=["innovation"]
            )
        )

        crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        assert crew.attendee_data == attendee_data
        assert crew.style_config == style_config

    def test_crew_loads_yaml_configs(self):
        """Test that crew loads agents.yaml and tasks.yaml configurations."""
        attendee_data = {"id": "1001", "firstName": "Jane"}
        style_config = EventStyleConfig(
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

        crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        assert hasattr(crew, "agents_config")
        assert hasattr(crew, "tasks_config")
        assert crew.agents_config is not None
        assert crew.tasks_config is not None

    def test_crew_has_agent_methods(self):
        """Test that crew has individual agent methods."""
        attendee_data = {"id": "1001", "firstName": "Jane"}
        style_config = EventStyleConfig(
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

        crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        # Check that agent methods exist
        assert hasattr(crew, "content_writer_agent")
        assert hasattr(crew, "personalization_agent")
        assert hasattr(crew, "brand_voice_agent")
        assert hasattr(crew, "quality_editor_agent")

    def test_crew_agent_methods_are_callable(self):
        """Test that agent methods can be called."""
        attendee_data = {"id": "1001", "firstName": "Jane"}
        style_config = EventStyleConfig(
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

        crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        # Verify methods are callable
        assert callable(crew.content_writer_agent)
        assert callable(crew.personalization_agent)
        assert callable(crew.brand_voice_agent)
        assert callable(crew.quality_editor_agent)

    def test_crew_has_task_methods(self):
        """Test that crew has individual task methods."""
        attendee_data = {"id": "1001", "firstName": "Jane"}
        style_config = EventStyleConfig(
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

        crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        # Check that task methods exist
        assert hasattr(crew, "analyze_attendee")
        assert hasattr(crew, "generate_content")
        assert hasattr(crew, "apply_brand_voice")
        assert hasattr(crew, "quality_check")

    def test_crew_task_methods_are_callable(self):
        """Test that task methods can be called."""
        attendee_data = {"id": "1001", "firstName": "Jane"}
        style_config = EventStyleConfig(
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

        crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        # Verify methods are callable
        assert callable(crew.analyze_attendee)
        assert callable(crew.generate_content)
        assert callable(crew.apply_brand_voice)
        assert callable(crew.quality_check)

    def test_crew_has_crew_method(self):
        """Test that crew has crew() method to build Crew object."""
        attendee_data = {"id": "1001", "firstName": "Jane"}
        style_config = EventStyleConfig(
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

        crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        assert hasattr(crew, "crew")
        assert callable(crew.crew)

    def test_crew_method_returns_crew_instance(self):
        """Test that crew() method returns a Crew instance."""
        attendee_data = {"id": "1001", "firstName": "Jane"}
        style_config = EventStyleConfig(
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

        content_crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        # The crew() method should return a Crew instance
        crew_instance = content_crew.crew()
        assert crew_instance is not None
        assert hasattr(crew_instance, "kickoff")

    def test_crew_config_directory_exists(self):
        """Test that crew has config directory with YAML files."""
        attendee_data = {"id": "1001", "firstName": "Jane"}
        style_config = EventStyleConfig(
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

        crew = ContentCreationCrew(
            attendee_data=attendee_data,
            style_config=style_config
        )

        assert hasattr(crew, "config_dir")
        assert isinstance(crew.config_dir, Path)
        assert crew.config_dir.name == "config"
