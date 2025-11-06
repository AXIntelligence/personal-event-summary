"""Security-hardened tool wrappers for web scraping."""

from urllib.parse import urlparse
import ipaddress
import validators


class SecurityError(Exception):
    """Raised when a security violation is detected."""

    pass


class WebScraperTool:
    """
    Security-hardened web scraping tool.

    Implements security measures:
    - URL validation (no file://, data://, javascript: schemes)
    - SSRF prevention (blocks private IPs, localhost, 127.0.0.1)
    - Timeout enforcement
    - Single-use enforcement (prevents tool reuse attacks)
    - User agent configuration for ethical scraping
    - Rate limiting support
    - robots.txt compliance option
    """

    def __init__(
        self,
        timeout: int = 60,
        respect_robots_txt: bool = True,
        rate_limit_delay: float = 1.0,
    ):
        """
        Initialize WebScraperTool.

        Args:
            timeout: Maximum request timeout in seconds
            respect_robots_txt: Whether to respect robots.txt
            rate_limit_delay: Delay between requests in seconds
        """
        self.timeout = timeout
        self.respect_robots_txt = respect_robots_txt
        self.rate_limit_delay = rate_limit_delay
        self.user_agent = (
            "EventStyleScraper/0.1.0 "
            "(+https://github.com/personal-event-summary; contact@example.com)"
        )
        self._used = False

    def validate_url(self, url: str) -> None:
        """
        Validate URL for security concerns.

        Args:
            url: URL to validate

        Raises:
            SecurityError: If URL fails security checks
        """
        # Parse URL first for scheme checking
        parsed = urlparse(url)

        # Check for missing/empty scheme
        if not parsed.scheme:
            raise SecurityError(f"Invalid URL format: Missing scheme (http:// or https://)")

        # Block dangerous schemes
        allowed_schemes = {"http", "https"}
        if parsed.scheme not in allowed_schemes:
            raise SecurityError(
                f"URL scheme '{parsed.scheme}' is not allowed. Only HTTP/HTTPS permitted."
            )

        # Check for hostname
        if not parsed.hostname:
            raise SecurityError(f"Invalid URL format: Missing hostname")

        # Block localhost (BEFORE validators.url which may reject these)
        if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
            raise SecurityError("Localhost URLs are not allowed (SSRF prevention)")

        # Block private IP ranges
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                raise SecurityError(
                    f"Private/internal IP addresses are not allowed: {parsed.hostname}"
                )
        except ValueError:
            # Not an IP address, that's fine (it's a domain name)
            pass

        # Additional hostname checks
        hostname_lower = parsed.hostname.lower() if parsed.hostname else ""

        # Block common internal hostnames
        internal_hostnames = {
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "169.254",  # Link-local
        }
        for internal in internal_hostnames:
            if hostname_lower.startswith(internal):
                raise SecurityError(f"Internal hostname not allowed: {parsed.hostname}")

        # Block private IP patterns (10.x.x.x, 192.168.x.x, 172.16-31.x.x)
        if hostname_lower.startswith("10.") or hostname_lower.startswith("192.168."):
            raise SecurityError(
                f"Private IP range not allowed: {parsed.hostname} (SSRF prevention)"
            )

        if hostname_lower.startswith("172."):
            try:
                second_octet = int(hostname_lower.split(".")[1])
                if 16 <= second_octet <= 31:
                    raise SecurityError(
                        f"Private IP range not allowed: {parsed.hostname} (SSRF prevention)"
                    )
            except (IndexError, ValueError):
                pass  # Not a valid IP format

    def mark_used(self) -> None:
        """Mark this tool instance as used."""
        self._used = True

    def is_used(self) -> bool:
        """Check if this tool instance has been used."""
        return self._used

    def check_not_used(self) -> None:
        """
        Check that this tool has not been used yet.

        Raises:
            SecurityError: If tool has already been used
        """
        if self._used:
            raise SecurityError("This tool instance has already been used (single-use enforcement)")
