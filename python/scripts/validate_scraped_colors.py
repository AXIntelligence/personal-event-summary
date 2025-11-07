#!/usr/bin/env python3
"""
Validate scraped colors against DevTools inspection.

This script uses Playwright to extract the actual computed color from a website
element and compares it to the color in a scraped style config file.

Usage:
    python scripts/validate_scraped_colors.py \\
        --url https://eventtechlive.com \\
        --config python/style-configs/eventtechlive-com.json \\
        --selector header \\
        --property backgroundColor \\
        --expected "#160822"

Exit codes:
    0: Colors match within tolerance
    1: Colors differ beyond tolerance
    2: Error during validation
"""

import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_string_to_tuple(rgb_string: str) -> tuple:
    """Convert 'rgb(R, G, B)' string to (R, G, B) tuple."""
    # Handle both "rgb(22, 8, 34)" and "rgba(22, 8, 34, 1)" formats
    rgb_string = rgb_string.replace("rgba(", "rgb(")
    if not rgb_string.startswith("rgb("):
        raise ValueError(f"Invalid RGB string: {rgb_string}")

    # Extract numbers
    nums_str = rgb_string.replace("rgb(", "").replace(")", "").split(",")
    # Take only first 3 values (R, G, B), ignore alpha if present
    nums = [int(n.strip()) for n in nums_str[:3]]

    return tuple(nums)


def extract_color_with_playwright(url: str, selector: str, property: str, timeout: int = 30000) -> str:
    """
    Use Playwright to extract computed color from a website element.

    Args:
        url: Website URL
        selector: CSS selector for element
        property: CSS property to extract (e.g., 'backgroundColor', 'color')
        timeout: Timeout in milliseconds

    Returns:
        Color as 'rgb(R, G, B)' string

    Raises:
        RuntimeError: If element not found or property not available
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=timeout)

            # Extract computed style using JavaScript
            color = page.evaluate(f'''() => {{
                const el = document.querySelector("{selector}");
                if (!el) {{
                    throw new Error("Element not found: {selector}");
                }}
                const computed = window.getComputedStyle(el);
                return computed.{property};
            }}''')

            return color

        finally:
            browser.close()


def load_scraped_config(config_path: Path) -> dict:
    """Load scraped style configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def compare_colors(scraped_rgb: tuple, actual_rgb: tuple, tolerance: int = 2) -> tuple[bool, int]:
    """
    Compare two RGB colors with tolerance.

    Args:
        scraped_rgb: RGB tuple from scraped config
        actual_rgb: RGB tuple from DevTools
        tolerance: Maximum difference allowed per channel

    Returns:
        (matches, max_diff): Whether colors match and maximum channel difference
    """
    max_diff = max(abs(scraped_rgb[i] - actual_rgb[i]) for i in range(3))
    matches = max_diff <= tolerance
    return matches, max_diff


def main():
    parser = argparse.ArgumentParser(
        description="Validate scraped colors against DevTools inspection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate Event Tech Live primary color
  python scripts/validate_scraped_colors.py \\
      --url https://eventtechlive.com \\
      --config style-configs/eventtechlive-com.json \\
      --selector header \\
      --property backgroundColor \\
      --expected "#160822"

  # Validate with custom tolerance
  python scripts/validate_scraped_colors.py \\
      --url https://example.com \\
      --config style-configs/example-com.json \\
      --selector body \\
      --property color \\
      --expected "#333333" \\
      --tolerance 5
        """
    )

    parser.add_argument("--url", required=True, help="Website URL to validate against")
    parser.add_argument("--config", required=True, help="Path to scraped style config JSON")
    parser.add_argument("--selector", required=True, help="CSS selector for element to inspect")
    parser.add_argument("--property", required=True, help="CSS property to check (e.g., backgroundColor, color)")
    parser.add_argument("--expected", required=True, help="Expected hex color (e.g., #160822)")
    parser.add_argument("--tolerance", type=int, default=2, help="Max RGB difference allowed per channel (default: 2)")
    parser.add_argument("--timeout", type=int, default=30, help="Page load timeout in seconds (default: 30)")
    parser.add_argument("--scraped-field", default="colors.primary", help="JSON path to scraped color in config (default: colors.primary)")

    args = parser.parse_args()

    print(f"🔍 Validating scraped color for {args.url}")
    print(f"📁 Config: {args.config}")
    print(f"🎯 Element: {args.selector}")
    print(f"🎨 Property: {args.property}")
    print()

    try:
        # Load scraped config
        config = load_scraped_config(Path(args.config))

        # Extract scraped color from config using field path
        field_parts = args.scraped_field.split('.')
        scraped_color = config
        for part in field_parts:
            scraped_color = scraped_color[part]

        print(f"📋 Scraped color: {scraped_color}")

        # Extract actual color from website using Playwright
        print(f"🌐 Fetching actual color from {args.url}...")
        actual_color = extract_color_with_playwright(
            args.url,
            args.selector,
            args.property,
            timeout=args.timeout * 1000  # Convert to ms
        )
        print(f"✅ Actual color: {actual_color}")
        print()

        # Convert colors to RGB tuples
        scraped_rgb = hex_to_rgb(scraped_color)
        actual_rgb = rgb_string_to_tuple(actual_color)
        expected_rgb = hex_to_rgb(args.expected)

        # Compare scraped vs actual
        scraped_matches, scraped_diff = compare_colors(scraped_rgb, actual_rgb, args.tolerance)

        # Compare expected vs actual
        expected_matches, expected_diff = compare_colors(expected_rgb, actual_rgb, args.tolerance)

        # Display comparison
        print("📊 Comparison Results:")
        print(f"  Scraped:  {scraped_color} → RGB{scraped_rgb}")
        print(f"  Expected: {args.expected} → RGB{expected_rgb}")
        print(f"  Actual:   {actual_color} → RGB{actual_rgb}")
        print()

        print(f"  Scraped vs Actual:  Δ={scraped_diff} RGB units  {'✅ MATCH' if scraped_matches else '❌ MISMATCH'}")
        print(f"  Expected vs Actual: Δ={expected_diff} RGB units  {'✅ MATCH' if expected_matches else '❌ MISMATCH'}")
        print()

        # Determine final result
        if scraped_matches:
            print("✅ SUCCESS: Scraped color matches DevTools within tolerance")
            print(f"   Difference: {scraped_diff} RGB units (max {args.tolerance} allowed)")
            return 0
        else:
            print("❌ FAILURE: Scraped color differs from DevTools beyond tolerance")
            print(f"   Difference: {scraped_diff} RGB units (max {args.tolerance} allowed)")
            print()
            print("Possible causes:")
            print("  - Agent hallucinated colors instead of using Playwright tool")
            print("  - Wrong CSS selector or property")
            print("  - Website styles changed since scraping")
            print("  - Dynamic styles (light/dark mode, hover states)")
            return 1

    except FileNotFoundError as e:
        print(f"❌ Error: Config file not found: {args.config}")
        return 2
    except KeyError as e:
        print(f"❌ Error: Field not found in config: {args.scraped_field}")
        print(f"   Available fields: {list(config.keys())}")
        return 2
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
