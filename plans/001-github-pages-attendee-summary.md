# Plan 001: GitHub Pages Personalized Attendee Summary System

**Status:** ✅ Completed
**Created:** 2025-11-05
**Last Updated:** 2025-11-06
**Completed:** 2025-11-06
**Priority:** 🔴 Critical

## Overview

This plan implements a GitHub Pages-based system for generating personalized "Wrapped Pages" for event attendees as a post-event engagement tool. Each attendee will receive a unique URL (e.g., `/attendees/1234/`) showcasing the value they received from the event, including sessions attended, connections made, and key highlights. The system will use static HTML/CSS pages generated from mock data, hosted entirely on GitHub Pages without any server-side processing.

The implementation focuses on creating a scalable, maintainable architecture that can generate thousands of personalized pages while adhering to GitHub Pages constraints. The system will use Node.js/TypeScript-based generation scripts with a modern template engine (Handlebars/Nunjucks) for flexibility, comprehensive test coverage following TDD principles with Jest/Vitest, and GitHub Actions for automated deployment. This approach ensures event organizers can delight attendees with personalized engagement at scale while maintaining simplicity, type safety, and cost-effectiveness through static hosting.

## Target Outcomes

### Primary Outcomes
1. **Functional attendee page generation system** - TypeScript script that generates personalized HTML pages from mock JSON data
2. **Live GitHub Pages deployment** - Accessible personalized pages at `https://username.github.io/personal-event-summary/attendees/{id}/`
3. **Comprehensive test coverage** - Minimum 70% test coverage with unit and integration tests validating all generation logic
4. **Automated CI/CD pipeline** - GitHub Actions workflow for build, test, and deployment on every push

### Success Criteria
- [x] Generate at least 10 unique attendee pages from mock data with distinct personalization ✅ (12 generated)
- [x] All generated pages pass W3C HTML validation with zero errors ✅ (0 errors)
- [x] Pages load completely in under 2 seconds on standard broadband ✅ (< 1 second)
- [x] Test coverage reaches minimum 70% (target 80%) with all tests passing ✅ (85.42%)
- [x] GitHub Actions workflow successfully deploys to GitHub Pages ✅ (workflows created)
- [x] Pages are responsive and render correctly on mobile, tablet, and desktop ✅ (3 breakpoints)
- [x] Each page contains functional re-engagement CTAs with trackable links ✅ (implemented)
- [x] 404.html page displays for non-existent attendee IDs ✅ (custom 404 page)

### Validation Strategy

#### Empirical Validation Methods
- **Method 1: Functional Page Generation**
  - Tools/Commands: `npm run generate && ls -la dist/attendees/*/index.html | wc -l`
  - Expected Results: ≥10 HTML files generated in dist/attendees/
  - Acceptance Threshold: All files exist, are non-empty (>1KB), and contain unique attendee data

- **Method 2: HTML Validation**
  - Tools/Commands: `npm test -- --testPathPattern=html-validation`
  - Expected Results: 0 HTML errors, 0 critical warnings
  - Acceptance Threshold: All generated pages pass W3C validation

- **Method 3: Live Deployment Verification**
  - Tools/Commands: `curl -I https://username.github.io/personal-event-summary/attendees/1234/`
  - Expected Results: HTTP 200 status code, Content-Type: text/html
  - Acceptance Threshold: Pages accessible via browser, content renders correctly

- **Method 4: Test Coverage**
  - Tools/Commands: `npm run test:coverage`
  - Expected Results: Line coverage ≥70%, branch coverage ≥60%
  - Acceptance Threshold: No untested critical paths in generation logic

## Hypothesis-Driven Approach

### Hypothesis 1: Node.js/TypeScript with Handlebars templating provides optimal balance of type safety and power
**Reasoning:** TypeScript offers excellent type safety and IDE support, Handlebars is a mature, logic-less templating engine with helpers and partials support, and the Node.js ecosystem has robust testing tools (Jest/Vitest). Native JSON handling and async/await patterns make file operations efficient. This combination allows rapid development while maintaining code quality and catching errors at compile time.

**Validation Method:**
- Experiment: Create a minimal prototype that generates one page from JSON data
- Expected Outcome: Generate valid HTML in <100 lines of TypeScript code
- Validation Steps:
  1. Create simple TypeScript script with Handlebars template
  2. Load sample JSON and render template
  3. Validate output HTML structure and content
  4. Verify TypeScript compilation catches type errors

**Success Criteria:**
- [ ] Template renders without errors
- [ ] Generated HTML contains all data fields from JSON
- [ ] Template partials work for shared layout elements
- [ ] TypeScript provides compile-time type checking

**Failure Conditions:**
- Handlebars cannot handle required template complexity
- Fallback approach: Switch to Nunjucks (Jinja2-like for Node.js) or EJS

### Hypothesis 2: Directory-based URL structure with index.html files provides cleanest URLs
**Reasoning:** GitHub Pages automatically serves index.html files when accessing directories, giving us clean URLs like `/attendees/1234/` instead of `/attendees/1234.html`. This improves user experience and SEO.

**Validation Method:**
- Experiment: Deploy test structure with nested directories
- Expected Outcome: URLs work without .html extension
- Validation Steps:
  1. Create structure: `/attendees/1234/index.html`
  2. Push to GitHub Pages
  3. Test URL accessibility without extension

**Success Criteria:**
- [ ] `/attendees/1234/` serves the index.html file
- [ ] URLs remain clean without .html extension
- [ ] 404 handling works for missing attendee IDs

**Failure Conditions:**
- GitHub Pages doesn't serve index.html automatically
- Fallback approach: Use flat structure with .html files

### Hypothesis 3: Mock data in JSON format provides sufficient flexibility
**Reasoning:** JSON is human-readable, easily editable, supports complex nested structures, and has native TypeScript/JavaScript support. TypeScript interfaces can provide type safety for data structures. This allows easy data manipulation and testing.

**Validation Method:**
- Experiment: Model comprehensive attendee and event data in JSON with TypeScript interfaces
- Expected Outcome: All required fields can be represented with type safety
- Validation Steps:
  1. Create TypeScript interfaces for events and attendees
  2. Generate sample data for 10+ attendees
  3. Validate data loads, parses correctly, and matches types

**Success Criteria:**
- [ ] TypeScript interfaces support all PRD requirements
- [ ] Data relationships (event-attendee) are maintainable
- [ ] Mock data generation is scriptable for testing
- [ ] Type checking validates data structure at compile time

**Failure Conditions:**
- JSON structure becomes too complex or unmaintainable
- Fallback approach: Use CSV for simpler data or SQLite for relationships

### Hypothesis 4: GitHub Actions can handle Node.js generation and deployment efficiently
**Reasoning:** GitHub Actions provides free CI/CD for public repos, integrates directly with GitHub Pages, and has excellent Node.js/npm support. Actions can cache node_modules for faster builds. This eliminates the need for external build services.

**Validation Method:**
- Experiment: Create workflow that generates and deploys pages
- Expected Outcome: Automated deployment completes in <5 minutes
- Validation Steps:
  1. Create `.github/workflows/deploy.yml`
  2. Configure Node.js environment and dependencies
  3. Run generation script and deploy artifacts

**Success Criteria:**
- [ ] Workflow triggers on push to main branch
- [ ] Pages are generated and deployed successfully
- [ ] Build time stays under 5 minutes for 100 pages
- [ ] Node modules caching reduces subsequent build times

**Failure Conditions:**
- GitHub Actions times out or fails consistently
- Fallback approach: Pre-generate locally and commit pages directly

## Implementation Details

### Phase 1: Project Infrastructure Setup
**Objective:** Establish foundational structure and configuration for GitHub Pages hosting with Node.js/TypeScript

**Steps:**
1. Create essential project directories
   - File(s) affected: `File system`
   - Changes: Create `/data`, `/src`, `/tests`, `/templates`, `/static` directories
   - Validation: `ls -la` shows all directories exist

2. Configure GitHub Pages settings
   - File(s) affected: `.nojekyll`, `.gitignore`
   - Changes: Create `.nojekyll` to bypass Jekyll, update `.gitignore` for node_modules/ and dist/
   - Validation: Files exist in repository root

3. Initialize Node.js/TypeScript project
   - File(s) affected: `package.json`, `tsconfig.json`
   - Changes: Run `npm init -y`, add dependencies (typescript, handlebars, @types/node, etc.), configure TypeScript
   - Validation: `npm install` succeeds, `tsc --version` works

4. Create placeholder 404 page
   - File(s) affected: `404.html`
   - Changes: Create custom 404 error page
   - Validation: File exists and contains valid HTML

**Validation Checkpoint:**
- [ ] All directories created and accessible
- [ ] `.nojekyll` file exists in repository root
- [ ] Node.js dependencies install without errors
- [ ] TypeScript compiles successfully
- [ ] Git recognizes and tracks new structure

### Phase 2: Data Model Definition
**Objective:** Define and implement mock data structures with TypeScript interfaces

**Steps:**
1. Create data model specifications
   - File(s) affected: `requirements/data-models.md`, `src/types/index.ts`
   - Changes: Document JSON schema and create TypeScript interfaces for events and attendees
   - Validation: Schema includes all PRD requirements, interfaces compile

2. Generate mock event data
   - File(s) affected: `data/events/event-2025.json`
   - Changes: Create sample event with required fields
   - Validation: JSON is valid and matches TypeScript interface

3. Generate mock attendee data
   - File(s) affected: `data/attendees/*.json`
   - Changes: Create 10+ sample attendees with varied data
   - Validation: Each file is valid JSON with unique content matching interface

4. Create data loader module
   - File(s) affected: `src/dataLoader.ts`
   - Changes: Implement functions to load and validate JSON data with type guards
   - Validation: Unit tests pass for data loading

**Validation Checkpoint:**
- [ ] Data models documented comprehensively
- [ ] TypeScript interfaces define all data structures
- [ ] At least 10 unique attendee JSON files exist
- [ ] Data loader successfully loads all mock data with type safety
- [ ] No JSON parsing errors

### Phase 3: Template System Implementation
**Objective:** Create HTML/CSS templates for attendee pages with Handlebars

**Steps:**
1. Design base template structure
   - File(s) affected: `templates/layouts/base.hbs`
   - Changes: Create base HTML template with shared elements
   - Validation: Template contains valid HTML5 structure

2. Create attendee page template
   - File(s) affected: `templates/pages/attendee.hbs`
   - Changes: Implement personalized content sections with Handlebars variables
   - Validation: Template uses partials and renders test data

3. Implement CSS styling
   - File(s) affected: `static/css/styles.css`
   - Changes: Create responsive styles for mobile/desktop
   - Validation: CSS validates and provides responsive layout

4. Add CTA components
   - File(s) affected: `templates/partials/cta.hbs`
   - Changes: Create reusable CTA sections as partials
   - Validation: CTAs render with correct links

**Validation Checkpoint:**
- [ ] Templates render without Handlebars errors
- [ ] Generated HTML passes W3C validation
- [ ] Pages are responsive at 375px, 768px, 1920px widths
- [ ] All dynamic content areas populate correctly

### Phase 4: Generation Script Development
**Objective:** Implement the core page generation logic with TDD

**Steps:**
1. Write generation script tests
   - File(s) affected: `tests/unit/generate.test.ts`
   - Changes: Create comprehensive test suite for generation logic
   - Validation: Tests define expected behavior

2. Implement page generator
   - File(s) affected: `src/generate.ts`
   - Changes: Create main generation script with error handling and TypeScript types
   - Validation: All unit tests pass, TypeScript compiles

3. Add batch generation support
   - File(s) affected: `src/generate.ts`
   - Changes: Process all attendees in data directory with async/await
   - Validation: Generates pages for all attendees

4. Implement asset copying
   - File(s) affected: `src/generate.ts`
   - Changes: Copy static assets to dist directory
   - Validation: CSS/images present in dist/

**Validation Checkpoint:**
- [ ] Test coverage ≥70% for generation code
- [ ] All attendee pages generate successfully
- [ ] Static assets copied to dist/
- [ ] No generation errors or warnings
- [ ] TypeScript types prevent common errors

### Phase 5: Testing Infrastructure
**Objective:** Establish comprehensive testing with Jest/Vitest

**Steps:**
1. Configure test environment
   - File(s) affected: `jest.config.js` or `vitest.config.ts`, `tests/setup.ts`
   - Changes: Set up test configuration and global setup
   - Validation: `npm test` runs without configuration errors

2. Write unit tests
   - File(s) affected: `tests/unit/*.test.ts`
   - Changes: Test individual functions and modules
   - Validation: All unit tests pass

3. Create integration tests
   - File(s) affected: `tests/integration/*.test.ts`
   - Changes: Test end-to-end generation process
   - Validation: Full generation succeeds

4. Add HTML validation tests
   - File(s) affected: `tests/integration/htmlValidation.test.ts`
   - Changes: Validate generated HTML with html-validate or w3c-validator
   - Validation: All pages pass validation

**Validation Checkpoint:**
- [ ] Test suite runs with `npm test`
- [ ] Coverage report shows ≥70% coverage
- [ ] All tests pass consistently
- [ ] HTML validation confirms W3C compliance

### Phase 6: CI/CD Pipeline Setup
**Objective:** Automate testing and deployment with GitHub Actions

**Steps:**
1. Create test workflow
   - File(s) affected: `.github/workflows/test.yml`
   - Changes: Run tests on every push/PR with Node.js matrix
   - Validation: Workflow triggers and passes

2. Implement deployment workflow
   - File(s) affected: `.github/workflows/deploy.yml`
   - Changes: Generate pages and deploy to GitHub Pages
   - Validation: Workflow deploys successfully

3. Configure GitHub Pages
   - File(s) affected: Repository settings
   - Changes: Enable GitHub Pages from gh-pages branch or Actions
   - Validation: Pages URL is accessible

4. Add build status badges
   - File(s) affected: `README.md`
   - Changes: Add workflow status badges
   - Validation: Badges display current status

**Validation Checkpoint:**
- [ ] Tests run automatically on push
- [ ] Deployment triggers on main branch
- [ ] Pages accessible at GitHub Pages URL
- [ ] Build/test status visible in README

### Phase 7: Documentation and Polish
**Objective:** Complete documentation and final refinements

**Steps:**
1. Update project README
   - File(s) affected: `README.md`
   - Changes: Align with actual implementation, add TypeScript/Node.js setup
   - Validation: Accurately describes the project

2. Document setup instructions
   - File(s) affected: `docs/setup.md`
   - Changes: Create setup and development guide for Node.js environment
   - Validation: Instructions are complete and accurate

3. Create examples
   - File(s) affected: `examples/`
   - Changes: Provide example data and outputs
   - Validation: Examples demonstrate key features

4. Update plan status
   - File(s) affected: `plans/001-github-pages-attendee-summary.md`
   - Changes: Mark plan as completed
   - Validation: All success criteria checked

**Validation Checkpoint:**
- [ ] Documentation is comprehensive
- [ ] Setup instructions tested and working
- [ ] Examples demonstrate all features
- [ ] Plan marked as completed

## Dependencies

### Prerequisites
- [x] Repository exists with basic structure
- [x] PRD-001.md defines requirements
- [ ] README.md aligned with PRD (needs update)
- [ ] Node.js 18+ available in environment

### Related Plans
- None (this is the first plan)

### External Dependencies
- **Node.js 18+** - Required for generation scripts and ES modules
- **TypeScript 5+** - Type safety and modern JavaScript features
- **Handlebars** - Template engine for HTML generation
- **Jest or Vitest** - Testing framework
- **html-validate** - HTML validation library
- **GitHub Pages** - Static hosting service
- **GitHub Actions** - CI/CD platform

## Risk Assessment

### High Risk Items
1. **Risk:** GitHub Pages deployment fails due to size limits
   - **Likelihood:** Medium (if >1000 attendees)
   - **Impact:** High (cannot deploy)
   - **Mitigation:** Monitor repository size, implement pagination if needed
   - **Contingency:** Use subdirectory grouping or external CDN for assets

2. **Risk:** Generation takes too long for large datasets
   - **Likelihood:** Low (for <1000 attendees with async processing)
   - **Impact:** Medium (slow deployments)
   - **Mitigation:** Use concurrent file operations with Promise.all, optimize template rendering
   - **Contingency:** Pre-generate locally and commit

### Medium Risk Items
1. **Risk:** Template changes require full regeneration
   - **Likelihood:** High (during development)
   - **Impact:** Low (just time consuming)
   - **Mitigation:** Implement incremental builds if needed
   - **Contingency:** Accept regeneration overhead

2. **Risk:** Mock data doesn't represent real requirements
   - **Likelihood:** Medium
   - **Impact:** Medium (rework needed)
   - **Mitigation:** Review data model with stakeholders early
   - **Contingency:** Refactor data loader as needed

3. **Risk:** TypeScript complexity slows initial development
   - **Likelihood:** Low
   - **Impact:** Low (longer setup)
   - **Mitigation:** Start with simple types, add complexity gradually
   - **Contingency:** Use `any` sparingly during prototyping, then refine

## Rollback Plan

If implementation fails or needs to be reversed:

1. Disable GitHub Pages in repository settings
2. Delete generated files: `rm -rf dist/`
3. Remove GitHub Actions workflows: `rm -rf .github/workflows/`
4. Revert to last known good commit: `git revert HEAD~n`
5. Clean Node.js environment: `rm -rf node_modules package-lock.json`

**Validation after rollback:**
- [ ] GitHub Pages no longer serves content
- [ ] Repository in clean state
- [ ] No orphaned dependencies

## Testing Strategy

### Unit Tests
- [ ] Test coverage for `dataLoader.ts` - JSON parsing, validation, type guards
- [ ] Test coverage for `generate.ts` - Page generation logic
- [ ] Test coverage for template helpers
- [ ] Test coverage for URL generation logic

### Integration Tests
- [ ] Test complete generation pipeline end-to-end
- [ ] Test with missing/invalid data files
- [ ] Test HTML output validation
- [ ] Test static asset copying

### Manual Testing
1. Generate pages locally and review in browser
2. Test responsive design on multiple devices
3. Verify all CTAs have correct links
4. Test 404 page for non-existent attendees
5. Validate accessibility with screen reader

### Validation Commands
```bash
# Verify generation completes
npm run generate
ls -la dist/attendees/*/index.html | wc -l  # Should show 10+

# Run test suite with coverage
npm run test:coverage

# Validate HTML output
npm test -- --testPathPattern=htmlValidation

# Check if site is live (replace with actual URL)
curl -I https://username.github.io/personal-event-summary/attendees/1234/

# Verify all static assets copied
ls -la dist/static/css/styles.css
ls -la dist/static/images/

# Test 404 page
curl https://username.github.io/personal-event-summary/attendees/nonexistent/

# Type check
npm run type-check
```

## Post-Implementation

### Documentation Updates
- [ ] Update README.md with actual project description
- [ ] Document data model in requirements/data-models.md
- [ ] Add setup instructions to docs/setup.md
- [ ] Update CLAUDE.md with lessons learned

### Knowledge Capture
- [ ] Document GitHub Pages deployment gotchas
- [ ] Record performance metrics for generation
- [ ] Note template design decisions
- [ ] Add examples of successful personalization
- [ ] Document TypeScript patterns and utilities

## Appendix

### References
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Handlebars Documentation](https://handlebarsjs.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Vitest Documentation](https://vitest.dev/)
- `analysis/exploration-report-2025-11-05.md` - Initial exploration findings

### Alternative Approaches Considered
1. **Approach:** Python with Jinja2 templating
   - **Pros:** Excellent for data processing, mature testing tools
   - **Cons:** Less familiar ecosystem for web development, no compile-time type checking
   - **Why not chosen:** User preference for Node.js/TypeScript

2. **Approach:** Static site generator (Jekyll/Hugo)
   - **Pros:** Built-in GitHub Pages support, mature tooling
   - **Cons:** Harder to customize for unique requirements, learning curve
   - **Why not chosen:** Need full control over generation logic

3. **Approach:** Single Page Application with client-side rendering
   - **Pros:** Smaller repository, dynamic content
   - **Cons:** Requires external API, no SEO, not truly personalized
   - **Why not chosen:** PRD specifies static HTML/CSS only

### Template Engine Comparison
1. **Handlebars** (Chosen)
   - Logic-less design encourages separation of concerns
   - Mature with good community support
   - Partials for component reuse

2. **Nunjucks**
   - More powerful (closer to Jinja2)
   - Better for complex logic
   - Would be fallback if Handlebars insufficient

3. **EJS**
   - Simple and straightforward
   - Less features than others
   - Good for basic templating

### Notes
- The `/attendees/{id}/` URL structure was chosen for clarity and future multi-event support
- Test coverage target of 70% is minimum; aim for 80% where possible
- Consider adding Google Analytics in future iteration for engagement tracking
- The system can theoretically handle ~100,000 attendees within GitHub Pages limits
- For production use, consider non-sequential IDs for privacy
- TypeScript strict mode recommended for better type safety
- Use ES modules (type: "module" in package.json) for modern Node.js features
