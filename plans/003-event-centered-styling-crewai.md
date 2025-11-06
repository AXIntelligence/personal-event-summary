# Plan 003: Event-Centered Styling with CrewAI Web Scraping

**Status:** ⏸️ In Progress (Paused at Phase 2) - 2/7 Phases Complete (29%)
**Created:** 2025-11-06
**Last Updated:** 2025-11-06
**Priority:** 🟡 High

**Progress Summary:**
- ✅ Phase 1: Python/CrewAI Environment Setup (Complete - Commit 1fd2458)
- ✅ Phase 2: Web Scraping Crew Implementation (Complete - Commit 27062e2)
- ❌ Phases 3-7: Remaining (Flow, Content Crew, TypeScript, Testing, Deployment)
- 📊 Test Coverage: 94% (39/39 tests passing)
- 📝 Progress Report: analysis/plan-003-implementation-progress.md

## Overview

This plan implements PRD-002 requirements for event-centered styling by introducing a Python/crewAI layer with two specialized multi-agent crews: (1) a style extraction crew that scrapes event websites to extract styling, branding, and voice characteristics, and (2) a content creation crew that generates personalized content using the scraped styles and brand voice, integrating directly with our GitHub Pages build/deploy system. The implementation leverages proven patterns from the book_wizards project, using multi-agent crews with specialized sub-agents for complex scraping, analysis, content generation, and validation tasks.

The architecture employs a dual-crew approach: The first crew (StyleExtractionCrew) handles intelligent web scraping and style analysis, while the second crew (ContentCreationCrew) uses those extracted styles to generate enhanced, brand-aligned content for attendee pages. The existing TypeScript/Handlebars system continues to handle final page generation, but now receives both styling configuration and AI-enhanced content from the crewAI layer. This hybrid approach minimizes changes to the production-ready generation pipeline while adding sophisticated AI-powered styling and content creation capabilities.

## Target Outcomes

### Primary Outcomes
1. **Automated style extraction** from event websites using crewAI web scraping crew
2. **Dynamic CSS generation** based on scraped brand colors, typography, and design patterns
3. **Brand voice analysis** to match event tone in generated content
4. **AI-powered content creation** using ContentCreationCrew that generates personalized attendee content
5. **GitHub Pages integration** with content creation crew directly using build/deploy system
6. **Markus AI branding** integration with footer attribution
7. **Enhanced personalization** through AI-generated content that matches event brand voice
8. **JSON style configs and content** that integrate seamlessly with existing TypeScript pipeline

### Success Criteria
- [ ] Event pages visually match source event website (color scheme, typography, spacing)
- [ ] Brand voice analysis correctly identifies tone (professional/casual/energetic/sophisticated)
- [ ] Content creation crew generates personalized content for each attendee
- [ ] Generated content reflects event's brand voice and messaging style
- [ ] ContentCreationCrew integrates with GitHub Pages build/deploy pipeline
- [ ] Scraped styles apply correctly to all 24 existing attendee pages
- [ ] Markus AI footer attribution displays on all generated pages
- [ ] Zero regression in existing functionality (tests still pass at 89.93%+ coverage)
- [ ] Style extraction completes in < 60 seconds per event website
- [ ] Content generation completes in < 30 seconds per attendee
- [ ] Generated CSS validates without errors
- [ ] Integration requires minimal changes to existing Handlebars templates

### Validation Strategy

#### Empirical Validation Methods
- **Method 1: Visual Similarity Validation**
  - Tools/Commands: `python -m event_style_scraper.validate --compare-screenshots`
  - Expected Results: 80%+ visual similarity score between source and generated pages
  - Acceptance Threshold: Colors match within 5% tolerance, fonts correctly identified

- **Method 2: Style Config Validation**
  - Tools/Commands: `ajv validate -s style-schema.json -d style-configs/*.json`
  - Expected Results: All style configs pass JSON schema validation
  - Acceptance Threshold: 100% valid JSON with all required fields populated

- **Method 3: CSS Generation Validation**
  - Tools/Commands: `npx stylelint dist/static/css/event-*.css`
  - Expected Results: Generated CSS files have 0 errors, < 5 warnings
  - Acceptance Threshold: Valid CSS that applies correctly in all modern browsers

- **Method 4: Integration Testing**
  - Tools/Commands: `npm test && python -m pytest tests/`
  - Expected Results: All existing TypeScript tests pass, new Python tests pass
  - Acceptance Threshold: 100% test pass rate, coverage maintained at 85%+

- **Method 5: Brand Voice Accuracy**
  - Tools/Commands: Sub-agent validation using `VoiceValidationAgent`
  - Expected Results: Identified tone matches manual assessment in 4/5 test cases
  - Acceptance Threshold: 80% accuracy in tone identification

- **Method 6: Content Generation Quality**
  - Tools/Commands: `python -m event_style_scraper.validate --content-quality`
  - Expected Results: Generated content scores 4+/5 on relevance, personalization, brand alignment
  - Acceptance Threshold: Average quality score ≥ 4.0 across all dimensions

- **Method 7: GitHub Pages Integration**
  - Tools/Commands: `npm run build && python -m event_style_scraper generate --trigger-deploy`
  - Expected Results: Content flows through pipeline, pages deploy successfully
  - Acceptance Threshold: Full end-to-end pipeline executes without manual intervention

## Hypothesis-Driven Approach

### Hypothesis 1: Multi-agent crews can reliably extract visual styles from websites
**Reasoning:** Specialized agents focusing on specific aspects (colors, typography, layout) will be more accurate than a single general-purpose scraper. The book_wizards pattern of task specialization has proven effective for complex multi-step processes.

**Validation Method:**
- Experiment: Scrape 3 test websites (TechConf, Event Tech Live, Markus AI)
- Expected Outcome: Extracted styles match manual inspection
- Validation Steps:
  1. Run scraping crew on test websites
  2. Compare extracted colors with browser DevTools color picker
  3. Verify font families match computed styles
  4. Validate spacing measurements against actual CSS

**Success Criteria:**
- [ ] Primary colors extracted within RGB(5,5,5) tolerance
- [ ] Font families correctly identified (exact match or fallback)
- [ ] Layout grid system detected (12-column, flexbox, or grid)
- [ ] Logo and favicon URLs successfully extracted

**Failure Conditions:**
- Colors off by more than 10%
- Fallback approach: Provide manual override configuration

### Hypothesis 2: CSS custom properties enable dynamic styling without template changes
**Reasoning:** Using CSS variables for all style values allows us to inject scraped styles without modifying Handlebars templates. This maintains backward compatibility and simplifies integration.

**Validation Method:**
- Experiment: Generate test pages with injected CSS variables
- Expected Outcome: Pages render with dynamic styles
- Validation Steps:
  1. Create test CSS with custom properties
  2. Generate pages with different style configs
  3. Verify visual changes without template modifications
  4. Test in Chrome, Firefox, Safari

**Success Criteria:**
- [ ] All style properties use CSS variables
- [ ] Style injection requires zero template changes
- [ ] Pages render correctly in 3+ browsers
- [ ] Fallback values work when variables undefined

**Failure Conditions:**
- CSS variables not supported in target browsers
- Fallback approach: Generate static CSS files per event

### Hypothesis 3: Sub-agents improve complex task accuracy and reliability
**Reasoning:** Using specialized sub-agents for validation, error checking, and quality assurance (similar to book_wizards' Judi agent doing vocabulary validation) will catch issues that primary agents miss.

**Validation Method:**
- Experiment: Compare results with and without validation sub-agents
- Expected Outcome: Sub-agents catch 80%+ of extraction errors
- Validation Steps:
  1. Run scraping with primary agents only
  2. Run scraping with validation sub-agents
  3. Compare accuracy and error rates
  4. Measure false positive/negative rates

**Success Criteria:**
- [ ] ValidationAgent catches invalid color formats
- [ ] QualityAgent identifies missing required fields
- [ ] ConsistencyAgent detects conflicting styles
- [ ] Error rate reduced by 50%+ with sub-agents

**Failure Conditions:**
- Sub-agents introduce more errors than they catch
- Fallback approach: Single agent with comprehensive validation

### Hypothesis 4: ContentCreationCrew can generate brand-aligned content that integrates with GitHub Pages
**Reasoning:** A dedicated crew for content creation that understands both the event's brand voice and our GitHub Pages pipeline will generate more personalized and engaging content than static templates alone. Using the scraped brand voice data, the crew can create content that feels authentic to the event while maintaining the technical structure needed for our build system.

**Validation Method:**
- Experiment: Generate content for 5 different attendee profiles using scraped brand voice
- Expected Outcome: Content reflects event personality while maintaining data integrity
- Validation Steps:
  1. Scrape and analyze event brand voice
  2. Generate content for diverse attendee profiles
  3. Verify content integrates with existing JSON structure
  4. Build and deploy pages using GitHub Actions
  5. Assess content quality and brand alignment

**Success Criteria:**
- [ ] Content maintains JSON schema compatibility
- [ ] Brand voice consistency score ≥ 85%
- [ ] Personalization increases engagement metrics
- [ ] GitHub Pages build succeeds without modifications
- [ ] Content generation triggers automatic deployment

**Failure Conditions:**
- Generated content breaks existing data structure
- Fallback approach: Generate supplementary content files instead of modifying core data

### Hypothesis 5: Playwright provides reliable cross-site scraping capability
**Reasoning:** Playwright handles JavaScript-rendered content, authentication, and complex page interactions better than simple HTTP requests. This is critical for modern event websites using React/Vue/Angular.

**Validation Method:**
- Experiment: Scrape 5 different event website technologies
- Expected Outcome: Successful extraction from all site types
- Validation Steps:
  1. Test static HTML site
  2. Test React SPA
  3. Test server-rendered site
  4. Test authenticated content
  5. Test lazy-loaded content

**Success Criteria:**
- [ ] Extracts styles from 5/5 test sites
- [ ] Handles JavaScript-rendered content
- [ ] Respects robots.txt and rate limits
- [ ] Completes within 60-second timeout

**Failure Conditions:**
- Cannot scrape JavaScript-heavy sites
- Fallback approach: Combine Playwright with BeautifulSoup

## Implementation Details

### Phase 1: Python/CrewAI Environment Setup
**Objective:** Establish Python project structure alongside existing TypeScript codebase

**Steps:**
1. Create Python project directory structure
   - File(s) affected: `python/` directory tree
   - Changes: New directory with src, tests, configs
   - Validation: Directory structure matches book_wizards pattern

2. Initialize Python package configuration
   - File(s) affected: `python/pyproject.toml`, `python/requirements.txt`
   - Changes: Add crewAI, Playwright, Pydantic dependencies
   - Validation: `cd python && pip install -e .` succeeds

3. Create Pydantic data models
   - File(s) affected: `python/src/event_style_scraper/types.py`
   - Changes: Define EventStyleConfig, ColorPalette, Typography, BrandVoice
   - Validation: Models instantiate with test data

4. Set up security-hardened tool wrappers
   - File(s) affected: `python/src/event_style_scraper/tools/`
   - Changes: Create WebScraperTool with URL validation, timeout, single-use
   - Validation: Security tests pass (path traversal, SSRF prevention)

**Validation Checkpoint:**
- [ ] Python environment installs without conflicts
- [ ] Pydantic models validate test data correctly
- [ ] Security tests pass for tool wrappers
- [ ] Can import crewAI and instantiate basic crew

### Phase 2: Web Scraping Crew Implementation
**Objective:** Create multi-agent crew for intelligent web scraping

**Steps:**
1. Define agent configurations
   - File(s) affected: `python/src/event_style_scraper/crews/style_extraction_crew/config/agents.yaml`
   - Changes: Define WebScraperAgent, StyleAnalystAgent, VoiceAnalystAgent
   - Validation: Agents instantiate with correct roles

2. Define task pipeline
   - File(s) affected: `python/src/event_style_scraper/crews/style_extraction_crew/config/tasks.yaml`
   - Changes: 4-stage pipeline: scrape → extract_styles → analyze_voice → compile
   - Validation: Tasks have proper context dependencies

3. Implement crew orchestration
   - File(s) affected: `python/src/event_style_scraper/crews/style_extraction_crew/style_extraction_crew.py`
   - Changes: Create crew class with agents, tasks, and Playwright tool
   - Validation: Crew executes test scraping successfully

4. Add validation sub-agents
   - File(s) affected: `python/src/event_style_scraper/crews/style_extraction_crew/validation_agents.py`
   - Changes: ColorValidationAgent, CSSValidationAgent, ConsistencyAgent
   - Validation: Sub-agents catch intentionally malformed data

**Validation Checkpoint:**
- [ ] Crew successfully scrapes test website
- [ ] Agents collaborate with proper context passing
- [ ] Validation sub-agents catch 80%+ of test errors
- [ ] Output matches EventStyleConfig schema

### Phase 3: Style Extraction Flow
**Objective:** Implement flow orchestration for style scraping process

**Steps:**
1. Create flow state management
   - File(s) affected: `python/src/event_style_scraper/flows/style_scraping_flow.py`
   - Changes: Define StyleScrapingState with Pydantic
   - Validation: State transitions work correctly

2. Implement scraping stage
   - File(s) affected: `python/src/event_style_scraper/flows/style_scraping_flow.py`
   - Changes: @start() method initiates crew, handles errors
   - Validation: Scraping completes or fails gracefully

3. Implement export stage
   - File(s) affected: `python/src/event_style_scraper/flows/style_scraping_flow.py`
   - Changes: @listen() method exports JSON to style-configs/
   - Validation: JSON files created with correct schema

4. Add CLI interface
   - File(s) affected: `python/src/event_style_scraper/main.py`
   - Changes: Click-based CLI for scraping command
   - Validation: `python -m event_style_scraper scrape --url https://example.com`

**Validation Checkpoint:**
- [ ] Flow executes end-to-end successfully
- [ ] JSON configs exported to correct location
- [ ] CLI interface works with various options
- [ ] Error handling prevents crashes

### Phase 4: Content Creation Crew Implementation
**Objective:** Create website content generation crew that uses scraped styles and integrates with GitHub Pages build/deploy

**Steps:**
1. Define content creation agents
   - File(s) affected: `python/src/event_style_scraper/crews/content_creation_crew/config/agents.yaml`
   - Changes: ContentWriterAgent, PersonalizationAgent, BrandVoiceAgent, QualityEditorAgent
   - Validation: Agents instantiate with appropriate capabilities

2. Define content generation tasks
   - File(s) affected: `python/src/event_style_scraper/crews/content_creation_crew/config/tasks.yaml`
   - Changes: Pipeline: analyze_attendee → generate_personalized_content → apply_brand_voice → quality_check
   - Validation: Tasks produce content matching event voice

3. Implement content creation crew
   - File(s) affected: `python/src/event_style_scraper/crews/content_creation_crew/content_creation_crew.py`
   - Changes: Crew that takes attendee data + style config and generates enhanced content
   - Validation: Generated content reflects event brand voice

4. Create content enhancement sub-agents
   - File(s) affected: `python/src/event_style_scraper/crews/content_creation_crew/enhancement_agents.py`
   - Changes: MetaphorAgent, StorytellingAgent, PersonalInsightsAgent, CallToActionAgent
   - Validation: Sub-agents enhance content quality measurably

5. Integrate with GitHub Pages pipeline
   - File(s) affected: `python/src/event_style_scraper/flows/content_generation_flow.py`
   - Changes: Flow that reads attendee data, applies styles, generates content, triggers build
   - Validation: Content flows into existing TypeScript generation pipeline

**Validation Checkpoint:**
- [ ] Content creation crew generates personalized content
- [ ] Generated content matches event brand voice
- [ ] Content integrates with existing attendee data
- [ ] GitHub Pages build triggered after content generation
- [ ] Sub-agents enhance content quality by 30%+

### Phase 5: TypeScript Integration
**Objective:** Integrate scraped styles and generated content with existing static site generator

**Steps:**
1. Extend TypeScript types
   - File(s) affected: `src/types/index.ts`
   - Changes: Add EventStyleConfig interface with optional field in Event
   - Validation: TypeScript compilation succeeds

2. Update data loader
   - File(s) affected: `src/dataLoader.ts`
   - Changes: Load style configs from style-configs/ directory
   - Validation: Style configs load and parse correctly

3. Create CSS generation helper
   - File(s) affected: `src/cssGenerator.ts`
   - Changes: Convert EventStyleConfig to CSS custom properties
   - Validation: Generated CSS is valid and complete

4. Update Handlebars templates
   - File(s) affected: `templates/layouts/base.hbs`
   - Changes: Inject dynamic CSS variables, add Markus AI footer
   - Validation: Pages render with dynamic styles

**Validation Checkpoint:**
- [ ] TypeScript types compile without errors
- [ ] Style configs load successfully
- [ ] CSS generation produces valid stylesheets
- [ ] Pages display with event-specific styling

### Phase 6: Testing and Validation
**Objective:** Comprehensive testing of scraping, content generation, and integration

**Steps:**
1. Create Python unit tests
   - File(s) affected: `python/tests/test_*.py`
   - Changes: Test models, tools, agents, crews, flows
   - Validation: 80%+ code coverage

2. Create content generation tests
   - File(s) affected: `python/tests/test_content_creation.py`
   - Changes: Test ContentCreationCrew, brand voice application, personalization
   - Validation: Content quality metrics pass thresholds

3. Create integration tests
   - File(s) affected: `python/tests/integration/test_end_to_end.py`
   - Changes: Test full scraping → content generation → export → build flow
   - Validation: End-to-end scenarios pass

4. Add TypeScript tests for style loading
   - File(s) affected: `tests/unit/cssGenerator.test.ts`
   - Changes: Test CSS generation from style configs
   - Validation: All new tests pass

5. Create visual regression tests
   - File(s) affected: `tests/visual/`
   - Changes: Screenshot comparison tests
   - Validation: Visual differences < 5% threshold

**Validation Checkpoint:**
- [ ] Python tests achieve 80%+ coverage
- [ ] TypeScript tests maintain 89.93%+ coverage
- [ ] Integration tests pass
- [ ] Visual regression tests pass

### Phase 7: Production Deployment
**Objective:** Deploy enhanced system with style scraping and content creation capabilities

**Steps:**
1. Update GitHub Actions workflow
   - File(s) affected: `.github/workflows/deploy.yml`
   - Changes: Add Python setup, run scraper before build
   - Validation: Workflow executes successfully

2. Scrape Markus AI website
   - File(s) affected: `style-configs/markus-ai-style.json`
   - Changes: One-time scrape of https://dearmarkus.ai/
   - Validation: Markus AI styles extracted correctly

3. Update documentation
   - File(s) affected: `README.md`, `CLAUDE.md`, `docs/`
   - Changes: Document new Python layer, usage instructions
   - Validation: Documentation is complete and accurate

4. Deploy to GitHub Pages
   - File(s) affected: Generated files in `dist/`
   - Changes: Deploy pages with dynamic styling
   - Validation: Live pages show event-specific styles

**Validation Checkpoint:**
- [ ] CI/CD pipeline runs successfully
- [ ] Markus AI attribution appears in footer
- [ ] Live pages match event website styling
- [ ] Documentation is comprehensive

## Dependencies

### Prerequisites
- [x] Plan 001 completed (base static site generator)
- [x] Plan 002 completed (Event Tech Live data integration)
- [x] Python 3.10+ available in environment
- [ ] OpenAI API key configured for crewAI
- [ ] Playwright dependencies installed

### Related Plans
- `plans/001-github-pages-attendee-summary.md` - Base implementation this extends
- `plans/002-event-tech-live-sample-data.md` - Sample data this will style

### External Dependencies
- **crewAI** - Multi-agent orchestration framework
- **Playwright** - Web scraping and browser automation
- **Pydantic** - Data validation and type safety
- **BeautifulSoup4** - HTML parsing fallback
- **Stylelint** - CSS validation

## Risk Assessment

### High Risk Items
1. **Risk:** Web scraping blocked by event websites
   - **Likelihood:** Medium
   - **Impact:** High
   - **Mitigation:** Respect robots.txt, use proper user agent, add rate limiting
   - **Contingency:** Provide manual style configuration option

2. **Risk:** Extracted styles don't match visual appearance
   - **Likelihood:** Medium
   - **Impact:** High
   - **Mitigation:** Use validation sub-agents, visual regression testing
   - **Contingency:** Manual review and adjustment process

### Medium Risk Items
1. **Risk:** Python/TypeScript integration complexity
   - **Likelihood:** Low
   - **Impact:** Medium
   - **Mitigation:** Use JSON as clean interface, comprehensive testing
   - **Contingency:** Keep systems loosely coupled

2. **Risk:** OpenAI API costs for crewAI usage
   - **Likelihood:** Medium
   - **Impact:** Medium
   - **Mitigation:** Cache scraped styles, rate limit requests
   - **Contingency:** Use local LLM alternatives

3. **Risk:** CSS conflicts with existing styles
   - **Likelihood:** Low
   - **Impact:** Medium
   - **Mitigation:** Use CSS custom properties with scoping
   - **Contingency:** Namespace all dynamic styles

## Rollback Plan

If implementation fails or needs to be reversed:

1. Remove Python directory: `rm -rf python/`
2. Remove style configs: `rm -rf style-configs/`
3. Revert TypeScript changes: `git checkout -- src/types/index.ts src/dataLoader.ts`
4. Revert template changes: `git checkout -- templates/`
5. Revert GitHub Actions: `git checkout -- .github/workflows/`
6. Clear any cached artifacts: `rm -rf .cache/`
7. Rebuild and test: `npm run build && npm test`

**Validation after rollback:**
- [ ] Original functionality restored
- [ ] All 105 tests pass
- [ ] Pages generate with original styling
- [ ] No Python dependencies remain

## Testing Strategy

### Unit Tests
- [ ] Test coverage for EventStyleConfig Pydantic models
- [ ] Test coverage for security-hardened WebScraperTool
- [ ] Test coverage for each agent (scraper, style, voice, validation)
- [ ] Test coverage for CSS generation from style configs
- [ ] Test coverage for style config loading in TypeScript

### Integration Tests
- [ ] Test full scraping flow with mock websites
- [ ] Test style config export and JSON validity
- [ ] Test TypeScript loading of generated configs
- [ ] Test page generation with dynamic styles
- [ ] Test GitHub Actions workflow integration

### Manual Testing
1. Scrape 3 different event websites manually
2. Verify extracted styles match visual inspection
3. Generate pages with each style config
4. Compare visual appearance with source websites
5. Test Markus AI footer attribution
6. Verify no regression in existing functionality

### Validation Commands
```bash
# Verify Python environment setup
cd python && python -m pytest tests/ -v

# Test web scraping crew
python -m event_style_scraper scrape --url https://dearmarkus.ai/ --output style-configs/test.json

# Validate generated style configs
ajv validate -s schemas/style-config-schema.json -d style-configs/*.json

# Test CSS generation
npm run test tests/unit/cssGenerator.test.ts

# Test content creation crew
python -m event_style_scraper generate-content --attendee data/attendees/1001.json --style style-configs/test.json

# Test full pipeline integration
python -m event_style_scraper full-pipeline --event-url https://dearmarkus.ai/ --attendee-dir data/attendees/

# Verify GitHub Pages integration
npm run generate && python -m event_style_scraper validate --dir dist/

# Test content quality
python -m event_style_scraper validate --content-quality --dir generated-content/

# Check visual similarity
python -m event_style_scraper compare --source https://example.com --generated dist/attendees/1001/

# Run full test suite
npm test && cd python && python -m pytest
```

## Post-Implementation

### Documentation Updates
- [ ] Update README.md with Python setup instructions
- [ ] Document style scraping usage in CLAUDE.md
- [ ] Create style-customization.md guide
- [ ] Update API documentation for new interfaces
- [ ] Add troubleshooting section for common scraping issues

### Knowledge Capture
- [ ] Document successful scraping patterns
- [ ] List websites that required special handling
- [ ] Record CSS variable naming conventions
- [ ] Document sub-agent effectiveness metrics
- [ ] Create examples of style override configurations

## Appendix

### References
- [crewAI Documentation](https://docs.crewai.com)
- [Playwright Python API](https://playwright.dev/python/)
- [book_wizards Implementation](../book_wizards/CLAUDE.md)
- [PRD-002 Requirements](requirements/PRD-002.md)
- [Exploration Report](analysis/exploration-report-2025-11-06-prd-002.md)

### Alternative Approaches Considered
1. **Approach:** Pure TypeScript implementation without crewAI
   - **Pros:** Single language, simpler deployment
   - **Cons:** No intelligent agent collaboration, manual prompt engineering
   - **Why not chosen:** PRD-002 specifically requires crewAI framework

2. **Approach:** Separate microservice for style scraping
   - **Pros:** Complete separation, independent scaling
   - **Cons:** Complex deployment, inter-service communication overhead
   - **Why not chosen:** Overkill for static site generation use case

3. **Approach:** Runtime style fetching on page load
   - **Pros:** Always up-to-date styles
   - **Cons:** Performance impact, requires API endpoint
   - **Why not chosen:** Violates static site architecture principle

### Sub-Agent Architecture Details

**Style Extraction Crew Sub-Agents**:

*Validation Sub-Agents* (Complex Task Handling):
1. **ColorValidationAgent**: Validates extracted colors are valid CSS values
2. **FontValidationAgent**: Verifies font families exist and are web-safe
3. **ConsistencyAgent**: Checks style coherence across properties
4. **AccessibilityAgent**: Ensures color contrast meets WCAG standards
5. **PerformanceAgent**: Validates CSS doesn't impact page load

*Quality Assurance Sub-Agents*:
1. **ScreenshotAgent**: Captures visual state for comparison
2. **DiffAgent**: Identifies visual differences between source and generated
3. **MetricsAgent**: Calculates similarity scores and quality metrics

*Error Recovery Sub-Agents*:
1. **RetryAgent**: Handles transient scraping failures
2. **FallbackAgent**: Provides default values for missing data
3. **RepairAgent**: Fixes common extraction errors

**Content Creation Crew Sub-Agents**:

*Content Enhancement Sub-Agents*:
1. **MetaphorAgent**: Creates event-themed metaphors for achievements
2. **StorytellingAgent**: Crafts narrative arcs for attendee journeys
3. **PersonalInsightsAgent**: Generates personalized insights from attendee data
4. **CallToActionAgent**: Creates compelling, brand-aligned CTAs
5. **EmotionalToneAgent**: Adjusts content emotional resonance to match brand

*Content Validation Sub-Agents*:
1. **BrandAlignmentAgent**: Verifies content matches brand voice
2. **FactCheckAgent**: Ensures content accuracy against attendee data
3. **ReadabilityAgent**: Optimizes content for target audience reading level
4. **SEOAgent**: Enhances content for search visibility

*GitHub Pages Integration Sub-Agents*:
1. **DataTransformAgent**: Converts generated content to JSON format
2. **BuildTriggerAgent**: Initiates GitHub Actions workflow
3. **DeploymentMonitorAgent**: Tracks deployment status
4. **RollbackAgent**: Handles failed deployments gracefully

### Notes
- Start with Markus AI scraping as it's a known, controlled website
- Consider caching scraped styles to reduce API calls
- Sub-agents should be used liberally for validation and quality checks
- Integration must maintain backward compatibility with existing pages
- Focus on CSS custom properties for maximum flexibility