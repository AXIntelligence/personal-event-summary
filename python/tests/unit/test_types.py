"""Tests for Pydantic data models."""

import pytest
from pydantic import ValidationError

from event_style_scraper.types import (
    ColorPalette,
    Typography,
    BrandVoice,
    LayoutConfig,
    EventStyleConfig,
)


class TestColorPalette:
    """Tests for ColorPalette model."""

    def test_color_palette_valid_data(self):
        """Test ColorPalette with valid color values."""
        palette = ColorPalette(
            primary="#667eea",
            secondary="#764ba2",
            accent="#f093fb",
            background="#ffffff",
            text="#1a202c",
        )
        assert palette.primary == "#667eea"
        assert palette.secondary == "#764ba2"
        assert palette.accent == "#f093fb"
        assert palette.background == "#ffffff"
        assert palette.text == "#1a202c"

    def test_color_palette_rgb_format(self):
        """Test ColorPalette accepts RGB format."""
        palette = ColorPalette(
            primary="rgb(102, 126, 234)",
            secondary="rgb(118, 75, 162)",
            accent="rgb(240, 147, 251)",
            background="rgb(255, 255, 255)",
            text="rgb(26, 32, 44)",
        )
        assert "rgb" in palette.primary

    def test_color_palette_invalid_format(self):
        """Test ColorPalette rejects invalid color format."""
        with pytest.raises(ValidationError):
            ColorPalette(
                primary="not-a-color",
                secondary="#764ba2",
                accent="#f093fb",
                background="#ffffff",
                text="#1a202c",
            )


class TestTypography:
    """Tests for Typography model."""

    def test_typography_valid_data(self):
        """Test Typography with valid font families."""
        typography = Typography(
            heading_font="Inter, sans-serif",
            body_font="system-ui, sans-serif",
            heading_size="2.5rem",
            body_size="1rem",
            line_height="1.5",
        )
        assert typography.heading_font == "Inter, sans-serif"
        assert typography.body_font == "system-ui, sans-serif"
        assert typography.heading_size == "2.5rem"

    def test_typography_default_values(self):
        """Test Typography uses defaults when optional fields omitted."""
        typography = Typography(
            heading_font="Inter",
            body_font="Roboto",
        )
        assert typography.heading_size == "2rem"
        assert typography.body_size == "1rem"
        assert typography.line_height == "1.6"


class TestBrandVoice:
    """Tests for BrandVoice model."""

    def test_brand_voice_valid_data(self):
        """Test BrandVoice with valid tone and keywords."""
        voice = BrandVoice(
            tone="professional",
            keywords=["innovation", "technology", "networking"],
            style="formal",
            personality="energetic",
        )
        assert voice.tone == "professional"
        assert len(voice.keywords) == 3
        assert voice.style == "formal"
        assert voice.personality == "energetic"

    def test_brand_voice_multiple_tones(self):
        """Test BrandVoice accepts comma-separated tones."""
        voice = BrandVoice(
            tone="professional, energetic, innovative",
            keywords=["tech", "events"],
            style="modern",
        )
        assert "professional" in voice.tone
        assert "energetic" in voice.tone


class TestLayoutConfig:
    """Tests for LayoutConfig model."""

    def test_layout_config_valid_data(self):
        """Test LayoutConfig with valid grid system."""
        layout = LayoutConfig(
            grid_system="12-column",
            spacing_unit="8px",
            border_radius="8px",
            container_width="1200px",
        )
        assert layout.grid_system == "12-column"
        assert layout.spacing_unit == "8px"
        assert layout.border_radius == "8px"

    def test_layout_config_defaults(self):
        """Test LayoutConfig uses defaults."""
        layout = LayoutConfig()
        assert layout.grid_system == "flexbox"
        assert layout.spacing_unit == "8px"


class TestEventStyleConfig:
    """Tests for EventStyleConfig (main model)."""

    def test_event_style_config_complete(self):
        """Test EventStyleConfig with all fields."""
        config = EventStyleConfig(
            event_id="event-2025",
            event_name="TechConf 2025",
            source_url="https://techconf.example.com",
            colors=ColorPalette(
                primary="#667eea",
                secondary="#764ba2",
                accent="#f093fb",
                background="#ffffff",
                text="#1a202c",
            ),
            typography=Typography(
                heading_font="Inter",
                body_font="Roboto",
            ),
            brand_voice=BrandVoice(
                tone="professional",
                keywords=["tech", "innovation"],
                style="modern",
            ),
            layout=LayoutConfig(
                grid_system="flexbox",
                spacing_unit="8px",
            ),
            logo_url="https://techconf.example.com/logo.png",
            favicon_url="https://techconf.example.com/favicon.ico",
        )
        assert config.event_id == "event-2025"
        assert config.event_name == "TechConf 2025"
        assert config.colors.primary == "#667eea"
        assert config.typography.heading_font == "Inter"
        assert config.brand_voice.tone == "professional"

    def test_event_style_config_missing_required_fields(self):
        """Test EventStyleConfig requires essential fields."""
        with pytest.raises(ValidationError):
            EventStyleConfig(
                event_id="event-2025",
                # Missing event_name
                source_url="https://example.com",
            )

    def test_event_style_config_to_dict(self):
        """Test EventStyleConfig serializes to dict correctly."""
        config = EventStyleConfig(
            event_id="event-2025",
            event_name="TechConf 2025",
            source_url="https://techconf.example.com",
            colors=ColorPalette(
                primary="#667eea",
                secondary="#764ba2",
                accent="#f093fb",
                background="#ffffff",
                text="#1a202c",
            ),
            typography=Typography(
                heading_font="Inter",
                body_font="Roboto",
            ),
            brand_voice=BrandVoice(
                tone="professional",
                keywords=["tech"],
                style="modern",
            ),
        )
        data = config.model_dump()
        assert data["event_id"] == "event-2025"
        assert data["colors"]["primary"] == "#667eea"
        assert isinstance(data["brand_voice"]["keywords"], list)

    def test_event_style_config_from_json(self):
        """Test EventStyleConfig can be loaded from JSON."""
        json_data = {
            "event_id": "event-2025",
            "event_name": "TechConf 2025",
            "source_url": "https://techconf.example.com",
            "colors": {
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f093fb",
                "background": "#ffffff",
                "text": "#1a202c",
            },
            "typography": {
                "heading_font": "Inter",
                "body_font": "Roboto",
            },
            "brand_voice": {
                "tone": "professional",
                "keywords": ["tech", "innovation"],
                "style": "modern",
            },
        }
        config = EventStyleConfig(**json_data)
        assert config.event_id == "event-2025"
        assert config.colors.primary == "#667eea"
