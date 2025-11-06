"""Tests for security-hardened tool wrappers."""

import pytest
from event_style_scraper.tools import WebScraperTool, SecurityError


class TestWebScraperTool:
    """Tests for WebScraperTool security and functionality."""

    def test_valid_http_url(self):
        """Test tool accepts valid HTTP URL."""
        tool = WebScraperTool()
        # Should not raise
        tool.validate_url("http://example.com")

    def test_valid_https_url(self):
        """Test tool accepts valid HTTPS URL."""
        tool = WebScraperTool()
        # Should not raise
        tool.validate_url("https://example.com")

    def test_reject_file_url(self):
        """Test tool rejects file:// URLs (path traversal prevention)."""
        tool = WebScraperTool()
        with pytest.raises(SecurityError, match="not allowed"):
            tool.validate_url("file:///etc/passwd")

    def test_reject_localhost(self):
        """Test tool rejects localhost URLs (SSRF prevention)."""
        tool = WebScraperTool()
        with pytest.raises(SecurityError, match="not allowed"):
            tool.validate_url("http://localhost:8080")

    def test_reject_127_0_0_1(self):
        """Test tool rejects 127.0.0.1 URLs (SSRF prevention)."""
        tool = WebScraperTool()
        with pytest.raises(SecurityError, match="not allowed"):
            tool.validate_url("http://127.0.0.1:8080")

    def test_reject_private_ip_192(self):
        """Test tool rejects private IP ranges (SSRF prevention)."""
        tool = WebScraperTool()
        with pytest.raises(SecurityError, match="not allowed"):
            tool.validate_url("http://192.168.1.1")

    def test_reject_private_ip_10(self):
        """Test tool rejects 10.x.x.x private IPs (SSRF prevention)."""
        tool = WebScraperTool()
        with pytest.raises(SecurityError, match="not allowed"):
            tool.validate_url("http://10.0.0.1")

    def test_reject_malformed_url(self):
        """Test tool rejects malformed URLs."""
        tool = WebScraperTool()
        with pytest.raises(SecurityError, match="Invalid URL"):
            tool.validate_url("not-a-url")

    def test_reject_missing_scheme(self):
        """Test tool rejects URLs without scheme."""
        tool = WebScraperTool()
        with pytest.raises(SecurityError, match="Invalid URL"):
            tool.validate_url("example.com")

    def test_timeout_enforced(self):
        """Test tool enforces timeout configuration."""
        tool = WebScraperTool(timeout=30)
        assert tool.timeout == 30

    def test_default_timeout(self):
        """Test tool has reasonable default timeout."""
        tool = WebScraperTool()
        assert tool.timeout == 60  # 60 seconds default

    def test_user_agent_configured(self):
        """Test tool has proper user agent for ethical scraping."""
        tool = WebScraperTool()
        assert "EventStyleScraper" in tool.user_agent
        assert "github.com" in tool.user_agent.lower() or "contact" in tool.user_agent.lower()

    def test_single_use_enforcement(self):
        """Test tool can only be used once per instance (prevents reuse attacks)."""
        tool = WebScraperTool()
        tool.mark_used()
        assert tool.is_used() is True

    def test_double_use_rejected(self):
        """Test tool rejects second use attempt."""
        tool = WebScraperTool()
        tool.mark_used()
        with pytest.raises(SecurityError, match="already been used"):
            tool.check_not_used()

    def test_respects_robots_txt_flag(self):
        """Test tool has configuration for robots.txt compliance."""
        tool = WebScraperTool(respect_robots_txt=True)
        assert tool.respect_robots_txt is True

    def test_rate_limiting_configuration(self):
        """Test tool has rate limiting configuration."""
        tool = WebScraperTool(rate_limit_delay=2.0)
        assert tool.rate_limit_delay == 2.0
