# Exploration Report: Plan 005 - Playwright-Based Scraping Tool

**Date**: 2025-11-07
**Explorer**: Claude Code
**Focus**: plans/005-playwright-scraping-tool.md implementation status and validation

## Executive Summary

Plan 005 aims to solve the critical problem that CrewAI agents hallucinate website content instead of actually scraping it. The plan proposes implementing `PlaywrightStyleExtractorTool` to replace AI guessing with real browser automation.

**Key Finding**: **Plan 005 is only PARTIALLY implemented** (Phases 1-3 complete, Phases 4-5 incomplete). The Playwright tool exists and passes unit tests, but the agent **does not actually use it during execution** - it still hallucinates content despite having the tool available.

## Implementation Status by Phase

### Phase 1: Core Playwright Tool Implementation ✅ COMPLETE

**Status**: Fully implemented (commits cb2b040, b661608)

**Evidence**:
- ✅ Tool file exists: `python/src/event_style_scraper/tools/playwright_scraper.py`
- ✅ Exported from `tools/__init__.py`
- ✅ Playwright browsers installed (v1.55.0)
- ✅ Tool implements all required methods: `_run()`, `_async_run()`
- ✅ Extracts HTML, computed styles, CSS variables, and assets
- ✅ Uses `asyncio.run()` bridge for sync/async compatibility

**Validation**:
```bash
# Tool can be imported and instantiated
from event_style_scraper.tools import PlaywrightStyleExtractorTool
tool = PlaywrightStyleExtractorTool(timeout=30000)
# ✅ PASS
```

### Phase 2: Unit Tests for Playwright Tool ✅ COMPLETE

**Status**: Fully implemented

**Evidence**:
- ✅ Test file: `python/tests/unit/test_playwright_scraper.py` (9 tests)
- ✅ Test fixture: `tests/fixtures/simple-page.html` (controlled HTML with known styles)
- ✅ All 9 tests passing (7.06s execution time)
- ✅ 100% coverage for `playwright_scraper.py`

**Test Coverage**:
```
test_playwright_scraper.py::TestPlaywrightStyleExtractorTool
  ✅ test_tool_instantiation
  ✅ test_tool_extracts_html
  ✅ test_tool_extracts_computed_styles
  ✅ test_tool_extracts_css_variables
  ✅ test_tool_extracts_multiple_elements
  ✅ test_tool_respects_timeout
  ✅ test_tool_validates_url_security
  ✅ test_tool_returns_structured_data
  ✅ test_tool_extracts_assets

Coverage: 23/23 statements (100%)
```

**Validation**: Tests use `file://` URLs with local fixtures to verify:
- HTML extraction accuracy
- Computed style measurement (header background: `rgb(22, 8, 34)` = `#160822`)
- CSS variable extraction from `:root`
- Asset URL detection (logo, favicon)

### Phase 3: Agent Integration ⚠️ PARTIALLY COMPLETE

**Status**: Code implemented, but agent does NOT use the tool

**Evidence of Integration**:
- ✅ Tool assigned to agent: `style_extraction_crew.py:53`
  ```python
  tools=[PlaywrightStyleExtractorTool(timeout=self.timeout * 1000)]
  ```
- ✅ Task description updated: `config/tasks.yaml:1-32` (emphasizes tool usage)
- ✅ Test confirms tool assignment: `test_web_scraper_agent_has_playwright_tool` ✅ PASS

**Evidence of Non-Usage (CRITICAL ISSUE)**:

Ran actual scraper CLI: `python -m event_style_scraper scrape --url https://example.com --timeout 90`

**Observed Behavior**:
1. Agent task description mentions "Use Playwright" ✅
2. Agent has tool available in `tools=[]` array ✅
3. **Agent NEVER calls the tool** ❌
4. Agent generates fictional HTML/CSS from imagination ❌
5. Agent output contains:
   - Invented HTML structure for example.com
   - Made-up CSS rules (`#site-header { background-color: #004080; }`)
   - Fabricated external stylesheet content (`/css/main.css`)
   - Simulated dark mode styles
   - Fictional logo URLs

**Logs Show**:
```
🤖 Agent: Web Content Scraper
📋 Task: "Use the Playwright Style Extractor tool to scrape..."
🧠 Thinking...
✅ Agent Final Answer: [Fabricated scraping report with made-up HTML/CSS]
```

**What's Missing**: No log line showing `"Tool: PlaywrightStyleExtractorTool"` or tool invocation

**Root Cause**: Agent is not actually calling the tool. Despite having access to it, the agent generates plausible-sounding content without running the Playwright automation.

### Phase 4: Integration Testing with Real Websites ❌ NOT IMPLEMENTED

**Status**: Not started

**Expected Artifacts** (from plan):
- `tests/integration/test_real_scraping.py` ❌ MISSING
- `scripts/validate_scraped_colors.py` ❌ MISSING

**Actual State**:
```bash
$ ls python/tests/integration/
__init__.py  # Empty directory
```

**Missing Tests**:
- ❌ `test_scrape_example_com()` - Scrape and validate example.com
- ❌ `test_scrape_eventtechlive_com()` - Verify #160822 color extraction
- ❌ DevTools validation script - Automated color comparison

**Impact**: No empirical validation that the tool produces accurate output when scraping real websites.

### Phase 5: Validation Pipeline & Documentation ❌ NOT IMPLEMENTED

**Status**: Not started

**Expected Artifacts** (from plan):
- `docs/scraper-validation-checklist.md` ❌ MISSING
- CLAUDE.md Lesson 19: "Agents Need Tools, Not Just Instructions" ❌ MISSING
- `.github/workflows/validate-scraper.yml` ❌ MISSING

**Actual State**:
```bash
$ find . -name "scraper-validation-checklist.md"
# No results
```

**Impact**: No validation workflow, no documented best practices, no CI/CD enforcement.

## Critical Gap Analysis

### The Tool vs. Agent Problem

**The Disconnect**:
```
Tool Implementation:       ✅ Working perfectly (100% test coverage)
Agent Integration:         ⚠️ Tool assigned but NOT USED
End-to-End Validation:     ❌ Never tested with real websites
```

**What Plan 005 Promises**:
> "Solution: Implement PlaywrightStyleExtractorTool that uses actual browser automation to navigate to URLs, execute JavaScript, extract computed styles via DevTools Protocol, and return real measurements (not AI guesses)."

**What Actually Happens**:
1. Tool exists ✅
2. Agent has tool available ✅
3. Agent generates fictional content anyway ❌
4. Tool never executes ❌

**Evidence from Live Scrape**:

| Plan Expectation | Actual Behavior |
|------------------|-----------------|
| Agent calls PlaywrightStyleExtractorTool | Agent never calls tool |
| Tool opens browser and measures styles | No browser launched |
| Returns actual `rgb(22, 8, 34)` from DevTools | Returns made-up `rgb(0, 64, 128)` |
| Extracts real HTML from DOM | Fabricates HTML with fictional IDs |
| No hallucinated CSS | Entire CSS invented by AI |

### Success Criteria Validation

From Plan 005 success criteria:

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Scrape eventtechlive.com and extract actual header color (#160822) | ❌ FAIL | Agent hasn't been tested against real site |
| Scrape example.com and extract real colors | ❌ FAIL | Agent fabricated colors (#004080 instead of real colors) |
| All scraped colors verified against DevTools | ❌ FAIL | No DevTools comparison performed |
| Tool integration: agent calls PlaywrightStyleExtractorTool | ❌ FAIL | Agent has tool but doesn't call it |
| Zero hallucinated HTML/CSS in scraper output | ❌ FAIL | Entire output is hallucinated |
| 100% of test cases pass (unit + integration) | ⚠️ PARTIAL | Unit tests pass, integration tests don't exist |
| Coverage ≥80% for new tool code | ✅ PASS | 100% coverage for tool itself |
| Manual validation: Side-by-side comparison shows perfect color match | ❌ FAIL | Not performed |

**Overall Success Rate**: 1/8 criteria met (12.5%)

## Hypothesis Validation Results

### Hypothesis 1: Playwright can extract actual computed styles from browser

**Status**: ✅ VALIDATED (unit tests)

**Evidence**: Tool correctly extracts `rgb(22, 8, 34)` from test fixture header
- Test: `test_tool_extracts_computed_styles` ✅ PASS
- Fixture has `--primary-color: #160822`
- Tool returns `"backgroundColor": "rgb(22, 8, 34)"` ✅ Correct conversion

**Conclusion**: Playwright works perfectly when called. Problem is agent doesn't call it.

### Hypothesis 2: CrewAI agents can call custom Playwright tool

**Status**: ⚠️ PARTIALLY VALIDATED (unit tests show tool is assigned, but NOT actually called)

**Evidence**:
- Test: `test_web_scraper_agent_has_playwright_tool` ✅ PASS
  ```python
  assert len(agent.tools) == 1
  assert isinstance(agent.tools[0], PlaywrightStyleExtractorTool)
  ```
- But live execution shows: Agent has tool, doesn't use it ❌

**Conclusion**: Tool CAN be assigned to agents, but agents need additional configuration/prompting to actually invoke it.

### Hypothesis 3: Extracted styles enable accurate style config generation

**Status**: ❌ NOT VALIDATED (hypothesis untested)

**Evidence**: Cannot validate because agent never calls tool to get real styles

**Conclusion**: Hypothesis remains untested. Requires Phase 4 integration tests.

## Test Coverage Analysis

### Unit Test Coverage: 94% Overall

```
TOTAL: 321 statements, 18 missed, 94% coverage
```

**Breakdown by Module**:
```
playwright_scraper.py:        23/23 (100%) ✅
style_extraction_crew.py:     48/48 (100%) ✅
content_creation_crew.py:     47/47 (100%) ✅
types.py:                      46/46 (100%) ✅
cli.py:                        38/39 ( 97%) ✅
style_scraping_flow.py:        52/55 ( 95%) ✅
web_scraper.py:                41/50 ( 82%) ⚠️
__main__.py:                    0/5  (  0%) ❌
```

**Coverage Gaps**:
- No integration tests (0 files in `tests/integration/`)
- No end-to-end tests validating actual scraping
- CLI `__main__.py` not tested (entry point)

### Test Execution Performance

```
91 unit tests passed in 8.06 seconds
9 Playwright tests: 7.06 seconds (78% of total test time)
```

**Performance Note**: Playwright tests are slowest (browser automation overhead), but still acceptable for unit tests.

## Architectural Analysis

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User / CLI                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           StyleScrapingFlow (Orchestration)                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           StyleExtractionCrew (CrewAI)                      │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ WebScraper  │→ │ StyleAnalyst│→ │ VoiceAnalyst│ →      │
│  │   Agent     │  │   Agent     │  │   Agent     │        │
│  └──────┬──────┘  └─────────────┘  └─────────────┘        │
│         │                                                   │
│         │ tools=[PlaywrightStyleExtractorTool]             │
│         ▼                                                   │
│  ┌─────────────────────────────────────┐                   │
│  │  PlaywrightStyleExtractorTool       │                   │
│  │  (ASSIGNED BUT NOT USED)            │ ❌                │
│  └─────────────────────────────────────┘                   │
│                                                             │
│  ┌─────────────┐                                           │
│  │ Compiler    │                                           │
│  │   Agent     │ → EventStyleConfig JSON                   │
│  └─────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│        Output: python/style-configs/{domain}.json           │
│        (Contains HALLUCINATED data, not real scrape)  ❌    │
└─────────────────────────────────────────────────────────────┘
```

**The Problem**: Arrow from WebScraper Agent → Tool is dotted because agent doesn't actually invoke the tool.

### Data Flow (Expected vs Actual)

**Expected Flow** (Plan 005 design):
```
1. User: python -m event_style_scraper scrape --url https://example.com
2. CLI → StyleScrapingFlow.start()
3. Flow → StyleExtractionCrew.kickoff()
4. Crew → WebScraper Agent: "Use Playwright tool to scrape {url}"
5. Agent → PlaywrightStyleExtractorTool._run(url)
   ↓
6. Tool: Launch Chromium browser
7. Tool: Navigate to URL and wait for network idle
8. Tool: Execute JavaScript to extract computed styles
9. Tool: Return { html, computed_styles, css_variables, assets }
   ↓
10. Agent → StyleAnalyst Agent: [Real scraped data]
11. StyleAnalyst → VoiceAnalyst → Compiler
12. Compiler → EventStyleConfig JSON with REAL colors
```

**Actual Flow** (observed behavior):
```
1. User: python -m event_style_scraper scrape --url https://example.com
2. CLI → StyleScrapingFlow.start()
3. Flow → StyleExtractionCrew.kickoff()
4. Crew → WebScraper Agent: "Use Playwright tool to scrape {url}"
5. Agent: [Thinks] "I'll generate plausible HTML/CSS for this URL"
   ↓ (Tool never called!)
6. Agent → StyleAnalyst Agent: [Hallucinated HTML/CSS]
7. StyleAnalyst → VoiceAnalyst → Compiler
8. Compiler → EventStyleConfig JSON with FAKE colors (#004080 instead of real)
9. Error: "Expecting value: line 1 column 1 (char 0)" ❌
```

**Critical Difference**: Step 5 diverges. Agent doesn't call tool, invents data instead.

## Root Cause Analysis

### Why Agent Doesn't Call Tool

**Possible Reasons**:

1. **Task Description Ambiguity**
   - Current: "Use the Playwright Style Extractor tool to scrape..."
   - Agent may interpret "use" as "use the approach" not "invoke the tool"
   - Needs more explicit instruction: "CALL the tool named 'Playwright Style Extractor' with the URL"

2. **LLM Default Behavior**
   - LLMs are trained to generate plausible text
   - When asked "what's on example.com?", LLM naturally generates fictional HTML
   - Tool usage requires explicit prompting and reinforcement

3. **Missing Tool Enforcement**
   - No validation that tool was called
   - No rejection of output if tool wasn't invoked
   - Agent can "succeed" without using tool

4. **CrewAI Configuration**
   - May need `force_tool_use=True` or similar flag
   - May need tool description refinement
   - May need examples of tool usage in prompt

5. **Output Format Mismatch**
   - Agent expects to write prose report
   - Tool returns structured dict
   - Agent may not know how to bridge formats

### Comparison to Plan 003/004 Lessons

**Lesson 16**: "End-to-End Validation is NON-NEGOTIABLE"
- ❌ Plan 005 violated this: No E2E tests in Phase 4
- ✅ Unit tests pass, but system doesn't work

**Lesson 17**: "Sample/Mock Data Can Hide Critical Flaws"
- ❌ Plan 005 violated this: Only tested with fixtures, not real websites
- ✅ Unit tests use `file://` URLs with known HTML

**Lesson 18**: "Verify Scraper Output with DevTools"
- ❌ Plan 005 violated this: No DevTools validation performed
- ❌ Phase 5 validation scripts not implemented

**Pattern**: Plan 005 repeated the EXACT mistakes from Plans 003/004 that the lessons warn against.

## Recommendations

### Immediate Actions (Unblock Plan 005)

1. **Fix Agent Tool Invocation** (Priority 🔴 Critical)
   - Update task description to explicitly require tool call
   - Add validation: Reject output if tool wasn't invoked
   - Add examples in agent backstory showing how to use tool
   - Consider using CrewAI's `@tool` decorator with explicit examples

2. **Implement Phase 4 Integration Tests** (Priority 🔴 Critical)
   - Create `tests/integration/test_real_scraping.py`
   - Add `test_scrape_example_com()` with real URL
   - Add `test_scrape_eventtechlive_com()` with color validation
   - Verify tool is actually called (check logs or mock tool)

3. **Implement Phase 5 Validation** (Priority 🟡 High)
   - Create `scripts/validate_scraped_colors.py`
   - Add DevTools comparison logic
   - Document validation checklist
   - Add GitHub Actions workflow

### Validation Checklist for Phase 4

**Before marking Phase 4 complete, verify**:

- [ ] Run actual scraper against example.com: `python -m event_style_scraper scrape --url https://example.com`
- [ ] Check logs for `"Tool: PlaywrightStyleExtractorTool"` - tool was called
- [ ] Verify output JSON contains real data, not fictional:
  - [ ] HTML contains actual example.com content
  - [ ] Colors match DevTools inspection
  - [ ] No invented CSS rules
- [ ] Compare colors with DevTools:
  - [ ] Open example.com in Chrome
  - [ ] Inspect elements, note colors
  - [ ] Compare to scraped JSON (±2 RGB units)
- [ ] Run integration tests: `pytest tests/integration/ -v`
- [ ] All integration tests pass
- [ ] Zero hallucinated content in output

### Long-Term Improvements

1. **Add Logging**
   - Log when tool is called: `"Calling PlaywrightStyleExtractorTool with URL: {url}"`
   - Log tool output summary: `"Tool extracted {len(html)} chars HTML, {len(styles)} elements"`
   - Log when agent skips tool: `"WARNING: Agent generated content without calling tool"`

2. **Add Validation Layer**
   - Before accepting agent output, validate:
     - Was tool called? (check logs)
     - Does output contain tool's fingerprint? (unique markers)
     - Are colors/fonts realistic? (not generic guesses)
   - Reject and retry if validation fails

3. **Improve Tool Discoverability**
   - Rename tool to be more explicit: `ActualWebsiteScraperTool`
   - Add docstring with usage examples
   - Update agent backstory with explicit tool usage pattern

4. **Add Monitoring**
   - Track: % of runs where tool is called vs. skipped
   - Alert if tool usage drops below 100%
   - Dashboard showing scraper accuracy over time

## Related Documentation

- **Plan 005**: `plans/005-playwright-scraping-tool.md`
- **Plan 003**: `plans/003-event-centered-styling-crewai.md` - Original scraper implementation
- **Plan 004**: `plans/004-fix-event-tech-live-style-mismatch.md` - Color mismatch fix
- **PRD-002**: `requirements/PRD-002.md` - Original requirements for style scraping
- **CLAUDE.md Lessons**:
  - Lesson 16: End-to-End Validation is NON-NEGOTIABLE
  - Lesson 17: Sample/Mock Data Can Hide Critical Flaws
  - Lesson 18: Verify Scraper Output with DevTools

## Conclusion

**Plan 005 Status**: 📝 **Draft** (correctly marked, not ready for "Completed")

**Implementation Progress**: 37.5% complete (3/8 phases)
- ✅ Phase 1: Core Tool Implementation (100%)
- ✅ Phase 2: Unit Tests (100%)
- ⚠️ Phase 3: Agent Integration (50% - assigned but not used)
- ❌ Phase 4: Integration Testing (0%)
- ❌ Phase 5: Validation Pipeline (0%)

**Readiness for Production**: ❌ NOT READY

**Blocker**: Agent doesn't call the tool despite having access to it. This defeats the entire purpose of Plan 005.

**Next Steps**:
1. Debug why agent doesn't invoke tool
2. Implement Phase 4 integration tests
3. Validate against real websites with DevTools
4. Only then mark as "In Progress" or "Completed"

**Key Insight**: This case study reinforces CLAUDE.md lessons:
- Unit tests passing ≠ system working (Lesson 16)
- Mock data hides real-world bugs (Lesson 17)
- Must validate with actual target environment (Lesson 18)

Plan 005 is well-designed on paper, partially implemented in code, but not yet delivering value because the critical integration (agent → tool invocation) is broken.

---

**Report Generated**: 2025-11-07
**Report Type**: Exploration + Validation
**Focus Areas**: Plan 005 implementation status, agent tool usage, end-to-end validation gaps
