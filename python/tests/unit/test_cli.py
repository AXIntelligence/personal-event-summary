"""Tests for CLI interface."""

import pytest
from click.testing import CliRunner
from pathlib import Path
import json
import tempfile
import os
from unittest.mock import patch, Mock, call

from event_style_scraper.cli import cli, scrape
from event_style_scraper.types import EventStyleConfig, ColorPalette, Typography, BrandVoice


class TestCLI:
    """Test suite for CLI interface."""

    def test_cli_group_exists(self):
        """Test that CLI group exists."""
        assert cli is not None
        assert callable(cli)

    def test_scrape_command_exists(self):
        """Test that scrape command exists."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "scrape" in result.output

    def test_scrape_requires_url(self):
        """Test that scrape command requires --url parameter."""
        runner = CliRunner()
        result = runner.invoke(cli, ["scrape"])

        assert result.exit_code != 0
        assert "url" in result.output.lower() or "required" in result.output.lower()

    @patch("event_style_scraper.cli.StyleScrapingFlow")
    def test_scrape_with_valid_url(self, mock_flow_class):
        """Test scrape command with valid URL."""
        # Create mock config
        config_json = {
            "event_id": "example-com",
            "event_name": "Example Event",
            "source_url": "https://example.com",
            "colors": {
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f093fb",
                "background": "#ffffff",
                "text": "#1a202c"
            },
            "typography": {
                "heading_font": "Inter, sans-serif",
                "body_font": "system-ui, sans-serif"
            },
            "brand_voice": {
                "tone": "professional",
                "style": "modern",
                "keywords": ["test"]
            }
        }

        # Mock flow
        mock_flow = Mock()
        config = EventStyleConfig(**config_json)
        mock_flow.start.return_value = config
        mock_flow.export_config.return_value = Path("style-configs/example-com.json")
        mock_flow_class.return_value = mock_flow

        runner = CliRunner()
        result = runner.invoke(cli, ["scrape", "--url", "https://example.com"])

        assert result.exit_code == 0
        mock_flow_class.assert_called_once_with(url="https://example.com", timeout=60)
        mock_flow.start.assert_called_once()
        mock_flow.export_config.assert_called_once_with(config)

    @patch("event_style_scraper.cli.StyleScrapingFlow")
    def test_scrape_with_custom_timeout(self, mock_flow_class):
        """Test scrape command with custom timeout."""
        config_json = {
            "event_id": "test",
            "event_name": "Test",
            "source_url": "https://example.com",
            "colors": {
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f093fb",
                "background": "#ffffff",
                "text": "#1a202c"
            },
            "typography": {
                "heading_font": "Inter, sans-serif",
                "body_font": "system-ui, sans-serif"
            },
            "brand_voice": {
                "tone": "professional",
                "style": "modern",
                "keywords": ["test"]
            }
        }

        mock_flow = Mock()
        config = EventStyleConfig(**config_json)
        mock_flow.start.return_value = config
        mock_flow.export_config.return_value = Path("style-configs/test.json")
        mock_flow_class.return_value = mock_flow

        runner = CliRunner()
        result = runner.invoke(cli, ["scrape", "--url", "https://example.com", "--timeout", "120"])

        assert result.exit_code == 0
        mock_flow_class.assert_called_once_with(url="https://example.com", timeout=120)

    @patch("event_style_scraper.cli.StyleScrapingFlow")
    def test_scrape_handles_invalid_url(self, mock_flow_class):
        """Test scrape command handles invalid URLs gracefully."""
        mock_flow_class.side_effect = ValueError("Invalid URL: not allowed")

        runner = CliRunner()
        result = runner.invoke(cli, ["scrape", "--url", "http://localhost:8080"])

        assert result.exit_code != 0
        assert "error" in result.output.lower() or "invalid" in result.output.lower()

    @patch("event_style_scraper.cli.StyleScrapingFlow")
    def test_scrape_handles_scraping_error(self, mock_flow_class):
        """Test scrape command handles scraping errors gracefully."""
        mock_flow = Mock()
        mock_flow.start.side_effect = Exception("Connection timeout")
        mock_flow_class.return_value = mock_flow

        runner = CliRunner()
        result = runner.invoke(cli, ["scrape", "--url", "https://example.com"])

        assert result.exit_code != 0
        assert "error" in result.output.lower() or "failed" in result.output.lower()

    @patch("event_style_scraper.cli.StyleScrapingFlow")
    def test_scrape_displays_success_message(self, mock_flow_class):
        """Test that scrape command displays success message with file path."""
        config_json = {
            "event_id": "success-test",
            "event_name": "Success Test",
            "source_url": "https://example.com",
            "colors": {
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f093fb",
                "background": "#ffffff",
                "text": "#1a202c"
            },
            "typography": {
                "heading_font": "Inter, sans-serif",
                "body_font": "system-ui, sans-serif"
            },
            "brand_voice": {
                "tone": "professional",
                "style": "modern",
                "keywords": ["test"]
            }
        }

        mock_flow = Mock()
        config = EventStyleConfig(**config_json)
        mock_flow.start.return_value = config
        output_path = Path("style-configs/success-test.json")
        mock_flow.export_config.return_value = output_path
        mock_flow_class.return_value = mock_flow

        runner = CliRunner()
        result = runner.invoke(cli, ["scrape", "--url", "https://example.com"])

        assert result.exit_code == 0
        assert "success" in result.output.lower() or "✓" in result.output
        assert "success-test.json" in result.output

    def test_cli_imports_load_dotenv(self):
        """Test that CLI imports load_dotenv from dotenv."""
        from event_style_scraper import cli as cli_module

        # Verify load_dotenv is imported
        assert hasattr(cli_module, "load_dotenv")
        assert callable(cli_module.load_dotenv)

    def test_cli_help_works(self):
        """Test that CLI help command works (verifies basic functionality)."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Event Style Scraper" in result.output
