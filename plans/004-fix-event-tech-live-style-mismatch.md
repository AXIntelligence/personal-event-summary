# Plan 004: Fix Event Tech Live Style Mismatch with Real Scraped Data

**Status:** Draft
**Created:** 2025-11-06
**Last Updated:** 2025-11-06
**Priority:** 🔴 Critical

## Overview

The generated Event Tech Live attendee pages currently use colors that do not match the actual eventtechlive.com website. Investigation reveals that the `style-configs/event-tech-live-2025.json` configuration file was manually created as "sample config" for testing Plan 003's TypeScript integration, rather than being scraped from the actual website. This represents a critical validation gap that undermines the credibility of the event-centered styling feature.

**Current State:**
- Generated pages use primary color **#00b8d4** (cyan)
- Actual eventtechlive.com uses primary color **#3182CE** (deep blue)
- Colors are ~65 degrees apart on the color wheel - immediately noticeable mismatch
- Python scraper was validated with example.com but never run against eventtechlive.com
- TypeScript integration tested with hand-crafted sample data, not real scraped output

This plan addresses the immediate style mismatch while establishing a robust validation process to prevent similar issues in the future.

## Target Outcomes

### Primary Outcomes

1. **Accurate Style Representation**: Generated Event Tech Live pages visually match the actual eventtechlive.com website with respect to colors, typography, and brand voice
2. **Real Scraped Data**: Replace sample config with data actually scraped from eventtechlive.com using the Python CrewAI pipeline
3. **End-to-End Validation**: Demonstrate complete pipeline validation from website scraping → JSON export → TypeScript CSS generation → HTML rendering
4. **Process Improvement**: Establish validation checklist and documentation to prevent future sample-data-as-real-data incidents

### Success Criteria

- [ ] Scraper successfully runs against https://eventtechlive.com and produces valid EventStyleConfig JSON
- [ ] Generated pages use primary color #3182CE (matches actual website, verified manually in browser DevTools)
- [ ] Visual side-by-side comparison confirms brand consistency (colors, fonts, spacing)
- [ ] All 139 TypeScript tests still passing (zero regression)
- [ ] All 81 Python tests still passing (zero regression)
- [ ] HTML validation maintains 0 errors (warnings acceptable)
- [ ] New validation checklist documented and integrated into workflow
- [ ] CLAUDE.md updated with Lesson 19/20 documenting this case study

### Validation Strategy

#### Empirical Validation Methods

**Method 1: Color Accuracy Validation**
- **Tools/Commands:**
  ```bash
  # Extract primary color from actual website
  curl -s https://eventtechlive.com | grep -o "#[0-9a-fA-F]\{6\}" | sort -u | head -5

  # Extract primary color from generated config
  jq -r '.colors.primary' style-configs/event-tech-live-2025.json

  # Extract primary color from generated HTML
  grep -o "color-primary: #[0-9a-fA-F]\{6\}" dist/attendees/2001/index.html
  ```
- **Expected Results:** All three sources show `#3182CE` (or very close blue variant)
- **Acceptance Threshold:** Primary color matches actual website within 5% RGB distance

**Method 2: End-to-End Pipeline Validation**
- **Tools/Commands:**
  ```bash
  # Run complete pipeline
  cd python
  PYTHONPATH=./src python3 -m event_style_scraper scrape \
    --url https://eventtechlive.com \
    --output ../style-configs/event-tech-live-2025.json \
    --timeout 120

  cd ..
  npm run generate

  # Verify output exists and is valid
  test -f dist/attendees/2001/index.html && echo "✅ Page generated"
  grep "#3182CE\|#3182ce" dist/attendees/2001/index.html && echo "✅ Color matches"
  ```
- **Expected Results:** Complete pipeline executes successfully, generates pages with correct colors
- **Acceptance Threshold:** Zero errors in pipeline execution, generated HTML contains correct color values

**Method 3: Visual Regression Validation**
- **Tools/Commands:** Manual visual inspection with documented screenshots
  1. Open https://eventtechlive.com in browser
  2. Inspect primary button/header to confirm #3182CE
  3. Open dist/attendees/2001/index.html in browser
  4. Visually compare colors, fonts, spacing
  5. Take screenshots for documentation
- **Expected Results:** Visual match between actual website and generated pages
- **Acceptance Threshold:** No immediately noticeable color/brand inconsistencies

**Method 4: Test Coverage Validation**
- **Tools/Commands:**
  ```bash
  # Python tests
  cd python
  PYTHONPATH=./src python3 -m pytest tests/unit/ -v --cov=event_style_scraper --cov-report=term-missing

  # TypeScript tests
  cd ..
  npm test
  npm run test:coverage
  ```
- **Expected Results:** All tests pass, coverage ≥85% (current: 91.6% TS, 94% Python)
- **Acceptance Threshold:** 100% tests passing, no coverage regression

## Hypothesis-Driven Approach

### Hypothesis 1: The Python scraper will extract #3182CE as primary color from eventtechlive.com

**Reasoning:**
- The scraper successfully extracted colors from example.com
- WebFetch confirms #3182CE is the primary blue color on eventtechlive.com
- The CrewAI StyleAnalystAgent is designed to identify primary brand colors from CSS
- Playwright-based scraping captures computed styles, not just static CSS

**Validation Method:**
- **Experiment:** Run `python -m event_style_scraper scrape --url https://eventtechlive.com` and inspect output JSON
- **Expected Outcome:** JSON file contains `"primary": "#3182CE"` (or close RGB equivalent)
- **Validation Steps:**
  1. Backup existing sample config: `mv style-configs/event-tech-live-2025.json style-configs/event-tech-live-2025.json.sample`
  2. Run scraper with verbose logging
  3. Inspect `python/style-configs/eventtechlive-com.json` for color values
  4. Compare extracted primary color to manual inspection in browser DevTools
  5. Validate JSON passes Pydantic schema validation

**Success Criteria:**
- [ ] Scraper completes without errors (exit code 0)
- [ ] Output JSON contains valid EventStyleConfig schema
- [ ] Primary color is within 10% RGB distance of #3182CE
- [ ] StyleAnalystAgent confidence score ≥80% for color extraction

**Failure Conditions:**
- Scraper fails with timeout or network error → Increase timeout to 180s, check robots.txt
- Primary color is wrong (e.g., still cyan) → Inspect scraped HTML/CSS, verify website structure
- JSON schema validation fails → Check Pydantic model matches CrewAI output format
- **Fallback:** If scraper consistently extracts wrong color, manually inspect CSS and create corrected config with documentation explaining why manual intervention was needed

### Hypothesis 2: Replacing sample config with scraped config will fix the color mismatch in generated pages

**Reasoning:**
- The TypeScript integration (loadStyleConfig → generateEventCSS → template injection) is proven to work
- Integration tests with sample data pass 100%
- The only issue is the input data (wrong colors), not the processing logic
- Once correct colors are in the JSON, TypeScript will generate correct CSS

**Validation Method:**
- **Experiment:** Replace `style-configs/event-tech-live-2025.json` with scraped version, regenerate pages, inspect output
- **Expected Outcome:** Generated HTML contains `--color-primary: #3182CE` instead of `--color-primary: #00b8d4`
- **Validation Steps:**
  1. Backup current generated pages: `cp -r dist/attendees dist/attendees.backup`
  2. Copy scraped config: `cp python/style-configs/eventtechlive-com.json style-configs/event-tech-live-2025.json`
  3. Regenerate: `npm run generate`
  4. Diff pages: `diff dist/attendees/2001/index.html dist/attendees.backup/2001/index.html`
  5. Confirm color change: `grep "color-primary" dist/attendees/2001/index.html`

**Success Criteria:**
- [ ] Generated HTML contains #3182CE instead of #00b8d4
- [ ] CSS variables properly updated in :root selector
- [ ] Gradient colors also updated (should use #3182CE in gradient)
- [ ] All 12 Event Tech Live attendee pages (2001-2012) updated consistently

**Failure Conditions:**
- Colors don't change after regeneration → Check if loadStyleConfig is correctly mapping eventId to config file
- Only some pages updated → Check event ID matching logic in generate.ts
- CSS variables not injected → Verify generateEventCSS is called and result is passed to template
- **Fallback:** Debug TypeScript integration, add logging to trace config loading and CSS generation

### Hypothesis 3: The existing test suite will catch any regressions introduced by using real scraped data

**Reasoning:**
- Tests validate the TypeScript integration works with any valid EventStyleConfig JSON
- Tests use parameterized data and don't hard-code specific color values (except in validation tests)
- Python tests validate scraper output format, not specific color values
- HTML validation tests check structure, not specific color values

**Validation Method:**
- **Experiment:** Run full test suite after replacing config and regenerating pages
- **Expected Outcome:** All tests pass with no changes needed
- **Validation Steps:**
  1. Run Python tests: `cd python && PYTHONPATH=./src pytest tests/unit/ -v`
  2. Run TypeScript tests: `npm test`
  3. Run integration tests: `npm run test:integration`
  4. Run HTML validation: `npm run validate:html`

**Success Criteria:**
- [ ] 81/81 Python tests passing
- [ ] 139/139 TypeScript tests passing
- [ ] 0 HTML validation errors (warnings acceptable)
- [ ] Test coverage maintains ≥85% (current: 91.6% TS, 94% Python)

**Failure Conditions:**
- Tests fail due to hard-coded color expectations → Update tests to be parameterized
- HTML validation fails with new colors → Check color contrast ratios, accessibility
- Coverage drops → Add tests for any new validation logic
- **Fallback:** Update tests to accommodate real data variations while maintaining validation rigor

### Hypothesis 4: A validation checklist will prevent future sample-data incidents

**Reasoning:**
- The root cause was lack of validation that scraped data matched actual website
- A checklist forces explicit verification steps before claiming "complete"
- Documentation of this incident provides a concrete case study for future reference
- Pre-commit hooks can catch sample configs being committed without documentation

**Validation Method:**
- **Experiment:** Create checklist, document in CLAUDE.md, test on this implementation
- **Expected Outcome:** Checklist catches all validation gaps that led to this issue
- **Validation Steps:**
  1. Draft validation checklist based on lessons learned
  2. Apply checklist to this implementation
  3. Verify every item can be checked empirically
  4. Add to CLAUDE.md as Lesson 19 or 20
  5. Create pre-commit hook template (optional)

**Success Criteria:**
- [ ] Checklist includes: scraper execution log, color comparison, visual validation, screenshot documentation
- [ ] All checklist items for this fix can be verified empirically
- [ ] CLAUDE.md updated with case study referencing this plan
- [ ] Validation checklist prevents claiming "complete" without running actual scraper

**Failure Conditions:**
- Checklist is too vague or subjective → Make items more specific and measurable
- Checklist too burdensome → Prioritize critical items, make others optional
- **Fallback:** Start with minimal checklist, iterate based on actual usage

## Implementation Details

### Phase 1: Scrape Real Data from Event Tech Live

**Objective:** Execute Python scraper against eventtechlive.com and capture authentic style configuration

**Steps:**

1. **Prepare Environment**
   - File(s): `python/.env`
   - Changes: Verify OPENAI_API_KEY is set (required for CrewAI agents)
   - Validation: `cd python && python3 -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✅ API key loaded' if os.getenv('OPENAI_API_KEY') else '❌ Missing API key')"`

2. **Backup Sample Config**
   - File(s): `style-configs/event-tech-live-2025.json`
   - Changes: Rename to `event-tech-live-2025.json.sample` for reference
   - Validation: `test -f style-configs/event-tech-live-2025.json.sample && echo "✅ Sample backed up"`

3. **Run Scraper**
   - File(s): Output to `python/style-configs/eventtechlive-com.json`
   - Changes: Execute scraper with increased timeout for thoroughness
   - Command:
     ```bash
     cd python
     PYTHONPATH=./src python3 -m event_style_scraper scrape \
       --url https://eventtechlive.com \
       --timeout 120 \
       2>&1 | tee ../analysis/scraper-eventtechlive-log-$(date +%Y%m%d-%H%M%S).txt
     ```
   - Validation:
     - Exit code 0
     - Log file shows successful CrewAI execution
     - JSON file exists: `test -f python/style-configs/eventtechlive-com.json`

4. **Inspect Scraped Data**
   - File(s): `python/style-configs/eventtechlive-com.json`
   - Changes: Manual inspection of extracted values
   - Validation Commands:
     ```bash
     # View full config
     jq '.' python/style-configs/eventtechlive-com.json

     # Check primary color
     jq -r '.colors.primary' python/style-configs/eventtechlive-com.json
     # Expected: #3182CE or similar blue

     # Check typography
     jq -r '.typography.headingFont' python/style-configs/eventtechlive-com.json

     # Check confidence scores (if present in output)
     jq '.metadata // "No metadata"' python/style-configs/eventtechlive-com.json
     ```
   - Manual validation: Open eventtechlive.com in browser, inspect CSS, confirm colors match

5. **Validate Against Schema**
   - File(s): `python/style-configs/eventtechlive-com.json`, `python/src/event_style_scraper/types.py`
   - Changes: Programmatic schema validation
   - Validation Command:
     ```bash
     cd python
     PYTHONPATH=./src python3 -c "
     import json
     from event_style_scraper.types import EventStyleConfig

     with open('style-configs/eventtechlive-com.json') as f:
         data = json.load(f)

     config = EventStyleConfig(**data)
     print('✅ Schema validation passed')
     print(f'Event: {config.event_name}')
     print(f'Primary Color: {config.colors.primary}')
     print(f'Heading Font: {config.typography.heading_font}')
     "
     ```

**Validation Checkpoint:**
- [ ] Scraper executed successfully (exit code 0)
- [ ] JSON output exists and is valid EventStyleConfig
- [ ] Primary color is blue (#3182CE or close variant), not cyan
- [ ] Typography fonts extracted (not default fallbacks)
- [ ] Brand voice keywords extracted (not generic placeholders)
- [ ] Log file saved to analysis/ for traceability

### Phase 2: Replace Sample Config and Regenerate Pages

**Objective:** Integrate scraped data into TypeScript pipeline and generate corrected pages

**Steps:**

1. **Normalize Config File**
   - File(s): `python/style-configs/eventtechlive-com.json` → `style-configs/event-tech-live-2025.json`
   - Changes: Copy scraped config to TypeScript location, ensure eventId matches
   - Commands:
     ```bash
     # Copy scraped config
     cp python/style-configs/eventtechlive-com.json \
        style-configs/event-tech-live-2025.json

     # Update eventId to match attendee data (if needed)
     # Check current eventId in attendee data
     jq -r '.eventId' data/attendees/2001.json
     # Expected: "event-tech-live-2025"

     # Verify config eventId matches
     jq -r '.eventId' style-configs/event-tech-live-2025.json
     # If mismatch, update config:
     # jq '.eventId = "event-tech-live-2025"' style-configs/event-tech-live-2025.json > tmp.json && mv tmp.json style-configs/event-tech-live-2025.json
     ```
   - Validation: `diff -u style-configs/event-tech-live-2025.json.sample style-configs/event-tech-live-2025.json | head -20` (should show color differences)

2. **Backup Current Generated Pages**
   - File(s): `dist/attendees/`
   - Changes: Preserve current state for comparison
   - Commands:
     ```bash
     mkdir -p analysis/page-comparison-$(date +%Y%m%d)
     cp dist/attendees/2001/index.html analysis/page-comparison-$(date +%Y%m%d)/before.html
     ```
   - Validation: `test -f analysis/page-comparison-*/before.html`

3. **Regenerate All Pages**
   - File(s): `dist/attendees/*/index.html` (all 24 pages)
   - Changes: Run generation pipeline with new config
   - Command: `npm run generate`
   - Validation:
     ```bash
     # Verify generation completed
     test -f dist/attendees/2001/index.html && echo "✅ Generation complete"

     # Check color was updated
     grep "color-primary: #3182CE" dist/attendees/2001/index.html && echo "✅ Color updated"

     # Verify all 12 Event Tech Live pages updated
     for id in 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012; do
       grep -q "#3182CE" dist/attendees/$id/index.html && echo "✅ $id updated" || echo "❌ $id not updated"
     done
     ```

4. **Compare Before/After**
   - File(s): `analysis/page-comparison-*/before.html` and `dist/attendees/2001/index.html`
   - Changes: Capture differences for documentation
   - Commands:
     ```bash
     # Save after version
     cp dist/attendees/2001/index.html analysis/page-comparison-$(date +%Y%m%d)/after.html

     # Generate diff
     diff -u analysis/page-comparison-*/before.html analysis/page-comparison-*/after.html > analysis/page-comparison-*/diff.txt || true

     # Extract color changes specifically
     grep -E "(color-primary|gradient-primary)" analysis/page-comparison-*/before.html > analysis/page-comparison-*/colors-before.txt
     grep -E "(color-primary|gradient-primary)" analysis/page-comparison-*/after.html > analysis/page-comparison-*/colors-after.txt

     echo "Color changes:"
     diff -u analysis/page-comparison-*/colors-before.txt analysis/page-comparison-*/colors-after.txt || true
     ```
   - Validation: Diff should show color changes from #00b8d4 → #3182CE

5. **Visual Validation**
   - File(s): Manual browser inspection + screenshots
   - Changes: Document visual match with screenshots
   - Steps:
     1. Open https://eventtechlive.com in browser
     2. Right-click header/button → Inspect → Confirm primary color is #3182CE
     3. Take screenshot: `analysis/screenshots/eventtechlive-actual-$(date +%Y%m%d).png`
     4. Open `dist/attendees/2001/index.html` in browser
     5. Inspect hero section, CTA buttons → Confirm colors match
     6. Take screenshot: `analysis/screenshots/generated-page-$(date +%Y%m%d).png`
     7. Create comparison document: `analysis/visual-validation-$(date +%Y%m%d).md`
   - Validation: Side-by-side screenshots show consistent brand colors

**Validation Checkpoint:**
- [ ] Config file copied to TypeScript location with correct eventId
- [ ] All 24 pages regenerated successfully
- [ ] Event Tech Live pages (2001-2012) now use #3182CE instead of #00b8d4
- [ ] Original event pages (1001-1012) unchanged (different event, different config)
- [ ] Before/after diff captured and documented
- [ ] Visual inspection confirms brand consistency
- [ ] Screenshots saved for documentation

### Phase 3: Validate Complete Pipeline

**Objective:** Run all tests and validation to confirm zero regressions and successful fix

**Steps:**

1. **Run Python Tests**
   - File(s): `python/tests/unit/*.py`
   - Changes: None expected, validating no regressions
   - Command:
     ```bash
     cd python
     PYTHONPATH=./src python3 -m pytest tests/unit/ -v \
       --cov=event_style_scraper \
       --cov-report=term-missing \
       --cov-report=html:../coverage/python-coverage
     ```
   - Validation: All 81 tests passing, coverage ≥94%

2. **Run TypeScript Tests**
   - File(s): `tests/**/*.test.ts`
   - Changes: None expected, validating no regressions
   - Command:
     ```bash
     npm test
     npm run test:coverage
     ```
   - Validation: All 139 tests passing, coverage ≥91.6%

3. **Run HTML Validation**
   - File(s): `dist/attendees/*/index.html`
   - Changes: None expected (HTML structure unchanged, only CSS values)
   - Command: `npm run validate:html`
   - Validation: 0 errors, warnings acceptable (should be same count as before: 48 warnings across 24 pages)

4. **Performance Validation**
   - File(s): N/A
   - Changes: Validate generation time hasn't regressed
   - Command: `time npm run generate`
   - Validation: Generation time < 2s (current baseline: ~1.6s for 24 pages)

5. **Integration Test Run**
   - File(s): `tests/integration/*.test.ts`
   - Changes: Validate end-to-end style integration still works
   - Command: `npm run test:integration`
   - Validation: All integration tests passing, including styleIntegration.test.ts

**Validation Checkpoint:**
- [ ] 81/81 Python tests passing
- [ ] 139/139 TypeScript tests passing
- [ ] 0 HTML validation errors
- [ ] Generation time < 2s
- [ ] Test coverage maintained (≥85%)
- [ ] No regressions in any test suite

### Phase 4: Document and Create Validation Process

**Objective:** Capture lessons learned and establish process to prevent future incidents

**Steps:**

1. **Update CLAUDE.md with New Lesson**
   - File(s): `CLAUDE.md`
   - Changes: Add Lesson 19 or 20 documenting this case study
   - Content Structure:
     ```markdown
     ### Lesson XX: Sample Data Is Not Validation Data (Critical)

     **Learning:** Testing with hand-crafted sample data validates code works,
     but does NOT validate the system produces correct output for real inputs.

     **Case Study:** Plan 003 Event Tech Live Style Mismatch
     - Claimed: "End-to-end validated with real data"
     - Reality: TypeScript tested with manually created sample config
     - Result: Generated pages used cyan (#00b8d4) instead of actual blue (#3182CE)
     - Impact: Brand inconsistency, credibility loss, cannot demo confidently

     **Validation Checklist for Style Scraping:**
     - [ ] Scraper executed against actual target URL (not sample/mock)
     - [ ] Execution log saved to analysis/ with timestamp
     - [ ] Primary color extracted matches manual browser inspection (within 5% RGB)
     - [ ] Typography fonts visible in generated pages (not system defaults)
     - [ ] Side-by-side screenshots compare favorably
     - [ ] All tests passing after using real scraped data

     **Anti-Pattern:**
     Creating sample configs to test integration is GOOD for development,
     but marking work "complete" without running real scraper is FALSE CONFIDENCE.

     **Correct Pattern:**
     1. ✅ Develop with sample data (fast iteration)
     2. ✅ Test integration with sample data (validate code)
     3. ✅ Run actual scraper (validate system)
     4. ✅ Compare output to expectations (validate accuracy)
     5. ✅ THEN mark complete (validated confidence)
     ```
   - Validation: Lesson added to CLAUDE.md with clear checklist

2. **Create Validation Checklist File**
   - File(s): `docs/validation-checklist-style-scraping.md` (new file)
   - Changes: Detailed checklist for future style scraping work
   - Content: Comprehensive checklist covering scraper execution, color validation, visual comparison, documentation
   - Validation: Checklist file exists and is referenced from CLAUDE.md

3. **Update Plan 003 Status**
   - File(s): `plans/003-event-centered-styling-crewai.md`, `plans/README.md`
   - Changes:
     - Mark Phase 6 as "Complete with validation gap (fixed in Plan 004)"
     - Update status to reflect partial completion
     - Reference Plan 004 for validation fix
   - Validation: Plan 003 accurately reflects what was actually validated vs. claimed

4. **Update Completion Report**
   - File(s): `analysis/plan-003-completion-report.md`
   - Changes: Add section at end clarifying validation gap and Plan 004 fix
   - Content:
     ```markdown
     ## Post-Completion Update (2025-11-06)

     **Validation Gap Identified:** Plan 004 revealed that the Event Tech Live
     style config was manually created sample data, not actually scraped from
     eventtechlive.com. This explains the color mismatch (cyan vs. blue).

     **Resolution:** Plan 004 executed the actual scraper and replaced sample
     config with real scraped data. See analysis/exploration-report-2025-11-06-style-mismatch.md
     for full investigation.

     **Lessons:** Updated CLAUDE.md Lesson XX documents this case as example of
     "sample data is not validation data" anti-pattern.
     ```
   - Validation: Completion report updated with correction

5. **Document This Fix**
   - File(s): `analysis/plan-004-validation-report.md` (new file)
   - Changes: Create comprehensive validation report for this plan
   - Content:
     - Before/after color comparison
     - Scraper execution log summary
     - Test results (all passing)
     - Visual validation screenshots
     - Checklist verification
     - Success criteria sign-off
   - Validation: Validation report exists and comprehensively documents the fix

**Validation Checkpoint:**
- [ ] CLAUDE.md updated with new lesson and checklist
- [ ] Validation checklist file created in docs/
- [ ] Plan 003 status updated to reflect validation gap
- [ ] Completion report corrected
- [ ] Plan 004 validation report created
- [ ] All documentation cross-references are correct

## Dependencies

### Prerequisites
- [ ] Python environment set up with dependencies (crewAI, playwright, etc.)
- [ ] OPENAI_API_KEY configured in python/.env
- [ ] Playwright browsers installed (`playwright install`)
- [ ] Node.js environment set up with dependencies
- [ ] Current working directory is project root

### Related Plans
- `plans/003-event-centered-styling-crewai.md` - Original implementation that had validation gap
- `plans/002-event-tech-live-sample-data.md` - Created Event Tech Live attendee data

### External Dependencies
- **OpenAI API**: Required for CrewAI agents (GPT-4 for reasoning)
- **Playwright**: Required for JavaScript-rendered site scraping
- **eventtechlive.com**: Target website must be accessible (check robots.txt, no rate limiting issues)

## Risk Assessment

### High Risk Items

1. **Risk:** Scraper fails to connect to eventtechlive.com due to rate limiting, geo-blocking, or robots.txt restrictions
   - **Likelihood:** Low (site is public conference site, should allow scraping)
   - **Impact:** High (blocks entire fix)
   - **Mitigation:**
     - Check robots.txt before running: `curl https://eventtechlive.com/robots.txt`
     - Use respectful User-Agent (already implemented in WebScraperTool)
     - Increase timeout to 120-180s to avoid premature failures
   - **Contingency:**
     - If rate limited: Wait 5 minutes, retry with longer delays between requests
     - If geo-blocked: Use different network/VPN
     - If robots.txt disallows: Manually inspect CSS, create config with documentation explaining manual extraction

2. **Risk:** Scraped colors differ significantly from manual inspection due to JavaScript-computed styles or theme variations
   - **Likelihood:** Medium (sites with theme switchers or JS-heavy styling)
   - **Impact:** Medium (would need manual adjustment)
   - **Mitigation:**
     - Playwright waits for page load and network idle before scraping
     - StyleAnalystAgent examines computed styles, not just CSS files
     - Manual validation step catches discrepancies
   - **Contingency:**
     - If scraped primary color is wrong: Manually extract from browser DevTools, update JSON, document reason
     - If multiple themes detected: Choose light mode as default, document dark mode exists

3. **Risk:** Tests fail after replacing config due to hard-coded color expectations
   - **Likelihood:** Low (tests designed to be parameterized)
   - **Impact:** Medium (requires test updates)
   - **Mitigation:**
     - Review test code before running to identify hard-coded values
     - Tests use generic validation (valid hex color) not specific values
   - **Contingency:**
     - Update failing tests to use parameterized validation
     - Ensure tests validate "config was loaded and applied" not "config has specific color X"

### Medium Risk Items

1. **Risk:** Generated pages have accessibility issues with new color scheme (contrast ratios)
   - **Likelihood:** Low (eventtechlive.com presumably follows accessibility guidelines)
   - **Impact:** Medium (would need color adjustments)
   - **Mitigation:**
     - HTML validation includes accessibility checks
     - Manual visual inspection catches obvious contrast issues
   - **Contingency:**
     - If contrast ratios fail WCAG: Adjust colors slightly for accessibility, document deviation from scraped values

2. **Risk:** Event Tech Live rebrands or changes website between scraping and demo
   - **Likelihood:** Low (short timeframe)
   - **Impact:** Low (can re-scrape)
   - **Mitigation:**
     - Document scrape date in config metadata
     - Take screenshots of actual site at time of scraping
   - **Contingency:**
     - Re-run scraper if website changes
     - Version style configs by scrape date if needed

3. **Risk:** Documentation updates incomplete or unclear
   - **Likelihood:** Low (detailed checklist in plan)
   - **Impact:** Low (mainly affects future reference)
   - **Mitigation:**
     - Follow documentation checklist systematically
     - Cross-reference all mentioned files
   - **Contingency:**
     - Review documentation in next planning session
     - Solicit feedback on checklist usability

## Rollback Plan

If implementation fails or introduces critical issues, rollback as follows:

### Rollback Steps

1. **Restore Sample Config**
   ```bash
   # Restore original sample config
   cp style-configs/event-tech-live-2025.json.sample style-configs/event-tech-live-2025.json
   ```

2. **Regenerate Pages with Original Config**
   ```bash
   npm run generate
   ```

3. **Verify Rollback**
   ```bash
   # Check pages reverted to cyan
   grep "#00b8d4" dist/attendees/2001/index.html && echo "✅ Rolled back"

   # Run tests
   npm test
   ```

4. **Document Rollback**
   - Create `analysis/plan-004-rollback-$(date +%Y%m%d).md`
   - Document reason for rollback
   - Identify what needs to be fixed before retry

**Validation after rollback:**
- [ ] System is in stable state (tests passing)
- [ ] No data loss (sample config preserved)
- [ ] Previous functionality intact (pages generate successfully)
- [ ] Rollback documented in analysis/

**Note:** Rollback only affects generated pages and style config. Python scraper changes are not rolled back (no Python code changes in this plan).

## Testing Strategy

### Unit Tests

No new unit tests required. This plan uses existing test infrastructure.

- [ ] Existing 81 Python tests validate scraper functionality
- [ ] Existing 139 TypeScript tests validate integration
- [ ] Tests are parameterized and don't hard-code color values

### Integration Tests

- [ ] Run existing integration tests (`npm run test:integration`)
- [ ] Verify styleIntegration.test.ts passes with real scraped config
- [ ] Validate loadStyleConfig → generateEventCSS → render pipeline

### Manual Testing

1. **Scraper Execution Test**
   - Run scraper against eventtechlive.com
   - Verify output JSON is valid
   - Confirm colors match manual inspection

2. **Visual Comparison Test**
   - Open actual website in browser
   - Open generated page in browser
   - Side-by-side comparison of colors, fonts, spacing
   - Take screenshots for documentation

3. **End-to-End Pipeline Test**
   - Delete all generated pages: `rm -rf dist/attendees/`
   - Run generation: `npm run generate`
   - Verify 24 pages regenerated
   - Spot-check 3-4 pages for correct styling

### Validation Commands

```bash
# Verify scraper output exists and is valid
test -f python/style-configs/eventtechlive-com.json && echo "✅ Scraper output exists"
jq empty python/style-configs/eventtechlive-com.json && echo "✅ Valid JSON"

# Verify config has correct color (approximately)
PRIMARY_COLOR=$(jq -r '.colors.primary' style-configs/event-tech-live-2025.json)
[[ "$PRIMARY_COLOR" == "#3182CE" ]] || [[ "$PRIMARY_COLOR" == "#3182ce" ]] && echo "✅ Primary color correct"

# Verify generated pages use correct color
grep -q "#3182CE\|#3182ce" dist/attendees/2001/index.html && echo "✅ Pages use correct color"

# Run all tests
cd python && PYTHONPATH=./src pytest tests/unit/ -v && cd ..
npm test

# Validate HTML
npm run validate:html

# Check overall success
echo "✅ All validation passed - Plan 004 complete"
```

## Post-Implementation

### Documentation Updates
- [ ] Update CLAUDE.md with Lesson 19/20 (sample data case study)
- [ ] Create docs/validation-checklist-style-scraping.md
- [ ] Update plans/README.md index with Plan 004
- [ ] Update analysis/plan-003-completion-report.md with correction
- [ ] Create analysis/plan-004-validation-report.md

### Knowledge Capture
- [ ] Document root cause of validation gap in CLAUDE.md
- [ ] Create reusable validation checklist for future style scraping
- [ ] Capture before/after screenshots for visual reference
- [ ] Save scraper execution logs for traceability
- [ ] Document manual validation process in checklist

### Optional Enhancements (Not Blocking)
- [ ] Create pre-commit hook to warn about style config commits
- [ ] Create validation script (scripts/validate-e2e.sh) to automate checks
- [ ] Add visual regression testing framework evaluation to backlog
- [ ] Create color accuracy validation tool (compare scraped vs. actual)

## Appendix

### References
- **Exploration Report:** `analysis/exploration-report-2025-11-06-style-mismatch.md`
- **Plan 003:** `plans/003-event-centered-styling-crewai.md`
- **Plan 003 Completion Report:** `analysis/plan-003-completion-report.md`
- **CLAUDE.md Lesson 16:** End-to-End Validation is NON-NEGOTIABLE
- **Event Tech Live Website:** https://eventtechlive.com

### Alternative Approaches Considered

1. **Approach:** Manually create corrected config without running scraper
   - **Pros:** Fast, no dependencies on scraper working
   - **Cons:** Defeats purpose of automated scraping, doesn't validate scraper, perpetuates manual process
   - **Why not chosen:** Plan 003's value proposition is automated scraping; must validate it actually works

2. **Approach:** Only update colors in existing sample config
   - **Pros:** Minimal changes, fast
   - **Cons:** Doesn't validate typography/layout extraction, doesn't test full pipeline, other values might also be wrong
   - **Why not chosen:** Need to validate complete scraper functionality, not just color extraction

3. **Approach:** Accept sample data and document it as limitation
   - **Pros:** No additional work needed
   - **Cons:** Undermines credibility, cannot demo confidently, doesn't solve user-facing problem
   - **Why not chosen:** Brand inconsistency is unacceptable for production use

### Notes

- **Estimated Time:** 1-2 hours for implementation, 1 hour for documentation = 2-3 hours total
- **User Impact:** High - fixes immediately visible brand inconsistency
- **Technical Complexity:** Low - leverages existing working infrastructure
- **Validation Rigor:** High - multiple validation methods, comprehensive checklist
- **Reusability:** High - establishes pattern for future style scraping validation

---

**Plan Status:** Draft - Awaiting Approval
**Next Action:** Review plan, validate target outcomes, confirm to proceed with implementation
**Implementation Command:** `/implement ./plans/004-fix-event-tech-live-style-mismatch.md`
