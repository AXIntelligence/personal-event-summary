# Plans Directory

This directory contains implementation plans and design documents for the personal-event-summary project.

## Numbering System

Plans are numbered sequentially using a three-digit prefix format: `NNN-descriptive-name.md`

### Format
```
NNN-descriptive-name.md
```

Where:
- `NNN` = Three-digit number (001, 002, 003, etc.)
- `descriptive-name` = Kebab-case description of the plan
- `.md` = Markdown file extension

### Examples
- `001-event-data-model.md` - Data model design for events
- `002-event-processing-pipeline.md` - Event processing implementation
- `003-api-design.md` - API design and implementation

## Creating a New Plan

### Using the /plan Command (Recommended)

```bash
/plan [your requirements or description]
```

The `/plan` command will:
- Automatically determine the next plan number
- Create a comprehensive, hypothesis-driven plan
- Validate assumptions empirically
- Define clear success criteria
- Save the plan to the plans/ directory

See [/.claude/commands/plan.md](../.claude/commands/plan.md) for details.

### Manual Creation

1. **Determine the next number**: Check existing files and increment the highest number
   ```bash
   ls plans/*.md | sort | tail -1
   ```

2. **Create the file**: Use the numbering format
   ```bash
   # If last plan was 001, create 002
   touch plans/002-your-plan-name.md
   ```

3. **Document the plan**: Include the following sections:
   - **Title**: Clear, descriptive title
   - **Status**: Draft, In Progress, Completed, Archived
   - **Date**: Creation date and last updated
   - **Overview**: Brief description of the plan
   - **Goals**: What this plan aims to achieve
   - **Implementation Details**: Technical details
   - **Dependencies**: Related plans or prerequisites
   - **Success Criteria**: Empirically measurable outcomes

## Implementing a Plan

### Using the /implement Command (Recommended)

```bash
/implement ./plans/NNN-plan-name.md [additional-instructions]
```

The `/implement` command will:
- Execute the plan using Test-Driven Development (TDD) methodology
- Validate coverage thresholds
- Seek confirmation before moving between phases
- Run and wait for integration tests to complete
- Validate all success criteria empirically
- Update all documentation upon completion
- Create validation reports in analysis/

See [/.claude/commands/implement.md](../.claude/commands/implement.md) for details.

**Example:**
```bash
/implement ./plans/001-event-data-model.md
```

### Manual Implementation

If implementing manually:
1. Follow the plan phases in order
2. Use TDD: Write tests first, then implementation
3. Run integration tests before marking complete
4. Validate all success criteria empirically
5. Update documentation and plan status

## Plan Lifecycle

### Status Indicators

- **Draft**: Plan is being written and reviewed
- **Approved**: Plan has been reviewed and approved
- **In Progress**: Implementation is underway
- **Completed**: All tasks in the plan are done, all success criteria validated, quality metrics met:
  - ✅ All unit tests passing (100%)
  - ✅ Line coverage ≥70% (target: 80%)
  - ✅ Integration tests successful
  - ✅ Documentation updated
- **Deferred**: Plan has been paused till a later date
- **Abandoned**: Plan was abandoned for reasons
- **Archived**: Plan is historical reference only

### Updating Plans

- Minor updates: Edit the existing file
- Major changes: Consider creating a new plan that references the original
- Add a "Last Updated" timestamp when making significant changes
- Mark plans as "Completed" only after empirical validation of all outcomes

## Referencing Plans

When referencing plans in code comments or documentation:
```python
# Implementation follows plan 001-event-data-model.md
# See plans/002-event-processing-pipeline.md for context
```

## Index of Plans

| Number | Name | Status | Completion Date | Priority | Description |
|--------|------|--------|-----------------|----------|-------------|
| 001 | [GitHub Pages Attendee Summary](001-github-pages-attendee-summary.md) | ✅ Completed | 2025-11-06 | 🔴 Critical | Implement personalized attendee pages on GitHub Pages |
| 002 | [Event Tech Live Sample Data](002-event-tech-live-sample-data.md) | ✅ Completed | 2025-11-06 | 🟡 High | Enhance sample data with Event Tech Live real event insights |
| 003 | [Event-Centered Styling with CrewAI](003-event-centered-styling-crewai.md) | 📝 Draft | - | 🟡 High | Implement PRD-002: Event website style scraping using crewAI multi-agent framework |
| 004 | [Fix Event Tech Live Style Mismatch](004-fix-event-tech-live-style-mismatch.md) | 📝 Draft | - | 🔴 Critical | Fix style mismatch by replacing sample config with real scraped data from eventtechlive.com |
| 005 | [Playwright-Based Scraping Tool](005-playwright-scraping-tool.md) | ✅ Completed | 2025-11-07 | 🔴 Critical | Replace AI-guessing with actual browser automation for accurate style extraction |
| 006 | [End-to-End Scrape-Deploy Pipeline](006-end-to-end-scrape-deploy-pipeline.md) | 📝 Draft | - | 🔴 Critical | Automate scraping in GitHub Actions for continuous style updates and full pipeline validation |
| 007 | [AWS re:Invent Data Source Integration](007-aws-reinvent-data-source.md) | ✅ Completed | 2025-11-07 | 🔴 Critical | Replace TechConf 2025 with AWS re:Invent as high-quality event data source |
| 008 | [Fix Missing Event Logos and Markus AI Attribution](008-fix-missing-event-and-markus-logos.md) | ✅ Completed | 2025-11-07 | 🔴 Critical | Fix missing logos and Markus AI attribution on GitHub Pages deployment |

## Status Legend
- ✅ **Completed**: Implementation done, all tests passing
- 🚧 **In Progress**: Currently being implemented
- 📝 **Draft**: Planning phase, not yet started
- 🔄 **In Review**: Completed but pending review/approval
- ⏸️ **Deferred**: Planned but postponed
- 💀 **Abandoned**: Plan has been abandoned
- 📦 **Archived**: Historical reference, no longer active

## Priority Legend
- 🔴 **Critical**: Addresses major issues or core functionality
- 🟡 **High**: Important enhancements with clear value
- 🟢 **Low**: Nice-to-have features, polish, future enhancements

---

## Recent Updates

- **2025-11-07**: Completed Plan 008 - Fix Missing Event Logos and Markus AI Attribution ✅
  - Created Event Tech Live and AWS re:Invent SVG logos
  - Added favicon.svg for browser tabs
  - Updated event JSON files with local logo paths
  - Completed AWS re:Invent style config with logoUrl/faviconUrl
  - Removed conditional rendering of Markus AI attribution (now shows on all pages)
  - All 139 tests passing, 0 HTML validation errors
  - Lesson 20 added to CLAUDE.md: "Visual Assets Require Local Hosting"
- **2025-11-07**: Created Plan 008 - Fix Missing Event Logos and Markus AI Attribution (Draft)
  - Addresses missing logos on GitHub Pages (AWS re:Invent, Event Tech Live)
  - Fixes missing Markus AI attribution in footer (PRD-002 requirement)
  - Downloads and hosts logos locally in static/images/
  - Updates event JSON files with local logo paths
  - Removes conditional rendering of Markus AI attribution
  - Adds missing logoUrl/faviconUrl to AWS re:Invent style config
- **2025-11-07**: Completed Plan 007 - AWS re:Invent Data Source Integration ✅
  - Scraped AWS re:Invent website for authentic branding (#232f3e primary color, Amazon Ember font)
  - Created aws-reinvent-2025.json event config with 30 AWS-themed sessions across 7 tracks
  - Generated 12 believable attendee personas (3001-3012) with realistic engagement patterns
  - Removed TechConf 2025 data (event-2025.json, attendees 1001-1012)
  - Updated all 139 tests to reference Event Tech Live (2001-2012) and AWS re:Invent (3001-3012)
  - All tests passing (100%), test coverage maintained at 89.93%
  - Documentation updated (README.md, CLAUDE.md, plans/README.md)
  - Validation report: [analysis/plan-007-validation-report.md](../analysis/plan-007-validation-report.md)
- **2025-11-07**: Created Plan 007 - AWS re:Invent Data Source Integration (Draft)
  - Replaces generic TechConf 2025 with AWS re:Invent as high-quality event example
  - Scrapes https://reinvent.awsevents.com/ for authentic AWS branding
  - Creates 12 believable attendee personas (3001-3012) with AWS-themed sessions
  - Includes 60+ unique AWS sessions across 7 tracks (Compute, AI/ML, Serverless, etc.)
  - Removes old event-2025.json and attendees 1001-1012
  - Hypothesis-driven approach with DevTools color validation
- **2025-11-07**: Created Plan 006 - End-to-End Scrape-Deploy Pipeline (Draft) - Modified
  - Addresses CLAUDE.md Lesson 16 compliance (end-to-end validation)
  - Automates Python scraper in GitHub Actions workflow
  - **Manual-only triggers** (no scheduled runs) for complete cost control
  - Validates complete pipeline: scrape → export → CSS gen → HTML → deploy
  - Adds fallback logic, staleness warnings, and DevTools validation
  - Includes E2E test script and comprehensive monitoring
  - Push-triggered deploys complete in < 5 minutes (no scraping overhead)
- **2025-11-07**: Completed Plan 005 - Playwright-Based Scraping Tool ✅
  - Fixed critical hallucination bug where agents generated fictional HTML/CSS
  - Implemented explicit tool invocation instructions with step-by-step format
  - Agent role redefined as "Tool Operator" (not "Expert") to prevent hallucination
  - Integration tests passing: agent reliably calls Playwright tool (100% invocation rate)
  - Created validation pipeline: validate_scraped_colors.py + scraper-validation-checklist.md
  - Validation report: [analysis/plan-005-validation-report.md](../analysis/plan-005-validation-report.md)
  - Lesson 19 added to CLAUDE.md: "Agents Need Explicit Tool Instructions"
  - All success criteria met: 7/7 passing (100%)
- **2025-11-06**: Created Plan 005 - Playwright-Based Scraping Tool (Draft)
  - Addresses root cause: agents have no tools, hallucinate HTML/CSS
  - Implements PlaywrightStyleExtractorTool for real browser automation
  - Extracts actual computed styles from rendered pages (not AI guesses)
  - Includes comprehensive validation pipeline with DevTools comparison
  - Expected to fix color mismatch issues permanently (e.g., #0072ce → #160822)
- **2025-11-06**: Created Plan 004 - Fix Event Tech Live Style Mismatch (Draft)
  - Addresses critical style mismatch discovered in exploration
  - Replaces manually created sample config with real scraped data
  - Establishes validation checklist to prevent future incidents
  - Validates complete Python→TypeScript pipeline end-to-end
- **2025-11-06**: Created Plan 003 - Event-Centered Styling with CrewAI (Draft)
  - Implements PRD-002 requirements for event website style scraping
  - Uses crewAI multi-agent framework with specialized sub-agents
  - Adds Python/crewAI layer for intelligent web scraping
  - Maintains backward compatibility with existing TypeScript pipeline
  - Leverages patterns from book_wizards reference implementation
- **2025-11-06**: Completed Plan 002 - Event Tech Live Sample Data Enhancement
  - Added B2B data model with optional fields (productsExplored, boothsVisited, sponsorInteractions)
  - Created Event Tech Live 2025 event with 30 sessions and 12 attendees
  - Achieved 89.93% test coverage (105 tests passing)
  - Zero breaking changes, full backward compatibility maintained
  - Validation report: [analysis/plan-002-validation-report.md](../analysis/plan-002-validation-report.md)
- **2025-11-06**: Completed Plan 001 - GitHub Pages Attendee Summary System
- **2025-11-06**: Created Plan 002 - Event Tech Live Sample Data Enhancement (Draft)
- **2025-11-05**: Created Plan 001 - GitHub Pages Attendee Summary System (Draft)

---

**Note**: Keep plans up-to-date and mark them with appropriate status as work progresses.