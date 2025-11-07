"""Playwright-based style extraction tool for accurate web scraping."""

import asyncio
from typing import Any, Dict
from crewai.tools import BaseTool
from playwright.async_api import async_playwright


class PlaywrightStyleExtractorTool(BaseTool):
    """
    Extract HTML, CSS, and computed styles from websites using Playwright.

    This tool uses actual browser automation to:
    - Navigate to URLs and render JavaScript
    - Extract computed styles from rendered elements
    - Capture CSS custom properties (variables)
    - Extract logo and favicon URLs

    Unlike text-based scraping, this provides accurate measurements
    from the browser's rendering engine, not AI guesses.
    """

    name: str = "Playwright Style Extractor"
    description: str = (
        "Extracts HTML, CSS, and computed styles from websites using "
        "Playwright browser automation. Returns actual browser-computed "
        "styles, colors, typography, and layout properties."
    )
    timeout: int = 30000  # Declare as Pydantic field

    def __init__(self, timeout: int = 30000, **kwargs):
        """
        Initialize PlaywrightStyleExtractorTool.

        Args:
            timeout: Maximum time in milliseconds for page load (default: 30000ms = 30s)
            **kwargs: Additional arguments passed to BaseTool
        """
        super().__init__(timeout=timeout, **kwargs)

    def _run(self, url: str) -> Dict[str, Any]:
        """
        Synchronous wrapper for async scraping (required by CrewAI).

        Args:
            url: URL to scrape (http://, https://, or file://)

        Returns:
            Dictionary containing:
                - url: The scraped URL
                - html: Full HTML content
                - computed_styles: Computed styles for key elements
                - css_variables: CSS custom properties from :root
                - assets: Logo and favicon URLs
                - success: True if scraping succeeded
        """
        return asyncio.run(self._async_run(url))

    async def _async_run(self, url: str) -> Dict[str, Any]:
        """
        Async implementation of scraping with Playwright.

        Args:
            url: URL to scrape

        Returns:
            Dictionary with scraped data
        """
        async with async_playwright() as p:
            # Launch browser (headless mode)
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navigate to URL and wait for network to be idle
            await page.goto(url, wait_until="networkidle", timeout=self.timeout)

            # Extract raw HTML
            html = await page.content()

            # Extract computed styles for key elements
            computed_styles = await page.evaluate(
                """() => {
                    const selectors = ['body', 'header', 'nav', 'h1', 'button', 'a'];
                    const styles = {};

                    selectors.forEach(sel => {
                        const el = document.querySelector(sel);
                        if (el) {
                            const computed = window.getComputedStyle(el);
                            styles[sel] = {
                                backgroundColor: computed.backgroundColor,
                                color: computed.color,
                                fontFamily: computed.fontFamily,
                                fontSize: computed.fontSize,
                                lineHeight: computed.lineHeight
                            };
                        }
                    });

                    return styles;
                }"""
            )

            # Extract CSS custom properties (variables) from :root
            css_vars = await page.evaluate(
                """() => {
                    const rootStyle = getComputedStyle(document.documentElement);
                    const vars = {};

                    // Get all custom properties from :root
                    for (let prop of rootStyle) {
                        if (prop.startsWith('--')) {
                            vars[prop] = rootStyle.getPropertyValue(prop).trim();
                        }
                    }

                    return vars;
                }"""
            )

            # Extract logo and favicon URLs
            assets = await page.evaluate(
                """() => {
                    const logo = document.querySelector('img[alt*="logo" i], .logo img, #logo');
                    const favicon = document.querySelector('link[rel="icon"], link[rel="shortcut icon"]');

                    return {
                        logo: logo ? logo.src : null,
                        favicon: favicon ? favicon.href : null
                    };
                }"""
            )

            await browser.close()

            return {
                "url": url,
                "html": html,
                "computed_styles": computed_styles,
                "css_variables": css_vars,
                "assets": assets,
                "success": True,
            }
