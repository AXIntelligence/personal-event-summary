# Plan 005: Playwright-Based Scraping Tool

**Status:** ✅ Completed
**Created:** 2025-11-06
**Last Updated:** 2025-11-07
**Completed:** 2025-11-07
**Priority:** 🔴 Critical

## Overview

Replace the current AI-guessing approach with actual browser-based style extraction using Playwright. Currently, the scraper hallucinates website content because no actual scraping tool is assigned to agents - they generate fictional HTML/CSS based on task descriptions. This plan implements a real Playwright-based tool that captures computed styles from rendered pages, ensuring accurate color, typography, and layout extraction.

**Problem**: CrewAI agents have no tools assigned. When asked to "scrape using Playwright," they generate plausible-sounding HTML/CSS from imagination. For example, when scraping eventtechlive.com, the agent fabricated an entire website structure with made-up CSS like `#site-header { background-color: #004080; }` - none of this exists on the actual website.

**Solution**: Implement `PlaywrightStyleExtractorTool` that uses actual browser automation to navigate to URLs, execute JavaScript, extract computed styles via DevTools Protocol, and return real measurements (not AI guesses).

## Target Outcomes

### Primary Outcomes
1. **Accurate Color Extraction**: Scraped colors match DevTools inspection within ±2 RGB units
2. **Real HTML Capture**: Tool extracts actual HTML/CSS from live browser, not hallucinated content
3. **Computed Style Access**: Extract browser-computed styles for headers, buttons, text, backgrounds
4. **Agent Integration**: CrewAI agents use the tool correctly for scraping tasks
5. **Validation Pipeline**: Automated comparison between scraped output and DevTools ground truth

### Success Criteria
- [ ] Scrape eventtechlive.com and extract actual header color (#160822) - not AI guess (#0072ce)
- [ ] Scrape example.com and extract real colors from rendered page
- [ ] All scraped colors verified against DevTools color picker (within ±2 RGB units)
- [ ] Tool integration: web_scraper_agent successfully calls PlaywrightStyleExtractorTool
- [ ] Zero hallucinated HTML/CSS in scraper output
- [ ] 100% of test cases pass (unit + integration)
- [ ] Coverage ≥80% for new tool code
- [ ] Manual validation: Side-by-side comparison shows perfect color match

### Validation Strategy

#### Empirical Validation Methods

**Method 1: DevTools Color Comparison**
- **Tools/Commands**:
  ```bash
  # Scrape website
  python -m event_style_scraper scrape --url https://eventtechlive.com

  # Extract primary color from output
  jq '.colors.primary' python/style-configs/eventtechlive-com.json

  # Manual verification:
  # 1. Open https://eventtechlive.com in Chrome
  # 2. Right-click header → Inspect
  # 3. Check Computed tab → background-color
  # 4. Convert rgb() to hex
  ```
- **Expected Results**: Scraped color matches DevTools color exactly
- **Acceptance Threshold**: RGB difference ≤ 2 units (accounts for rounding)

**Method 2: No Hallucination Test**
- **Tools/Commands**:
  ```bash
  # Scrape a website we control
  npx http-server ./test-fixtures/sample-site -p 9999 &
  python -m event_style_scraper scrape --url http://localhost:9999

  # Compare output to known HTML
  diff <(jq -r '.scraped_html' output.json) test-fixtures/sample-site/index.html
  ```
- **Expected Results**: Scraped HTML matches actual HTML character-by-character
- **Acceptance Threshold**: Zero diff lines (exact match)

**Method 3: Computed Style Accuracy**
- **Tools/Commands**:
  ```python
  # Unit test
  async def test_extract_computed_styles():
      tool = PlaywrightStyleExtractorTool()
      result = await tool.scrape("https://example.com")

      # Verify we got actual computed styles
      assert "background-color" in result.computed_styles["body"]
      assert result.computed_styles["body"]["background-color"] == "rgb(255, 255, 255)"
  ```
- **Expected Results**: Computed styles contain actual CSS properties from browser
- **Acceptance Threshold**: All key elements (header, body, button, nav) have computed styles

**Method 4: Agent Tool Usage**
- **Tools/Commands**:
  ```bash
  # Run full crew with verbose logging
  PYTHONPATH=./src python3 -m event_style_scraper scrape --url https://example.com -vv | tee output.log

  # Check for tool usage
  grep "Tool: PlaywrightStyleExtractorTool" output.log
  grep "Hallucinated" output.log | wc -l  # Should be 0
  ```
- **Expected Results**: Log shows agent called tool, no hallucination warnings
- **Acceptance Threshold**: Tool called exactly once per URL, zero hallucination flags

## Hypothesis-Driven Approach

### Hypothesis 1: Playwright can extract actual computed styles from browser

**Reasoning:** Playwright provides DevTools Protocol access, allowing us to query computed styles for any DOM element after JavaScript execution completes. This is the same mechanism Chrome DevTools uses, guaranteeing accuracy.

**Validation Method:**
- **Experiment:** Create a simple HTML page with known styles, launch Playwright browser, navigate to page, extract computed styles for body/header elements
- **Expected Outcome:**
  ```python
  computed = page.evaluate('''() => {
      const header = document.querySelector('header');
      return window.getComputedStyle(header).backgroundColor;
  }''')
  # Returns: "rgb(22, 8, 34)" for eventtechlive.com header
  ```
- **Validation Steps:**
  1. Create test fixture: `tests/fixtures/test-page.html` with `<header style="background-color: #160822">`
  2. Launch Playwright, navigate to fixture
  3. Extract computed style
  4. Assert: `rgb(22, 8, 34)` == computed color
  5. Repeat with 10 different colors to verify accuracy

**Success Criteria:**
- [ ] Playwright successfully launches browser (Chromium)
- [ ] JavaScript evaluation returns computed styles
- [ ] 10/10 colors match expected values exactly
- [ ] Extraction completes within timeout (default: 30s)

**Failure Conditions:**
- Browser launch fails (missing Playwright browsers)
- JavaScript evaluation returns undefined/null
- Colors differ by >2 RGB units
- **Fallback:** Use Selenium as alternative browser automation

### Hypothesis 2: CrewAI agents can call custom Playwright tool

**Reasoning:** CrewAI's `Tool` base class allows us to wrap Playwright functionality. Agents can invoke tools via the `tools` parameter when tools implement the required `_run()` method.

**Validation Method:**
- **Experiment:** Create minimal PlaywrightStyleExtractorTool extending crewai.tools.BaseTool, register with web_scraper_agent, verify agent calls it
- **Expected Outcome:**
  ```python
  # In style_extraction_crew.py
  @agent
  def web_scraper_agent(self) -> Agent:
      return Agent(
          config=self.agents_config["web_scraper_agent"],
          tools=[PlaywrightStyleExtractorTool(timeout=self.timeout)],  # ← Tool assigned
          verbose=True
      )
  ```
- **Validation Steps:**
  1. Implement tool with `_run(url: str)` method
  2. Add tool to agent's `tools=[]` list
  3. Run crew with mock assertions
  4. Verify tool's `_run()` was called with correct URL
  5. Check tool output appears in agent's context

**Success Criteria:**
- [ ] Tool successfully registered with agent
- [ ] Agent calls `tool._run(url)` during execution
- [ ] Tool output passes to next agent in context
- [ ] No "tool not found" errors in logs

**Failure Conditions:**
- Tool not discovered by agent
- Agent hallucinates scraping results instead of calling tool
- Tool exceptions crash the crew
- **Fallback:** Use CrewAI's `@tool` decorator instead of BaseTool inheritance

### Hypothesis 3: Extracted styles enable accurate style config generation

**Reasoning:** When AI agents receive *actual* HTML/CSS (not guesses), they can extract colors by parsing CSS rules, custom properties, and computed styles - eliminating guesswork.

**Validation Method:**
- **Experiment:** Feed real scraped HTML/CSS to StyleAnalystAgent, compare extracted colors to DevTools
- **Expected Outcome:**
  ```json
  {
    "colors": {
      "primary": "#160822",  // ✅ Actual color from DevTools
      "secondary": "#0a2540",
      "accent": "#005bb5"
    }
  }
  ```
- **Validation Steps:**
  1. Scrape eventtechlive.com with Playwright tool
  2. Pass output to StyleAnalystAgent
  3. Extract primary color from agent's output
  4. Open eventtechlive.com in Chrome DevTools
  5. Inspect header element, note background-color
  6. Compare: scraped vs DevTools
  7. Calculate RGB distance

**Success Criteria:**
- [ ] Primary color matches DevTools (≤2 RGB units difference)
- [ ] Secondary/accent colors match DevTools
- [ ] Typography matches actual font-family declarations
- [ ] No AI-guessed values in output (all sourced from CSS)

**Failure Conditions:**
- Agent still guesses colors despite receiving real CSS
- Colors differ by >10 RGB units
- Agent hallucinates fonts not present in CSS
- **Fallback:** Add explicit CSS parsing rules to reduce AI interpretation

## Implementation Details

### Phase 1: Core Playwright Tool Implementation

**Objective:** Create PlaywrightStyleExtractorTool that extracts HTML, CSS, and computed styles from live browser

**Steps:**

1. **Create tool file: `python/src/event_style_scraper/tools/playwright_scraper.py`**
   - File affected: `python/src/event_style_scraper/tools/playwright_scraper.py` (new)
   - Changes:
     ```python
     from crewai.tools import BaseTool
     from playwright.async_api import async_playwright
     from typing import Optional, Dict, Any

     class PlaywrightStyleExtractorTool(BaseTool):
         name: str = "Playwright Style Extractor"
         description: str = "Extracts HTML, CSS, and computed styles from websites using Playwright browser automation"

         def __init__(self, timeout: int = 30000):
             super().__init__()
             self.timeout = timeout

         def _run(self, url: str) -> Dict[str, Any]:
             """Synchronous wrapper for async scraping"""
             import asyncio
             return asyncio.run(self._async_run(url))

         async def _async_run(self, url: str) -> Dict[str, Any]:
             async with async_playwright() as p:
                 browser = await p.chromium.launch()
                 page = await browser.new_page()
                 await page.goto(url, wait_until="networkidle", timeout=self.timeout)

                 # Extract HTML
                 html = await page.content()

                 # Extract computed styles for key elements
                 computed_styles = await page.evaluate('''() => {
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
                 }''')

                 # Extract CSS custom properties
                 css_vars = await page.evaluate('''() => {
                     const rootStyle = getComputedStyle(document.documentElement);
                     const vars = {};

                     // Get all custom properties from :root
                     for (let prop of rootStyle) {
                         if (prop.startsWith('--')) {
                             vars[prop] = rootStyle.getPropertyValue(prop).trim();
                         }
                     }

                     return vars;
                 }''')

                 # Extract logo/favicon URLs
                 assets = await page.evaluate('''() => {
                     const logo = document.querySelector('img[alt*="logo" i], .logo img, #logo');
                     const favicon = document.querySelector('link[rel="icon"], link[rel="shortcut icon"]');

                     return {
                         logo: logo ? logo.src : null,
                         favicon: favicon ? favicon.href : null
                     };
                 }''')

                 await browser.close()

                 return {
                     "url": url,
                     "html": html,
                     "computed_styles": computed_styles,
                     "css_variables": css_vars,
                     "assets": assets,
                     "success": True
                 }
     ```
   - Validation: `pytest tests/unit/test_playwright_scraper.py -v`

2. **Update tools/__init__.py to export new tool**
   - File affected: `python/src/event_style_scraper/tools/__init__.py`
   - Changes:
     ```python
     from .web_scraper import WebScraperTool, SecurityError
     from .playwright_scraper import PlaywrightStyleExtractorTool

     __all__ = ["WebScraperTool", "SecurityError", "PlaywrightStyleExtractorTool"]
     ```
   - Validation: `python -c "from event_style_scraper.tools import PlaywrightStyleExtractorTool; print('Import OK')"`

3. **Install Playwright browsers**
   - File affected: None (system-level)
   - Changes: Run `playwright install chromium`
   - Validation: `playwright --version && ls ~/.cache/ms-playwright/chromium-*`

**Validation Checkpoint:**
- [ ] Tool file exists and imports successfully
- [ ] Playwright browsers installed (chromium)
- [ ] Can instantiate PlaywrightStyleExtractorTool()
- [ ] tool._run("https://example.com") returns dict with html/computed_styles/css_variables

### Phase 2: Unit Tests for Playwright Tool

**Objective:** Test tool in isolation with controlled fixtures

**Steps:**

1. **Create test fixtures**
   - File affected: `tests/fixtures/simple-page.html` (new)
   - Changes:
     ```html
     <!DOCTYPE html>
     <html>
     <head>
       <style>
         :root {
           --primary-color: #160822;
           --secondary-color: #0a2540;
         }
         header {
           background-color: var(--primary-color);
           color: white;
         }
       </style>
     </head>
     <body>
       <header>Test Header</header>
     </body>
     </html>
     ```
   - Validation: Open in browser to verify renders correctly

2. **Write unit tests**
   - File affected: `tests/unit/test_playwright_scraper.py` (new)
   - Changes:
     ```python
     import pytest
     from event_style_scraper.tools import PlaywrightStyleExtractorTool
     from pathlib import Path

     @pytest.mark.asyncio
     async def test_tool_extracts_html():
         """Test tool extracts actual HTML content"""
         tool = PlaywrightStyleExtractorTool(timeout=5000)

         # Serve fixture locally
         fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
         fixture_url = f"file://{fixture_path.absolute()}"

         result = tool._run(fixture_url)

         assert result["success"] is True
         assert "<header>Test Header</header>" in result["html"]

     @pytest.mark.asyncio
     async def test_tool_extracts_computed_styles():
         """Test tool extracts browser-computed styles"""
         tool = PlaywrightStyleExtractorTool(timeout=5000)
         fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
         fixture_url = f"file://{fixture_path.absolute()}"

         result = tool._run(fixture_url)

         assert "header" in result["computed_styles"]
         assert result["computed_styles"]["header"]["backgroundColor"] == "rgb(22, 8, 34)"
         assert result["computed_styles"]["header"]["color"] == "rgb(255, 255, 255)"

     @pytest.mark.asyncio
     async def test_tool_extracts_css_variables():
         """Test tool extracts CSS custom properties"""
         tool = PlaywrightStyleExtractorTool(timeout=5000)
         fixture_path = Path(__file__).parent.parent / "fixtures" / "simple-page.html"
         fixture_url = f"file://{fixture_path.absolute()}"

         result = tool._run(fixture_url)

         assert "--primary-color" in result["css_variables"]
         assert result["css_variables"]["--primary-color"] == "#160822"

     def test_tool_security_validation():
         """Test tool respects security constraints"""
         from event_style_scraper.tools import WebScraperTool, SecurityError

         validator = WebScraperTool()

         with pytest.raises(SecurityError, match="localhost"):
             validator.validate_url("http://localhost:8080")

         with pytest.raises(SecurityError, match="Private"):
             validator.validate_url("http://192.168.1.1")
     ```
   - Validation: `pytest tests/unit/test_playwright_scraper.py -v --cov=event_style_scraper.tools.playwright_scraper`

**Validation Checkpoint:**
- [ ] All unit tests pass (5/5)
- [ ] Coverage ≥80% for playwright_scraper.py
- [ ] Tests run in <10 seconds
- [ ] No flaky tests (run 5 times, all pass)

### Phase 3: Agent Integration

**Objective:** Connect PlaywrightStyleExtractorTool to web_scraper_agent

**Steps:**

1. **Update StyleExtractionCrew to assign tool to agent**
   - File affected: `python/src/event_style_scraper/crews/style_extraction_crew/style_extraction_crew.py`
   - Changes:
     ```python
     from event_style_scraper.tools import WebScraperTool, SecurityError, PlaywrightStyleExtractorTool

     @agent
     def web_scraper_agent(self) -> Agent:
         """Create web scraper agent with Playwright tool."""
         return Agent(
             config=self.agents_config["web_scraper_agent"],
             tools=[PlaywrightStyleExtractorTool(timeout=self.timeout)],  # ← Add tool
             verbose=True,
             allow_delegation=False
         )
     ```
   - Validation: `python -c "from event_style_scraper.crews.style_extraction_crew import StyleExtractionCrew; crew = StyleExtractionCrew('https://example.com'); print(crew.web_scraper_agent().tools)"`

2. **Update task description to reference tool explicitly**
   - File affected: `python/src/event_style_scraper/crews/style_extraction_crew/config/tasks.yaml`
   - Changes:
     ```yaml
     scrape_website:
       description: >
         Use the Playwright Style Extractor tool to scrape the event website at {url}.

         Call the tool with the URL to extract:
         - Raw HTML structure
         - Computed styles for all key elements (header, nav, body, h1, button, a)
         - CSS custom properties (--variable-name)
         - Logo and favicon URLs

         DO NOT generate or guess HTML/CSS. ONLY use the tool's actual output.

         Return the complete tool output as your final answer.
       expected_output: >
         The complete JSON output from the Playwright Style Extractor tool, containing:
         - html: Full HTML content
         - computed_styles: Object with computed styles for each selector
         - css_variables: Object with CSS custom properties
         - assets: Logo and favicon URLs
         - success: true
     ```
   - Validation: Visual inspection of task description

3. **Add tool call validation to tests**
   - File affected: `tests/unit/test_style_extraction_crew.py`
   - Changes:
     ```python
     def test_web_scraper_agent_has_playwright_tool():
         """Test that web scraper agent has PlaywrightStyleExtractorTool assigned"""
         from event_style_scraper.crews.style_extraction_crew import StyleExtractionCrew
         from event_style_scraper.tools import PlaywrightStyleExtractorTool

         crew_instance = StyleExtractionCrew("https://example.com", timeout=30)
         agent = crew_instance.web_scraper_agent()

         assert len(agent.tools) == 1
         assert isinstance(agent.tools[0], PlaywrightStyleExtractorTool)
         assert agent.tools[0].timeout == 30000  # 30s in ms
     ```
   - Validation: `pytest tests/unit/test_style_extraction_crew.py::test_web_scraper_agent_has_playwright_tool -v`

**Validation Checkpoint:**
- [ ] Agent has exactly 1 tool assigned
- [ ] Tool is PlaywrightStyleExtractorTool instance
- [ ] Task description emphasizes tool usage
- [ ] Test confirms tool assignment

### Phase 4: Integration Testing with Real Websites

**Objective:** Test end-to-end scraping with actual websites and validate against DevTools

**Steps:**

1. **Create integration test with example.com**
   - File affected: `tests/integration/test_real_scraping.py` (new)
   - Changes:
     ```python
     import pytest
     from event_style_scraper.crews.style_extraction_crew import StyleExtractionCrew

     @pytest.mark.integration
     @pytest.mark.timeout(120)
     def test_scrape_example_com():
         """Test scraping example.com and extracting real styles"""
         crew = StyleExtractionCrew("https://example.com", timeout=30)
         result = crew.crew().kickoff()

         # Validate result contains real data, not hallucinations
         config = result.pydantic

         # example.com has specific known colors
         # (Verify these by opening example.com in DevTools)
         assert config.colors.primary is not None
         assert len(config.colors.primary) == 7  # Hex format #RRGGBB
         assert config.colors.primary.startswith("#")

         # Should have actual source URL
         assert config.source_url == "https://example.com"

         # Should have actual event name (from <title> or h1)
         assert config.event_name is not None
         assert len(config.event_name) > 0

     @pytest.mark.integration
     @pytest.mark.timeout(120)
     def test_scrape_eventtechlive_com():
         """Test scraping Event Tech Live and extracting correct primary color"""
         crew = StyleExtractionCrew("https://eventtechlive.com", timeout=60)
         result = crew.crew().kickoff()

         config = result.pydantic

         # CRITICAL: Must extract actual primary color from DevTools
         # Expected: #160822 (dark purple header background)
         # NOT: #0072ce (AI-guessed tech blue)

         # Parse hex to RGB for comparison
         def hex_to_rgb(hex_color: str) -> tuple:
             hex_color = hex_color.lstrip('#')
             return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

         scraped_rgb = hex_to_rgb(config.colors.primary)
         expected_rgb = (22, 8, 34)  # #160822

         # Allow ±2 RGB units for rounding
         for i in range(3):
             assert abs(scraped_rgb[i] - expected_rgb[i]) <= 2, \
                 f"Primary color mismatch: got {config.colors.primary}, expected #160822"
     ```
   - Validation: `pytest tests/integration/test_real_scraping.py -v -m integration`

2. **Create DevTools validation script**
   - File affected: `scripts/validate_scraped_colors.py` (new)
   - Changes:
     ```python
     #!/usr/bin/env python3
     """
     Validate scraped colors against DevTools inspection.

     Usage:
         python scripts/validate_scraped_colors.py \
             --url https://eventtechlive.com \
             --config python/style-configs/eventtechlive-com.json \
             --selector header \
             --property backgroundColor \
             --expected "#160822"
     """
     import argparse
     import json
     from playwright.sync_api import sync_playwright

     def hex_to_rgb(hex_color):
         hex_color = hex_color.lstrip('#')
         return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

     def rgb_string_to_tuple(rgb_string):
         # "rgb(22, 8, 34)" -> (22, 8, 34)
         nums = rgb_string.replace("rgb(", "").replace(")", "").split(",")
         return tuple(int(n.strip()) for n in nums)

     def main():
         parser = argparse.ArgumentParser()
         parser.add_argument("--url", required=True)
         parser.add_argument("--config", required=True)
         parser.add_argument("--selector", required=True)
         parser.add_argument("--property", required=True)
         parser.add_argument("--expected", required=True)
         args = parser.parse_args()

         # Load scraped config
         with open(args.config) as f:
             config = json.load(f)

         # Extract scraped color from config
         scraped_color = config["colors"]["primary"]  # Adjust path as needed

         # Use Playwright to get actual computed style
         with sync_playwright() as p:
             browser = p.chromium.launch()
             page = browser.new_page()
             page.goto(args.url, wait_until="networkidle")

             actual_color = page.evaluate(f'''() => {{
                 const el = document.querySelector("{args.selector}");
                 return window.getComputedStyle(el).{args.property};
             }}''')

             browser.close()

         # Compare
         scraped_rgb = hex_to_rgb(scraped_color)
         expected_rgb = hex_to_rgb(args.expected)
         actual_rgb = rgb_string_to_tuple(actual_color)

         print(f"Scraped:  {scraped_color} -> {scraped_rgb}")
         print(f"Expected: {args.expected} -> {expected_rgb}")
         print(f"Actual:   {actual_color} -> {actual_rgb}")

         # Calculate differences
         scraped_diff = max(abs(scraped_rgb[i] - actual_rgb[i]) for i in range(3))
         expected_diff = max(abs(expected_rgb[i] - actual_rgb[i]) for i in range(3))

         print(f"\nScraped vs Actual: {scraped_diff} RGB units")
         print(f"Expected vs Actual: {expected_diff} RGB units")

         if scraped_diff <= 2:
             print("✅ PASS: Scraped color matches actual (±2 RGB units)")
             return 0
         else:
             print(f"❌ FAIL: Scraped color differs by {scraped_diff} RGB units")
             return 1

     if __name__ == "__main__":
         exit(main())
     ```
   - Validation: `chmod +x scripts/validate_scraped_colors.py && python scripts/validate_scraped_colors.py --help`

**Validation Checkpoint:**
- [ ] Integration tests pass (2/2)
- [ ] Scraped eventtechlive.com color matches DevTools (#160822)
- [ ] Validation script confirms accuracy
- [ ] No hallucinated HTML/CSS in output

### Phase 5: Validation Pipeline & Documentation

**Objective:** Establish validation checklist and document best practices

**Steps:**

1. **Create validation checklist document**
   - File affected: `docs/scraper-validation-checklist.md` (new)
   - Changes: (See Appendix A for full content)
   - Validation: Peer review checklist for completeness

2. **Update CLAUDE.md with new lesson learned**
   - File affected: `CLAUDE.md`
   - Changes: Add "Lesson 19: Agents Need Tools, Not Just Instructions"
   - Validation: Verify lesson captures key insights

3. **Create example validation workflow**
   - File affected: `.github/workflows/validate-scraper.yml` (new)
   - Changes:
     ```yaml
     name: Validate Scraper Accuracy

     on:
       push:
         paths:
           - 'python/style-configs/*.json'
       workflow_dispatch:

     jobs:
       validate:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v3

           - uses: actions/setup-python@v4
             with:
               python-version: '3.11'

           - name: Install dependencies
             run: |
               cd python
               pip install -r requirements.txt
               playwright install chromium

           - name: Validate Event Tech Live colors
             run: |
               python scripts/validate_scraped_colors.py \
                 --url https://eventtechlive.com \
                 --config python/style-configs/eventtechlive-com.json \
                 --selector header \
                 --property backgroundColor \
                 --expected "#160822"
     ```
   - Validation: Manually trigger workflow to verify it runs

**Validation Checkpoint:**
- [ ] Validation checklist created
- [ ] CLAUDE.md updated with lesson
- [ ] GitHub Actions workflow configured
- [ ] Documentation reviewed and approved

## Dependencies

### Prerequisites
- [ ] Playwright installed: `playwright install chromium`
- [ ] Python 3.10+ (for async/await syntax)
- [ ] pytest-asyncio for async test support
- [ ] Access to test websites (example.com, eventtechlive.com)

### Related Plans
- `plans/003-event-centered-styling-crewai.md` - Original scraper implementation (now being fixed)
- `plans/004-fix-event-tech-live-style-mismatch.md` - Documented color mismatch issue

### External Dependencies
- **Playwright** (v1.40.0+) - Browser automation
- **Chromium browser** - Installed via `playwright install`
- **CrewAI** (v0.80.0+) - Agent framework
- **pytest-asyncio** - Async test support

## Risk Assessment

### High Risk Items

1. **Risk:** Playwright browser automation is async, but CrewAI tools expect sync `_run()` method
   - **Likelihood:** High
   - **Impact:** High (blocks implementation)
   - **Mitigation:** Wrap async Playwright calls with `asyncio.run()` in synchronous `_run()` method
   - **Contingency:** If asyncio.run() causes issues, use `nest_asyncio` library

2. **Risk:** Agent ignores tool and continues hallucinating despite tool being available
   - **Likelihood:** Medium
   - **Impact:** Critical (defeats purpose of plan)
   - **Mitigation:** Update task descriptions to explicitly instruct "DO NOT guess, ONLY use tool output"
   - **Contingency:** Add validation layer that rejects output if tool wasn't called (check logs)

3. **Risk:** Playwright browser launch fails in CI/CD (missing dependencies, sandboxing issues)
   - **Likelihood:** Medium
   - **Impact:** High (blocks automated testing)
   - **Mitigation:** Use `playwright install-deps` to install system dependencies, configure GitHub Actions with proper permissions
   - **Contingency:** Run headless browser with `--no-sandbox` flag

### Medium Risk Items

1. **Risk:** Websites block Playwright with anti-bot detection
   - **Likelihood:** Low (for example.com, eventtechlive.com)
   - **Impact:** Medium (can't scrape certain sites)
   - **Mitigation:** Use stealth mode, rotate user agents, add delays
   - **Contingency:** Document unsupported websites, provide manual fallback

2. **Risk:** Test flakiness due to network timeouts or slow page loads
   - **Likelihood:** Medium
   - **Impact:** Low (annoying but not blocking)
   - **Mitigation:** Increase timeouts, use `wait_until="networkidle"`, retry logic
   - **Contingency:** Mark flaky tests with `@pytest.mark.flaky(reruns=3)`

3. **Risk:** Color rounding differences between browsers
   - **Likelihood:** Low
   - **Impact:** Low
   - **Mitigation:** Allow ±2 RGB units tolerance in validation
   - **Contingency:** Document browser-specific quirks in validation checklist

## Rollback Plan

If implementation fails or causes issues:

1. **Remove tool from agent**
   ```python
   # In style_extraction_crew.py
   @agent
   def web_scraper_agent(self) -> Agent:
       return Agent(
           config=self.agents_config["web_scraper_agent"],
           tools=[],  # ← Remove PlaywrightStyleExtractorTool
           verbose=True
       )
   ```

2. **Revert task description changes**
   ```bash
   git checkout HEAD -- python/src/event_style_scraper/crews/style_extraction_crew/config/tasks.yaml
   ```

3. **Remove new tool files**
   ```bash
   rm python/src/event_style_scraper/tools/playwright_scraper.py
   rm tests/unit/test_playwright_scraper.py
   rm tests/integration/test_real_scraping.py
   ```

4. **Verify system stability**
   ```bash
   PYTHONPATH=./python/src pytest python/tests/unit/ -v
   ```

**Validation after rollback:**
- [ ] All existing tests pass (pre-implementation test count)
- [ ] CLI still runs: `python -m event_style_scraper --help`
- [ ] No import errors when loading crews

## Testing Strategy

### Unit Tests
- [ ] Test PlaywrightStyleExtractorTool with local HTML fixtures
- [ ] Test computed style extraction accuracy (10 color variations)
- [ ] Test CSS variable extraction
- [ ] Test asset URL extraction (logo, favicon)
- [ ] Test error handling (invalid URL, timeout, network error)
- [ ] Test security validation integration

### Integration Tests
- [ ] Test full crew execution with Playwright tool
- [ ] Test scraping example.com and validating output
- [ ] Test scraping eventtechlive.com and validating primary color
- [ ] Test that agents call tool (not hallucinate)
- [ ] Test end-to-end: scrape → analyze → compile → export

### Manual Testing
1. **Visual DevTools comparison**
   - Scrape eventtechlive.com
   - Open website in Chrome
   - Right-click header → Inspect
   - Compare scraped color to Computed background-color
   - Verify match within ±2 RGB units

2. **CLI smoke test**
   ```bash
   python -m event_style_scraper scrape --url https://example.com --timeout 60
   cat python/style-configs/example-com.json | jq '.colors.primary'
   ```

3. **No-hallucination test**
   - Review scraper logs
   - Verify "Tool: PlaywrightStyleExtractorTool" appears
   - Check no generic descriptions like "modern website" or "tech blue"
   - Confirm actual HTML snippets in output

### Validation Commands
```bash
# Unit tests
PYTHONPATH=./python/src pytest python/tests/unit/test_playwright_scraper.py -v --cov

# Integration tests
PYTHONPATH=./python/src pytest python/tests/integration/test_real_scraping.py -v -m integration

# Full test suite
PYTHONPATH=./python/src pytest python/tests/ -v --cov=event_style_scraper --cov-report=term-missing

# Coverage check (must be ≥80%)
PYTHONPATH=./python/src pytest python/tests/unit/ --cov=event_style_scraper.tools.playwright_scraper --cov-report=term | grep "TOTAL"

# Manual scrape validation
python -m event_style_scraper scrape --url https://eventtechlive.com --timeout 90
python scripts/validate_scraped_colors.py \
  --url https://eventtechlive.com \
  --config python/style-configs/eventtechlive-com.json \
  --selector header \
  --property backgroundColor \
  --expected "#160822"
```

## Post-Implementation

### Documentation Updates
- [ ] Update `README.md` with Playwright tool explanation
- [ ] Update `python/README.md` with tool usage examples
- [ ] Add docstrings to all public methods in PlaywrightStyleExtractorTool
- [ ] Document validation workflow in `docs/scraper-validation-checklist.md`

### Knowledge Capture
- [ ] Document "Lesson 19: Agents Need Tools, Not Just Instructions" in CLAUDE.md
- [ ] Add "Best Practice: Always assign tools to agents, verify tool calls in logs" to CLAUDE.md
- [ ] Create troubleshooting guide for Playwright issues
- [ ] Add examples to `examples/` directory showing correct vs incorrect scraping

### Metrics to Track
- **Accuracy**: % of scraped colors within ±2 RGB of DevTools
- **Reliability**: % of scrapes that succeed without timeout
- **Performance**: Average scrape time per website
- **Tool Usage**: % of agent executions that actually call the tool (vs hallucinate)

## Appendix

### Appendix A: Validation Checklist Content

```markdown
# Scraper Validation Checklist

## Pre-Scrape Validation

- [ ] **URL Security Check**: Verify URL passes WebScraperTool.validate_url()
- [ ] **Timeout Configuration**: Set appropriate timeout (30s for simple sites, 90s for complex)
- [ ] **Playwright Browsers**: Confirm chromium installed (`playwright install chromium`)

## Post-Scrape Validation

### 1. Tool Usage Validation
- [ ] **Agent Called Tool**: Check logs for "Tool: PlaywrightStyleExtractorTool"
- [ ] **No Hallucination**: Search logs for "Thought:" followed by CSS - should be none
- [ ] **Tool Output Present**: Verify tool returned dict with html/computed_styles/css_variables

### 2. Accuracy Validation (DevTools Comparison)
- [ ] **Open Website**: Navigate to target URL in Chrome
- [ ] **Inspect Header Element**: Right-click header → Inspect
- [ ] **Check Computed Styles**: Styles tab → Computed → background-color
- [ ] **Convert to Hex**: Use color picker or convert rgb() to hex
- [ ] **Compare**: Scraped color vs DevTools color (±2 RGB units)

### 3. Completeness Validation
- [ ] **HTML Captured**: Verify result["html"] contains actual page HTML
- [ ] **Computed Styles**: Check all key selectors present (body, header, nav, h1, button, a)
- [ ] **CSS Variables**: If site uses custom properties, verify captured
- [ ] **Assets**: Logo and favicon URLs populated (if present on site)

### 4. Schema Validation
- [ ] **Colors Valid**: All hex colors match format #RRGGBB
- [ ] **Typography Complete**: Font families have fallbacks (e.g., "Inter, sans-serif")
- [ ] **Required Fields**: event_id, event_name, source_url, colors, typography, brand_voice
- [ ] **Pydantic Passes**: Config validates against EventStyleConfig schema

## Validation Tools

### Automated
```bash
# Run validation script
python scripts/validate_scraped_colors.py \
  --url <site-url> \
  --config <config-path> \
  --selector header \
  --property backgroundColor \
  --expected <hex-color>
```

### Manual
1. Open DevTools (F12)
2. Select element (Ctrl+Shift+C)
3. Check Computed styles
4. Compare to scraped config
5. Document any differences >2 RGB units
```

### Alternative Approaches Considered

1. **Approach:** Use CrewAI's built-in ScrapeWebsiteTool
   - **Pros:** Already integrated, no custom code needed
   - **Cons:** Only extracts text content, no CSS/computed styles, causes hallucination
   - **Why not chosen:** Doesn't solve the root problem - we need browser automation

2. **Approach:** Use Selenium instead of Playwright
   - **Pros:** More mature, wider browser support, larger community
   - **Cons:** Slower than Playwright, more verbose API, harder to extract computed styles
   - **Why not chosen:** Playwright is faster, has better async support, cleaner API for our use case

3. **Approach:** Use third-party scraping APIs (Firecrawl, Jina AI, Browserless)
   - **Pros:** No browser management, handles anti-bot measures, scalable
   - **Cons:** Costs money, external dependency, API key management, rate limits
   - **Why not chosen:** Want to keep scraper self-contained, avoid external dependencies

4. **Approach:** Parse static CSS files instead of computed styles
   - **Pros:** Simpler, no browser needed, faster
   - **Cons:** Misses JavaScript-applied styles, doesn't resolve CSS variables, inaccurate for modern sites
   - **Why not chosen:** Modern sites use CSS-in-JS, custom properties, and dynamic styling

### References

- Playwright Documentation: https://playwright.dev/python/
- Playwright DevTools Protocol: https://playwright.dev/python/docs/api/class-cdpsession
- CrewAI Custom Tools: https://docs.crewai.com/core-concepts/Tools/
- CLAUDE.md Lesson 16: End-to-End Validation is NON-NEGOTIABLE
- CLAUDE.md Lesson 17: Sample/Mock Data Can Hide Critical Flaws
- CLAUDE.md Lesson 18: Verify Scraper Output with DevTools
- Analysis Report: `analysis/exploration-report-2025-11-06-scraper-accuracy.md`

### Notes

**Performance Considerations:**
- Playwright browser launch adds ~2-3 seconds overhead per scrape
- Can be mitigated with browser context reuse for multiple pages
- Trade-off: accuracy vs speed - we prioritize accuracy

**Browser Selection:**
- Using Chromium (not Firefox/WebKit) because:
  - Most event websites test primarily on Chrome
  - DevTools validation uses Chrome
  - Best computed style API compatibility

**Async/Sync Bridge:**
- Playwright is async-first
- CrewAI tools expect synchronous `_run()` method
- Bridge using `asyncio.run()` in `_run()`, keep `_async_run()` for actual logic
- This pattern allows future async crew support while maintaining current compatibility
