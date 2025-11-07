# Scraper Validation Checklist

This checklist ensures scraped website styles are accurate and the Playwright tool is working correctly. Use this after scraping any new website or when validating changes to the scraper.

## Pre-Scrape Validation

### 1. Environment Setup
- [ ] **OpenAI API Key**: Verify `OPENAI_API_KEY` is set in `.env`
  ```bash
  grep OPENAI_API_KEY .env
  ```
- [ ] **Playwright Browsers**: Confirm Chromium installed
  ```bash
  playwright --version
  ls ~/.cache/ms-playwright/chromium-*
  ```
- [ ] **Dependencies**: All Python packages installed
  ```bash
  cd python && pip list | grep -E "playwright|crewai"
  ```

### 2. URL Security Check
- [ ] **Valid URL**: URL passes WebScraperTool.validate_url()
- [ ] **Not Localhost**: URL is not localhost, 127.0.0.1, or private IP
- [ ] **HTTPS**: URL uses https:// (http:// is acceptable but less secure)
- [ ] **Accessible**: Website is publicly accessible (not behind auth)

### 3. Timeout Configuration
- [ ] **Set Appropriate Timeout**:
  - Simple sites: 30s
  - Complex sites: 60-90s
  - Heavy JavaScript sites: 120s+

## Running the Scraper

### 4. Execute Scraper Command
```bash
cd python
PYTHONPATH=./src python3 -m event_style_scraper scrape \\
    --url https://example.com \\
    --timeout 90
```

### 5. Monitor Execution
- [ ] **Watch Logs**: Monitor output for progress
- [ ] **No Errors**: Check for runtime errors or exceptions
- [ ] **Completion**: Scraper completes without crashes
- [ ] **Output File**: JSON file created in `style-configs/`

## Post-Scrape Validation

### 6. Tool Usage Validation
- [ ] **Agent Called Tool**: Check logs for "Tool: Playwright Style Extractor"
  ```bash
  # If logs saved to file:
  grep -i "playwright" scraper_output.log
  grep "Tool:" scraper_output.log
  ```
- [ ] **No Hallucination**: Search for signs of fictional content:
  - Generic phrases like "Example Event" or "Official Site"
  - Made-up CSS IDs like "#site-header" on simple sites
  - Fictional robots.txt descriptions
  - Simulated dark mode styles not present on actual site
- [ ] **Tool Output Present**: Verify tool returned structured data (not prose)

### 7. Output File Validation
- [ ] **File Exists**: `style-configs/{domain}.json` created
  ```bash
  ls -lh style-configs/example-com.json
  ```
- [ ] **Valid JSON**: File parses without errors
  ```bash
  jq '.' style-configs/example-com.json | head
  ```
- [ ] **Required Fields**: All required fields present
  ```bash
  jq 'keys' style-configs/example-com.json
  # Should include: eventId, eventName, sourceUrl, colors, typography, brandVoice
  ```

### 8. Color Accuracy Validation (CRITICAL)

This is the most important validation step. Colors must match DevTools inspection.

#### Method A: Manual DevTools Comparison
1. **Open Website**: Navigate to scraped URL in Chrome
2. **Inspect Element**: Right-click header/prominent element → "Inspect"
3. **Check Computed Styles**: Styles tab → Computed → `background-color`
4. **Note Exact Color**: Record as RGB (e.g., `rgb(22, 8, 34)`)
5. **Convert to Hex**:
   ```javascript
   // In Chrome DevTools Console:
   "#" + [22, 8, 34].map(x => x.toString(16).padStart(2, '0')).join('')
   // Result: "#160822"
   ```
6. **Compare**: Scraped color vs DevTools color
   ```bash
   jq '.colors.primary' style-configs/example-com.json
   # Should match DevTools color (±2 RGB units)
   ```

#### Method B: Automated Validation Script
```bash
python scripts/validate_scraped_colors.py \\
    --url https://eventtechlive.com \\
    --config style-configs/eventtechlive-com.json \\
    --selector header \\
    --property backgroundColor \\
    --expected "#160822"
```

**Acceptance Criteria**:
- ✅ RGB difference ≤ 2 units per channel
- ❌ Difference > 10 units = likely hallucination

### 9. Content Completeness Validation
- [ ] **HTML Captured**: `html` field contains actual page HTML
  ```bash
  jq -r '.html | length' style-configs/example-com.json
  # Should be > 1000 characters for most sites
  ```
- [ ] **Computed Styles**: All key selectors present (body, header, nav, h1, button, a)
  ```bash
  jq '.computed_styles | keys' style-configs/example-com.json
  ```
- [ ] **CSS Variables**: If site uses custom properties, they're captured
  ```bash
  jq '.css_variables' style-configs/example-com.json
  ```
- [ ] **Assets**: Logo and favicon URLs populated (if present on site)
  ```bash
  jq '.assets' style-configs/example-com.json
  ```

### 10. Schema Validation
- [ ] **Colors Valid**: All hex colors match format `#RRGGBB`
  ```bash
  jq '.colors' style-configs/example-com.json
  # All values should be 7 characters starting with #
  ```
- [ ] **Typography Complete**: Font families have fallbacks
  ```bash
  jq '.typography.headingFont' style-configs/example-com.json
  # Example: "Inter, sans-serif"
  ```
- [ ] **Required Fields**: All required by EventStyleConfig present
  - `eventId`: string (derived from URL)
  - `eventName`: string (from title or h1)
  - `sourceUrl`: string (original URL)
  - `colors`: ColorPalette object
  - `typography`: Typography object
  - `brandVoice`: BrandVoice object
- [ ] **Pydantic Validation**: Config passes EventStyleConfig validation
  ```python
  from event_style_scraper.types import EventStyleConfig
  import json

  with open('style-configs/example-com.json') as f:
      config_data = json.load(f)

  config = EventStyleConfig(**config_data)  # Should not raise ValidationError
  ```

## Validation Tools

### Tool 1: Color Validation Script
```bash
python scripts/validate_scraped_colors.py \\
    --url <site-url> \\
    --config <config-path> \\
    --selector <css-selector> \\
    --property <css-property> \\
    --expected <hex-color>
```

**Example**:
```bash
python scripts/validate_scraped_colors.py \\
    --url https://eventtechlive.com \\
    --config style-configs/eventtechlive-com.json \\
    --selector header \\
    --property backgroundColor \\
    --expected "#160822"
```

### Tool 2: Integration Tests
```bash
# Run all integration tests
cd python
PYTHONPATH=./src pytest tests/integration/ -v -m integration

# Run specific test
PYTHONPATH=./src pytest tests/integration/test_real_scraping.py::test_scrape_eventtechlive_com_accurate_color -v
```

### Tool 3: Manual DevTools Inspection
1. Open DevTools (F12 or Cmd+Option+I)
2. Select element (Ctrl+Shift+C or Cmd+Shift+C)
3. Check Computed styles tab
4. Compare to scraped config
5. Document any differences >2 RGB units

## Red Flags (Signs of Hallucination)

### Immediate Red Flags ❌
- **No Tool Invocation**: Logs don't show "Tool: Playwright Style Extractor"
- **Prose Output**: Final answer is prose report, not structured dict
- **Generic Names**: Event names like "Example Event" or "Official Site"
- **Made-up IDs**: CSS IDs like "#site-header" on sites without them
- **Fictional CSS**: Detailed CSS rules for simple sites (e.g., example.com)
- **Perfect Dark Mode**: Complex dark mode styles for sites without them

### Suspicious Patterns ⚠️
- **Generic Blues**: Colors like #004080, #0072ce (tech company blues)
- **Round Numbers**: Colors ending in 00 (e.g., #ff0000, #0000ff)
- **Templated Structure**: All scraped sites have identical HTML structure
- **Missing Quirks**: No unique/unusual CSS that real sites have

### Validation Failures ❌
- **Color Mismatch**: >10 RGB units difference from DevTools
- **Missing Content**: HTML < 500 characters for complex site
- **No CSS Variables**: Site uses custom properties but none captured
- **Wrong Fonts**: Fonts don't match actual site fonts

## Troubleshooting

### Issue: Agent Hallucinates Instead of Calling Tool

**Symptoms**:
- No "Tool: Playwright Style Extractor" in logs
- Output is prose report, not structured dict
- Colors don't match DevTools inspection

**Solutions**:
1. Check task description emphasizes tool invocation
2. Verify agent backstory defines role as "Tool Operator"
3. Add explicit Action/Action Input format to task
4. Review CRITICAL RULES in task description

### Issue: Colors Don't Match DevTools

**Symptoms**:
- Scraped color differs by >10 RGB units from DevTools
- Colors are generic tech blues (#004080, #0072ce)

**Solutions**:
1. Re-run scraper with verbose logging
2. Verify Playwright tool actually executed
3. Check if website has dynamic styles (light/dark mode)
4. Inspect actual site element in DevTools
5. Compare scraped RGB to DevTools RGB

### Issue: Tool Fails to Launch Browser

**Symptoms**:
- Error: "Executable doesn't exist"
- Error: "Browser closed unexpectedly"

**Solutions**:
```bash
# Reinstall Playwright browsers
playwright install chromium

# Verify installation
playwright --version
ls ~/.cache/ms-playwright/chromium-*

# Check system dependencies (Linux)
playwright install-deps
```

### Issue: Timeout Errors

**Symptoms**:
- Error: "Timeout exceeded"
- Scraper hangs indefinitely

**Solutions**:
1. Increase timeout: `--timeout 120`
2. Check network connectivity
3. Verify website is accessible
4. Try simpler website first (example.com)

## Best Practices

### 1. Always Validate New Websites
- Never trust scraped output without validation
- Use DevTools to verify at least primary color
- Run validation script for critical colors

### 2. Document Validation Results
- Save before/after screenshots
- Record DevTools colors
- Document any mismatches
- Store validation reports in `analysis/`

### 3. Automate Where Possible
- Use validation script for regression testing
- Run integration tests in CI/CD
- Add GitHub Actions workflow for validation

### 4. Maintain Validation History
- Keep logs of successful validations
- Track color accuracy over time
- Document when websites change styles

## Quick Validation Workflow

**For New Website**:
1. Run scraper: `python -m event_style_scraper scrape --url <url>`
2. Check logs: Look for "Tool: Playwright Style Extractor"
3. Validate colors: Run `validate_scraped_colors.py`
4. Visual check: Open site in browser, compare side-by-side
5. Document: Save validation report to `analysis/`

**Expected Time**: 5-10 minutes per website

## References

- **CLAUDE.md Lesson 16**: End-to-End Validation is NON-NEGOTIABLE
- **CLAUDE.md Lesson 17**: Sample/Mock Data Can Hide Critical Flaws
- **CLAUDE.md Lesson 18**: Verify Scraper Output with DevTools
- **Plan 005**: Playwright-Based Scraping Tool
- **Plan 004**: Fix Event Tech Live Style Mismatch

---

**Last Updated**: 2025-11-07
**Version**: 1.0
**Maintained By**: Personal Event Summary Team
