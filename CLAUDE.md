# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal Event Summary is a **static site generator** for creating personalized event summary pages for attendees. Built with **Node.js/TypeScript** and **Handlebars templates**, it generates beautiful, responsive HTML pages showcasing each attendee's conference experience.

**Current Status**: ✅ **Production Ready** - v1.0.0 completed and deployed

### Key Features

- Personalized attendee summary pages with session and connection tracking
- Responsive design (mobile, tablet, desktop)
- W3C valid HTML5 with 85%+ test coverage
- GitHub Pages deployment via GitHub Actions
- < 500ms generation time for 12+ pages

## Development Workflow

### Planning & Design

```bash
# Create a new plan for a feature or task
/plan [description of what you want to build]

# Explore the codebase to understand current state
/explore

# Focus exploration on specific areas
/explore templates and page generation
```

### Implementation

```bash
# Implement a plan using TDD methodology
/implement ./plans/001-feature-name.md

# Run tests
npm test                    # Run all tests
npm run test:coverage       # With coverage report
npm run type-check          # TypeScript type checking
```

### Common Commands

```bash
# Build TypeScript
npm run build

# Generate static site
npm run generate

# Run development build
npx tsc --watch

# Serve locally
http-server dist -p 8080
```

## Architecture Summary

### System Overview

**Static Site Generator** using:
- **Data Layer**: JSON files with TypeScript type guards
- **Template Layer**: Handlebars templates with partials
- **Generation Layer**: Batch page generation with async/await
- **Deployment**: GitHub Actions → GitHub Pages

**Core Flow**:
```
JSON Data → TypeScript Types → Handlebars Templates → HTML Pages → GitHub Pages
```

### File Structure

```
personal-event-summary/
├── data/                      # Source data (JSON)
│   ├── events/
│   │   └── event-2025.json   # Event configuration
│   └── attendees/
│       ├── 1001.json         # Individual attendee data
│       └── ... (12 total)
├── src/                       # TypeScript source
│   ├── types/
│   │   └── index.ts          # Type definitions + type guards
│   ├── dataLoader.ts         # Data loading with validation
│   └── generate.ts           # Page generation engine
├── templates/                 # Handlebars templates
│   ├── layouts/
│   │   └── base.hbs          # Base HTML layout
│   ├── pages/
│   │   └── attendee.hbs      # Attendee page template
│   └── partials/
│       └── cta.hbs           # CTA component
├── static/                    # Static assets
│   ├── css/
│   │   └── styles.css        # 14KB responsive CSS
│   └── images/
├── tests/                     # Test suite (87 tests)
│   ├── unit/                 # 52 unit tests
│   ├── integration/          # 21 integration tests
│   └── validation/           # 14 HTML validation tests
├── dist/                      # Generated output (gitignored)
│   ├── attendees/
│   │   ├── 1001/
│   │   │   └── index.html    # Clean URLs
│   │   └── ...
│   └── static/
├── docs/                      # Documentation
│   ├── setup.md              # Setup guide
│   ├── examples.md           # Usage examples
│   └── github-pages-setup.md # Deployment guide
├── .github/workflows/         # CI/CD
│   ├── test.yml              # Automated testing
│   └── deploy.yml            # GitHub Pages deployment
└── 404.html                   # Custom 404 page
```

### Key Components

**dataLoader.ts**: Loads and validates JSON data
- Functions: `loadEvent()`, `loadAttendee()`, `loadAllAttendees()`
- Runtime type validation with type guards
- Error handling for missing/invalid data

**generate.ts**: Generates HTML pages
- Functions: `setupHandlebars()`, `generateAttendeePage()`, `generateAllAttendeePages()`, `copyStaticAssets()`
- Handlebars helpers: `formatDate`, `substring`, `currentYear`
- Parallel generation with `Promise.all()`

**types/index.ts**: TypeScript interfaces and type guards
- Interfaces: `Event`, `Attendee`, `Session`, `Connection`, `CallToAction`
- Type guards: `isEvent()`, `isAttendee()`, `isSession()`, etc.

## Critical Lessons Learned

### 1. TDD Pays Dividends

**Learning**: Strict TDD from the start led to 85% coverage and caught bugs early.

**Best Practices**:
- Write tests BEFORE implementation (RED phase)
- Keep tests focused and atomic
- Use descriptive test names that document behavior
- Integration tests caught issues unit tests missed

**Example**:
```typescript
// ✅ Good: Test written first, documents expected behavior
it('should throw error for non-existent attendee', async () => {
  await expect(loadAttendee('99999')).rejects.toThrow();
});

// Then implement to pass the test
```

### 2. Type Guards Are Essential

**Learning**: Runtime type guards prevented silent failures with malformed JSON data.

**Implementation**:
```typescript
export function isAttendee(obj: unknown): obj is Attendee {
  if (typeof obj !== 'object' || obj === null) return false;
  const a = obj as Attendee;
  return (
    typeof a.id === 'string' &&
    typeof a.firstName === 'string' &&
    Array.isArray(a.sessions) &&
    // ... more validation
  );
}
```

**Why It Matters**: Catches data errors at load time, not generation time.

### 3. Parallel Generation for Performance

**Learning**: Using `Promise.all()` for parallel generation was 10x faster than sequential.

**Before** (sequential): ~2000ms for 12 pages
**After** (parallel): ~500ms for 12 pages

**Implementation**:
```typescript
const generationPromises = attendees.map(async (attendee) => {
  const html = render(attendee, event);
  await writeFile(outputPath, html);
  return outputPath;
});

return await Promise.all(generationPromises);
```

### 4. HTML Entity Encoding Matters

**Learning**: Apostrophes in names (e.g., "O'Brien") get HTML-encoded as `&#x27;`.

**Impact**: Tests initially failed expecting literal apostrophes.

**Solution**: Use regex patterns in tests to handle both encoded and literal forms:
```typescript
expect(html).toMatch(/Michael O[&#x27;']+Brien/);
```

### 5. Directory-Based Clean URLs

**Learning**: GitHub Pages serves `index.html` from directories for clean URLs.

**Structure**:
```
dist/attendees/1001/index.html
```

**Result**:
- ✅ `/attendees/1001/` (clean)
- ✅ `/attendees/1001` (redirects)
- ✅ `/attendees/1001/index.html` (direct)

**Requirement**: Must include `.nojekyll` to bypass Jekyll processing.

### 6. Handlebars Compilation Optimization

**Learning**: Compiling templates once and reusing saved 200ms on generation.

**Before**: Compile template for each attendee
**After**: Compile once, render multiple times

```typescript
// ✅ Compile once
const hbs = await setupHandlebars();
const { render } = await compileTemplates(hbs);

// Render many times
attendees.forEach(attendee => {
  const html = render(attendee, event);
});
```

### 7. GitHub Actions Permissions

**Learning**: Workflows need explicit permissions for GitHub Pages deployment.

**Required Configuration**:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

**Also Required**: Repository Settings → Actions → "Read and write permissions"

### 8. Test Artifact Cleanup

**Learning**: Test directories (dist-test/, dist-integration-test/) accumulated.

**Solution**: Use unique test directories and clean up in afterAll hooks:
```typescript
afterAll(async () => {
  await rm(TEST_DIST_DIR, { recursive: true, force: true });
});
```

### 9. CSS Variable Power

**Learning**: CSS custom properties made theming trivial.

**Implementation**:
```css
:root {
  --color-primary: #667eea;
  --color-secondary: #764ba2;
  --gradient-primary: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
}
```

**Benefit**: Change 2 variables → entire theme updates

### 10. Responsive Breakpoints

**Learning**: Mobile-first CSS with strategic breakpoints worked perfectly.

**Breakpoints**:
- Base: < 375px (small mobile)
- 375-767px: Mobile
- 768-1023px: Tablet
- 1024px+: Desktop

**Pattern**:
```css
.stats-grid {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

@media (min-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### 11. Optional Fields for Backward Compatibility (Plan 002)

**Learning**: Optional TypeScript fields enable data model evolution without breaking changes.

**Implementation**:
```typescript
interface Attendee {
  // Required core fields
  id: string;
  firstName: string;
  // ...existing fields...

  // Optional B2B fields (Plan 002)
  productsExplored?: Product[];
  boothsVisited?: BoothVisit[];
  sponsorInteractions?: SponsorInteraction[];
}
```

**Impact**:
- Original 12 attendees (1001-1012) work unchanged
- New Event Tech Live attendees (2001-2012) use B2B fields
- Type guard validates optional fields only if present
- Zero breaking changes to existing data

**Why It Matters**: Enables gradual feature adoption without migration requirements.

### 12. Conditional Template Rendering (Plan 002)

**Learning**: Handlebars partials with conditional rendering keep templates clean and maintainable.

**Implementation**:
```handlebars
<!-- In attendee.hbs -->
{{> products productsExplored=attendee.productsExplored}}
{{> booths boothsVisited=attendee.boothsVisited}}

<!-- In products.hbs partial -->
{{#if productsExplored}}
<section class="products-section">
  <!-- Product cards -->
</section>
{{/if}}
```

**Benefits**:
- B2B sections appear only when data exists
- Original attendees see no empty sections
- DRY principle maintained with reusable partials
- Easy to add new optional sections

**Before**: Monolithic template with complex conditionals
**After**: Modular partials with clean separation

### 13. Multi-Event Architecture (Plan 002)

**Learning**: Supporting multiple events requires minimal code changes with proper data modeling.

**Key Changes**:
- Added `eventId` field to attendees
- Created multiple event configs (`event-2025.json`, `event-tech-live-2025.json`)
- Updated data loader test to support multiple events
- No changes needed to generation engine

**Validation**:
```typescript
// Test now validates multiple events gracefully
it('should load attendees for multiple events', async () => {
  const attendees = await loadAllAttendees();
  const eventIds = attendees.map(a => a.eventId);
  const uniqueEventIds = new Set(eventIds);

  expect(uniqueEventIds.size).toBeGreaterThanOrEqual(1);
  expect(attendees.length).toBeGreaterThan(0);
});
```

**Result**: 24 attendees across 2 events, all tests passing.

### 14. Real Data Quality Matters (Plan 002)

**Learning**: Using authentic company names and data creates believable demonstrations.

**Implementation**:
- Sourced 28 real companies from Event Tech Live CSV
- Created 30 realistic sessions with actual speakers
- Used genuine product names and categories
- Authentic sponsor CTAs with tracking IDs

**Validation**:
```bash
# Event Tech Live pages have 20-96 real company mentions
Attendee 2001: 39 company mentions (ExpoPlatform, Braindate, etc.)
Attendee 2012: 96 company mentions (max engagement persona)
```

**Impact**:
- Demonstrations feel professional and realistic
- Easy to show to potential clients
- Data patterns match real event behaviors
- CTAs drive actual engagement

**Anti-Pattern**: Generic "Company A", "Product B" data looks amateurish.

### 15. Persona-Based Data Generation (Plan 002)

**Learning**: Creating data based on attendee personas produces realistic engagement patterns.

**6 Personas Created**:
1. **Tech Scout** (2001-2002): 10-11 sessions, high innovation focus
2. **Sustainability Champion** (2003-2004): 7-8 sessions, eco-focused
3. **Registration Specialist** (2005-2006): 9 sessions, operational tools
4. **Learning Enthusiast** (2007-2008): 13-14 sessions, max attendance
5. **Hybrid Producer** (2009-2010): 9-10 sessions, streaming/AV focus
6. **Networking Maven** (2011-2012): 5-6 sessions, 26-30 connections

**Benefits**:
- Engagement metrics feel authentic (not uniform)
- Easy to demonstrate different use cases
- Product exploration patterns match persona goals
- Booth visit durations vary realistically (10-35 minutes)

**Example**:
```json
// Tech Scout explores cutting-edge AI/innovation products
"productsExplored": [
  {"name": "Erleah AI Networking", "category": "AI & Innovation"},
  {"name": "ExpoPlatform AI Matchmaking", "category": "Networking"}
]

// Registration Specialist focuses on operational tools
"productsExplored": [
  {"name": "Eventpack Check-In", "category": "Registration"},
  {"name": "Choose 2 Rent Badge Printers", "category": "Registration"}
]
```

**Why It Works**: Data tells a story that matches real attendee behaviors.

### 16. End-to-End Validation is NON-NEGOTIABLE (Plan 003 Critical Lesson)

**Learning**: NEVER claim a multi-system integration is "complete" without running the ACTUAL end-to-end pipeline with REAL data flow.

**What Went Wrong (Plan 003 Phase 5-6)**:
- ✅ Wrote TypeScript integration code
- ✅ Wrote 139 tests (all passing)
- ✅ Created MOCK JSON files to test TypeScript
- ❌ **NEVER ran the Python scraper to produce actual JSON output**
- ❌ **NEVER validated Python → JSON → TypeScript pipeline with real data**
- ❌ **Discovered runtime bugs only when user demanded validation**

**The Fatal Flaw**:
```
CLAIMED: "Phase 6 Complete - Integration fully tested and validated"
REALITY: Only tested TypeScript consuming hand-crafted JSON
MISSED:  - Python scraper requires API key from .env
         - Python scraper has runtime bug (.kickoff() vs .crew().kickoff())
         - Schema compatibility untested with REAL scraped output
```

**Correct Approach**:
1. **Write integration code** ✅
2. **Write integration tests with mocks** ✅
3. **Run ACTUAL end-to-end pipeline** ⚠️ THIS IS MANDATORY
4. **Verify real data flows through entire system** ⚠️ THIS IS MANDATORY
5. **Fix any runtime bugs discovered** ⚠️ THIS IS MANDATORY
6. **THEN and ONLY THEN claim "complete"** ✅

**Validation Checklist for Multi-System Integrations**:
- [ ] All environment variables/secrets configured (check .env)
- [ ] Actual CLI commands run successfully (not just unit tests)
- [ ] Real data produced by System A consumed by System B
- [ ] Schema compatibility verified with ACTUAL output (not mocks)
- [ ] Performance measured with real workloads
- [ ] Error handling tested with real failure scenarios

**Anti-Pattern to Avoid**:
```typescript
// ❌ BAD: Testing integration with hand-crafted mock data
const mockStyleConfig = {
  eventId: "test-event",
  colors: { primary: "#667eea", ... },
  // ... manually created to match schema
};
const css = generateEventCSS(mockStyleConfig); // Tests pass!
// ❌ CLAIM: "Integration validated" - NO IT'S NOT!
```

**Correct Pattern**:
```bash
# ✅ GOOD: Run the actual scraper
python -m event_style_scraper scrape --url https://example.com
# Check JSON file was created
ls -la style-configs/example-com.json
# Run TypeScript with REAL scraped data
npm run generate
# Verify pages have styles from REAL scraped data
grep "color-primary" dist/attendees/1001/index.html
# ✅ NOW you can claim: "Integration validated"
```

**Why This Matters**:
- Unit tests pass but system fails at runtime
- Schema mismatches only show up with real data
- Environment setup issues (API keys, .env) missed
- Integration bugs (wrong method calls) not caught
- Performance issues with real data vs mocks
- **False confidence is worse than no testing**

**Red Flags That You're Not Validating Properly**:
- ❌ "I created sample JSON files to test with"
- ❌ "All tests pass" (but never ran actual CLI)
- ❌ "Schema looks compatible" (but never tried real data)
- ❌ "Should work" (but never executed end-to-end)
- ❌ Claiming "Phase complete" without running actual pipeline

**Rule of Thumb**:
> **If you haven't seen the ACTUAL output file created by System A
> successfully consumed by System B, you haven't validated anything.**

This lesson learned the hard way during Plan 003 implementation.

### 17. Sample/Mock Data Can Hide Critical Flaws (Plan 004 Case Study)

**Learning**: Creating "sample config files" for testing without validating against real sources creates false confidence and leads to production bugs.

**What Happened (Plan 004 Discovery)**:
- Plan 003 Phase 5-6 created `style-configs/event-tech-live-2025.json` as "sample config"
- Config never validated against actual eventtechlive.com website
- Git commit message said "add sample configs for testing" (red flag!)
- Generated pages used wrong brand colors: #00b8d4 (cyan) vs #0072ce (actual blue)
- User discovered mismatch: "notice the style doesn't match what was generated"
- All 139 tests passing, but testing against WRONG data

**The Root Cause**:
```json
// ❌ BAD: Manually created "sample" config (style-configs/event-tech-live-2025.json)
{
  "eventId": "event-tech-live-2025",
  "colors": {
    "primary": "#00b8d4",  // ❌ Cyan - made up color
    "secondary": "#0097a7",  // ❌ Teal - not from website
    "accent": "#ff6f00"  // ❌ Orange - not from website
  },
  "typography": {
    "headingFont": "Montserrat, sans-serif"  // ❌ Wrong font
  },
  "brandVoice": {
    "tone": "energetic"  // ❌ Wrong tone
  }
}
```

**The Actual Reality**:
```json
// ✅ GOOD: Real scraped data from eventtechlive.com
{
  "eventId": "event-tech-live-2025",
  "colors": {
    "primary": "#0072ce",  // ✅ Actual brand blue
    "secondary": "#0a2540",  // ✅ Actual dark blue
    "accent": "#005bb5"  // ✅ Actual accent blue
  },
  "typography": {
    "headingFont": "'Helvetica Neue', Helvetica, Arial, sans-serif"  // ✅ Actual font
  },
  "brandVoice": {
    "tone": "professional"  // ✅ Actual tone
  }
}
```

**Impact**:
- 12 Event Tech Live attendee pages had wrong branding (2001-2012)
- Pages looked unprofessional with mismatched colors
- Damage to credibility if shown to actual event organizers
- Tests gave false confidence (all passing against wrong data)
- Required Plan 004 to fix: scrape real data, regenerate pages, update tests

**How It Should Have Been Done**:

1. **Create Plan 003 Phase 5-6** ✅
2. **Write Python scraper code** ✅
3. **Write TypeScript integration code** ✅
4. **Write tests with mock data** ✅
5. **RUN ACTUAL SCRAPER** ⚠️ THIS WAS SKIPPED
   ```bash
   python -m event_style_scraper scrape --url https://eventtechlive.com
   ```
6. **Validate scraped output against TypeScript** ⚠️ THIS WAS SKIPPED
7. **Regenerate pages with real data** ⚠️ THIS WAS SKIPPED
8. **Visual inspection of generated pages** ⚠️ THIS WAS SKIPPED
9. **THEN claim Phase 6 complete** ✅

**Red Flags to Watch For**:
- ❌ Commit messages saying "sample" or "mock" or "test data"
- ❌ Manually creating JSON files instead of generating them
- ❌ Skipping "visual inspection" or "manual validation" steps
- ❌ "Tests pass" but never looked at actual output
- ❌ Never ran the CLI tool that produces the data
- ❌ Colors/fonts/values that "look reasonable" but aren't verified

**Correct Validation Process**:
```bash
# 1. Run actual scraper (not mocks!)
python -m event_style_scraper scrape --url https://eventtechlive.com --output python/style-configs/output.json

# 2. Convert to TypeScript format
# (handle snake_case → camelCase, fix eventId)

# 3. Regenerate pages with REAL scraped data
npm run generate

# 4. Visual inspection (open in browser)
open dist/attendees/2001/index.html

# 5. Verify colors match actual website
# Compare side-by-side: generated page vs eventtechlive.com

# 6. Save before/after for documentation
cp dist/attendees/2001/index.html analysis/page-comparison-$(date +%Y%m%d)/after.html
```

**Why This Matters**:
- Mock data feels safe but hides integration bugs
- "Sample configs" become tech debt that ships to production
- User catches bugs that tests should have caught
- Visual/manual validation is NOT optional for user-facing output
- Automated tests don't replace human inspection of generated artifacts

**Rule of Thumb**:
> **If the data came from your keyboard instead of the actual source system,
> it's not validated—it's fantasy.**

**Lessons Applied in Fix (Plan 004)**:
1. ✅ Ran actual Python scraper against eventtechlive.com
2. ✅ Captured real scraped output (python/style-configs/eventtechlive-com.json)
3. ✅ Fixed schema conversion (snake_case → camelCase)
4. ✅ Regenerated all 24 pages with correct colors
5. ✅ Updated test expectations to match REAL data (not sample data)
6. ✅ Visual comparison: saved before/after pages for documentation
7. ✅ All 139 tests passing with correct data
8. ✅ Verified #0072ce appears in generated pages (not #00b8d4)

This case study demonstrates why Lesson 16's validation checklist is critical.

### 18. Verify Scraper Output with DevTools (Plan 004 Second Iteration)

**Learning**: Running the actual scraper and using real data isn't enough—you must verify the scraped output matches reality using browser DevTools inspection.

**What Happened (Plan 004 Correction)**:
- ✅ Ran actual Python scraper (better than Plan 003's sample data)
- ✅ Captured real output: `python/style-configs/eventtechlive-com.json`
- ✅ Fed real scraped data through TypeScript pipeline
- ✅ Regenerated all 24 pages with scraped colors
- ✅ All 139 tests passing
- ❌ **Never verified scraped colors against actual website with DevTools**
- ❌ **User discovered color mismatch during visual inspection**

**The Mismatch**:
```json
// Scraper captured (AI-extracted from page content)
"colors": {
  "primary": "#0072ce"  // Medium blue
}

// Actual website (DevTools color picker on header)
"colors": {
  "primary": "#160822"  // Dark purple
}
```

**Why Scraper Got It Wrong**:
- CrewAI agents analyzed page content and made best guess
- May have picked up accent/link colors instead of primary header color
- Without ground truth verification, we trusted AI output blindly
- **Lesson**: AI scrapers are helpful but not infallible—verify their work

**How User Caught It**:
1. Opened http://localhost:8080/attendees/2001/ (generated page)
2. Opened https://eventtechlive.com (actual website)
3. Noticed colors didn't match
4. Used DevTools: Right-click header → Inspect
5. Saw computed color: #160822 (not #0072ce)
6. Reported: "something is off, the primary color on the https://eventtechlive.com is #160822"

**The Missing Validation Step**:
Even though we followed most of the validation checklist, we skipped:
```bash
# ❌ What we did:
python -m event_style_scraper scrape --url https://eventtechlive.com
# Trusted scraper output blindly
npm run generate
# Assumed colors were correct

# ✅ What we should have done:
python -m event_style_scraper scrape --url https://eventtechlive.com
cat python/style-configs/eventtechlive-com.json | jq '.colors.primary'
# Shows: "#0072ce"

# Open https://eventtechlive.com in browser
# Right-click header element → Inspect → Computed tab
# Check background-color or color property
# DevTools shows: rgb(22, 8, 34) = #160822

# Compare: Scraped #0072ce vs Actual #160822 ❌ MISMATCH!
# Manually correct scraped output
jq '.colors.primary = "#160822"' python/style-configs/eventtechlive-com.json > /tmp/fixed.json
mv /tmp/fixed.json python/style-configs/eventtechlive-com.json

# Convert to TypeScript format and regenerate
npm run generate

# Now verify match:
grep "color-primary" dist/attendees/2001/index.html
# Shows: "#160822" ✓
# Open in browser and compare side-by-side with actual site ✓
```

**Impact**:
- First iteration (commit a42d2ae): Wrong color #0072ce
- User visual inspection: Discovered mismatch
- Second iteration (commit bd24327): Correct color #160822
- Even with "proper validation" (Plan 004), we had a gap!

**Why This Matters**:
- **AI/scraper output is not ground truth**
- Automated extraction can make mistakes (wrong element, wrong property)
- Visual inspection alone isn't enough—need DevTools measurement
- "Trusting but verifying" applies to scrapers too
- Color accuracy matters for brand fidelity

**Correct DevTools Verification Process**:

1. **Open actual website** in Chrome/Firefox
2. **Right-click dominant color element** (header, button, logo background)
3. **Select "Inspect"** → Opens DevTools
4. **Check Computed or Styles tab**
5. **Find color property** (background-color, color, border-color)
6. **Note exact hex value** (DevTools shows rgb(), convert to hex)
7. **Compare against scraper output**
8. **If mismatch**: Manually correct scraper output to match DevTools
9. **Regenerate pages** with corrected colors
10. **Visual verification**: Side-by-side comparison in browser

**DevTools Hex Conversion**:
```javascript
// If DevTools shows: rgb(22, 8, 34)
// Convert to hex:
"#" + [22, 8, 34].map(x => x.toString(16).padStart(2, '0')).join('')
// Result: "#160822"
```

**Red Flags You're Skipping DevTools Verification**:
- ❌ "Scraper extracted the colors, should be good"
- ❌ "Tests pass with scraped colors, must be right"
- ❌ "AI analyzed the page, it's probably accurate"
- ❌ "Visual inspection looks close enough"
- ❌ "Don't have time to check every color"

**When to Use DevTools Verification**:
- ✅ Every time you scrape a new website
- ✅ When colors are critical to brand identity
- ✅ Before claiming "validation complete"
- ✅ When user reports "colors don't match"
- ✅ After any scraper code changes

**Rule of Thumb**:
> **Scrapers extract, DevTools verify. Never ship scraped colors without
> DevTools color picker confirmation from the actual website.**

**Lesson Applied in Correction**:
1. ✅ User opened actual website (eventtechlive.com)
2. ✅ Used DevTools to inspect header element
3. ✅ Extracted exact color: #160822
4. ✅ Corrected both scraped JSON files
5. ✅ Regenerated all pages
6. ✅ Updated test expectations
7. ✅ Visual verification: colors now match

**See Also**:
- Lesson 16: End-to-End Validation is NON-NEGOTIABLE
- Lesson 17: Sample/Mock Data Can Hide Critical Flaws
- docs/validation-checklist.md Phase 3.4: "Compare against expected result"

This lesson reinforces that validation is **multi-layered**: run the tools, check the output, verify against reality, inspect visually, measure with DevTools.

### 20. Visual Assets Require Local Hosting for Reliability (Plan 008)

**Learning**: Event logos and visual assets must be hosted locally in `static/` directory rather than relying on external URLs from event websites. External dependencies can break if source sites change structure, require authentication, or go offline.

**What Happened (Plan 008 Discovery)**:
- Event JSON files had `logoUrl: null` despite templates being ready
- AWS re:Invent style config was missing `logoUrl` and `faviconUrl` fields
- Event Tech Live style config referenced external URL: `https://eventtechlive.com/wp-content/themes/eventtechlive/assets/images/logo.svg`
- Markus AI attribution was conditional on `eventCSS` being present (violated PRD-002 requirement)
- No logo image files existed in `static/images/` directory

**The Solution**:
```
1. Create local SVG logos for both events
   - Event Tech Live: 200x60px, brand color #160822
   - AWS re:Invent: 200x60px, AWS colors #232f3e + #ff9900
   - Favicon: 32x32px calendar icon

2. Update event JSON files
   "logoUrl": "/static/images/event-tech-live-logo.svg"

3. Complete style configs with local paths
   "logoUrl": "/static/images/aws-reinvent-logo.svg"
   "faviconUrl": "/static/images/favicon.svg"

4. Remove conditional rendering for Markus AI attribution
   - Attribution must appear on ALL pages per PRD-002
   - Was {{#if eventCSS}} - now unconditional
```

**Impact**:
- **Before**: No logos on any page, missing Markus AI attribution
- **After**: All 24 pages show event logos and Markus AI footer
- **GitHub Pages**: Serves images from same domain (fast, reliable)
- **No external dependencies**: Site remains functional even if event sites change

**Why Local Hosting Matters**:
- External URLs can break (404, authentication required, CORS issues)
- Source sites can restructure or go offline
- Slower load times (external domain lookups)
- GitHub Pages has full control over static assets
- Logos always available during development and production

**Path Conventions**:
- Use absolute paths from repository root: `/static/images/logo.svg`
- Not relative paths: `../../static/images/logo.svg` (breaks on different page depths)
- GitHub Pages serves assets correctly with absolute paths

**SVG Benefits**:
- Scalable to any size without quality loss
- Small file sizes (< 1KB for text-based logos)
- Can embed brand colors directly
- Browser-native support (no dependencies)

**Rule of Thumb**:
> **All visual assets (logos, icons, favicons) that are part of your system's
> branding must be hosted locally in `static/`. External URLs are acceptable
> only for user-generated content or third-party integrations.**

**Validation Checklist**:
- [ ] All image files exist in `static/images/`
- [ ] Event JSON files have non-null `logoUrl` fields
- [ ] Generated HTML contains `<img>` tags with correct paths
- [ ] Images load successfully on deployed site (HTTP 200)
- [ ] Favicon displays in browser tab
- [ ] Required attributions (like Markus AI) are unconditional

**See Also**:
- Plan 008: Fix Missing Event Logos and Markus AI Attribution
- PRD-002: Requirement for Markus AI footer attribution
- `analysis/plan-008-missing-logos-investigation.md`: Root cause analysis

This lesson was learned through Plan 008 implementation and emphasizes the importance of local asset hosting for production reliability.

### 19. Agents Need Explicit Tool Instructions, Not Just Access (Plan 005)

**Learning**: Assigning tools to agents is necessary but not sufficient. Agents may ignore tools and hallucinate content if task descriptions are vague. LLMs default to generating plausible text rather than invoking tools unless explicitly forced.

**What Happened (Plan 005 Discovery)**:
- ✅ Implemented PlaywrightStyleExtractorTool with 100% test coverage
- ✅ Assigned tool to web_scraper_agent in CrewAI configuration
- ❌ **Agent never invoked the tool - it generated fictional HTML/CSS instead**
- ❌ **Agent fabricated "Example Event - Official Site" with made-up colors**
- ❌ **0% tool invocation rate despite tool being available**

**The Hallucination Output**:
```
Agent Output:
"Scraping Report for https://example.com

1. URL Validation & robots.txt Check:...
2. Raw HTML Content:
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <title>Example Event - Official Site</title>  ← FICTIONAL
   ...
   #site-header {
     background-color: #004080;  ← MADE UP
```
- ❌ Agent wrote prose report instead of calling tool
- ❌ Fictional HTML structure that doesn't exist
- ❌ Made-up colors (#004080, #0072ce - generic tech blues)
- ❌ No evidence of tool invocation in logs

**Root Cause**: Task description was too vague:
```yaml
# ❌ BAD: Vague instruction that led to hallucination
scrape_website:
  description: >
    Use the Playwright Style Extractor tool to scrape the website at {url}.
    Extract HTML, CSS, and computed styles. Return the scraped data.
```

**The Fix - Extremely Explicit Instructions**:
```yaml
# ✅ GOOD: Explicit step-by-step instructions
scrape_website:
  description: >
    STEP 1: INVOKE THE TOOL
    You have access to a tool called "Playwright Style Extractor".
    You MUST call this tool with the URL: {url}

    Action: Playwright Style Extractor
    Action Input: {url}

    STEP 2: WAIT FOR TOOL OUTPUT
    The tool will return a structured dictionary containing:
    - url: The scraped URL
    - html: Raw HTML content
    - computed_styles: CSS computed styles
    - css_variables: Custom properties
    - success: Boolean status

    STEP 3: RETURN TOOL OUTPUT AS-IS
    Copy the EXACT output from the tool into your Final Answer.
    DO NOT modify, summarize, or reformat the tool output.

    CRITICAL RULES:
    - If you did not call the tool, your answer is WRONG
    - If you generate fictional HTML/CSS, your answer is WRONG
    - If you write a "scraping report", your answer is WRONG
    - If you guess or imagine website content, your answer is WRONG

    Example of CORRECT workflow:
    Thought: I need to scrape {url} using the Playwright Style Extractor tool
    Action: Playwright Style Extractor
    Action Input: {url}
    Observation: {{"url": "{url}", "html": "<actual html>", ...}}
    Final Answer: {{"url": "{url}", "html": "<actual html>", ...}}
```

**Agent Role Redefinition**:
```yaml
# ❌ BAD: Role implies content generation
web_scraper_agent:
  role: "Web Content Scraper and Style Analyst"
  goal: "Extract and analyze website styles"

# ✅ GOOD: Role emphasizes tool operation only
web_scraper_agent:
  role: "Web Content Scraper (Tool Operator)"
  goal: "Use the Playwright Style Extractor tool to extract raw HTML, CSS, and visual assets. ALWAYS invoke the tool - NEVER generate content."
  backstory: >
    You are a tool operator who ONLY uses the Playwright Style Extractor tool.
    You NEVER generate, guess, or imagine website content.

    Your workflow is simple:
    1. Receive a URL
    2. Invoke the "Playwright Style Extractor" tool
    3. Return the exact tool output

    You are like a vending machine: URL goes in → tool runs → data comes out.
    No thinking, no creativity, no improvisation - just tool invocation.
```

**Results After Fix**:
```
Agent Thought: I will use the Playwright Style Extractor tool
Action: Playwright Style Extractor
Using Tool: Playwright Style Extractor
Tool Input: {"url": "https://example.com"}
Tool Output: {
  "url": "https://example.com",
  "html": "<!DOCTYPE html><html lang=\"en\"><head><title>Example Domain</title>...",
  "computed_styles": {
    "body": {"backgroundColor": "rgb(238, 238, 238)", ...}
  },
  "success": true
}
Final Answer: {same as tool output}
```
- ✅ Agent called tool every time (100% invocation rate)
- ✅ Actual example.com HTML returned
- ✅ Real computed colors from browser
- ✅ Structured data output (not prose)

**Impact**:
- **Before**: 0% tool invocation, 100% hallucinated content
- **After**: 100% tool invocation, 0% hallucinated content
- Integration tests passing with real website data
- Colors match DevTools inspection (validated with automated script)

**Why This Matters**:
- Assigning tools != agents using tools
- LLMs are text generators by default, tool use is learned behavior
- Vague instructions trigger text generation instinct
- Explicit step-by-step format overrides default behavior
- "Tool Operator" role framing reduces hallucination
- Critical for any CrewAI implementation with tools

**Key Strategies for Forcing Tool Invocation**:

1. **Step-by-step format**: STEP 1, STEP 2, STEP 3
2. **Show exact format**: `Action: Tool Name` / `Action Input: {params}`
3. **List negative rules**: "If you did NOT call tool, answer is WRONG"
4. **Provide concrete example**: Show correct thought → action → observation → answer
5. **Redefine agent role**: "Tool Operator" not "Expert" or "Analyst"
6. **Use metaphors**: "You are like a vending machine" (emphasizes mechanical behavior)
7. **Eliminate wiggle room**: "MUST call", "ONLY use", "NEVER generate"

**Red Flags Your Agent Will Hallucinate**:
- ❌ Task says "use the tool" without showing how
- ❌ Agent role is "Expert" or "Analyst" (implies knowledge)
- ❌ No example of correct tool invocation workflow
- ❌ No explicit negative rules (what NOT to do)
- ❌ Task allows flexibility: "scrape and analyze" (analyze = hallucinate)

**Validation Checklist**:
- [ ] Check logs for "Tool: <tool_name>" or "Using Tool:"
- [ ] Verify tool output appears in logs (not just agent's prose)
- [ ] Compare agent output to known ground truth (DevTools for colors)
- [ ] Search for hallucination markers (generic names, made-up CSS)
- [ ] Integration test with real data source
- [ ] Measure tool invocation rate (should be 100%)

**Rule of Thumb**:
> **If your task description doesn't explicitly show the Action/Action Input format
> with a concrete example, your agent will hallucinate instead of using the tool.**

**See Also**:
- Lesson 16: End-to-End Validation is NON-NEGOTIABLE
- Lesson 18: Verify Scraper Output with DevTools
- `docs/scraper-validation-checklist.md`: Tool invocation validation
- `python/tests/integration/test_real_scraping.py`: Integration tests for tool usage
- Plan 005: Comprehensive documentation of the hallucination bug and fix

**Commits**:
- `9405ad6`: Phase 3 fix (explicit task instructions + agent role redefinition)
- `6e0f29d`: Phase 4-5 (integration tests + validation tools)

This lesson was learned through Plan 005 implementation and is critical for any AI agent system that relies on tools for accurate data extraction.

### 21. Automate End-to-End Validation in CI/CD (Plan 006)

**Learning**: Automating the complete pipeline in GitHub Actions provides continuous validation that multi-system integrations work correctly. Manual-triggered scraping with cached fallbacks provides explicit cost control while maintaining integration testing.

**What Was Built (Plan 006 Implementation)**:
- GitHub Actions workflow: Manual scrape → Validate → Generate → Deploy
- E2E validation script: Tests actual Python → TypeScript → HTML pipeline
- Playwright browser caching (~50% faster repeat runs)
- API cost tracking (logs token usage after each scrape)
- Staleness warnings (alerts if configs >30 days old)
- Workflow summaries (shows scraped colors, event names, timestamps)

**The Pipeline**:
```
Manual Trigger → Scrape websites → Commit configs → Generate pages → Deploy
Push to main   → Skip scraping   → Use cached configs → Generate  → Deploy (fast)
```

**Key Design Decisions**:

1. **Manual-Only Scraping**: No scheduled/automated runs
   - ✅ Full cost control (~$0.10/event/scrape, user decides when)
   - ✅ No surprise OpenAI API charges
   - ✅ Explicit timing (scrape before releases, after website redesigns)

2. **Graceful Fallback**: If scraping fails → use last known good config
   - ✅ Deployment never blocked by scraping failures
   - ✅ Cached configs provide reliability
   - ✅ Warning logged, but pipeline continues

3. **End-to-End Test**: Validates actual data flow (not mocks!)
   - ✅ Runs on every push to main/develop
   - ✅ Scrapes example.com with real Playwright + CrewAI
   - ✅ Verifies JSON → TypeScript → HTML → CSS injection
   - ✅ Addresses CLAUDE.md Lesson 16 (E2E validation requirement)

**Performance Impact**:
- First run: ~5-7 min (install Playwright + scrape)
- Cached run: ~3-5 min (50% faster)
- Push-only: <5 min (no scraping overhead)

**Monitoring Features**:
```yaml
# Workflow summary shows:
## 🎨 Scraping Results
✅ Status: Scraping successful

### Style Configurations
- **Event Tech Live 2025** (`event-tech-live-2025`)
  - Primary Color: `#160822`
  - Last Updated: 2024-11-06T12:34:56Z
```

**Cost Tracking**:
```
💰 API Cost Tracking:
   Tokens used: 15,234
   Estimated cost: $0.30
```

**Why This Matters**:
- Continuous validation catches regressions immediately
- Manual triggers prevent cost surprises
- Cached fallbacks ensure reliability
- Workflow summaries provide visibility
- E2E tests prove integration (not just unit tests)
- Addresses Lesson 16's "validate with REAL data" requirement

**Example Usage**:
```bash
# Trigger scraping for all events
gh workflow run scrape-and-deploy.yml

# Scrape specific events only
gh workflow run scrape-and-deploy.yml \
  --field events_to_scrape="eventtechlive.com"

# Force re-scrape even if configs exist
gh workflow run scrape-and-deploy.yml \
  --field force_scrape=true
```

**Rule of Thumb**:
> **Automate validation, not costs. Manual triggers for expensive operations (API calls) + automated testing = continuous validation with predictable expenses.**

**Commits**:
- `a547ec0`: Phase 1 (workflow creation)
- `d31ffc0`: Phase 2 (E2E validation script)
- `a0df305`: Phase 3 (caching, cost tracking, staleness warnings)
- `d5dfb31`: Phase 4 (monitoring, workflow summaries)

This lesson was learned through Plan 006 implementation and demonstrates how to balance automation (for validation) with manual control (for costs).

## Development Standards

### Test-Driven Development (TDD)

**Strict TDD Process**:
1. **RED**: Write failing test first
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve code quality

**Current Metrics** (as of Plan 002 completion):
- 105 tests (100% passing)
- 89.93% coverage (exceeds 85% target)
- 0 HTML validation errors
- 24 pages generated (12 original + 12 Event Tech Live)

### Quality Metrics

- ✅ **Test Coverage**: 89.93% (target: 85%) - **EXCEEDED**
- ✅ **HTML Validation**: 0 errors, 24 warnings across 24 pages
- ✅ **Performance**: < 1s for 24 pages (target: < 2s)
- ✅ **Type Safety**: Full TypeScript with strict mode (100% types coverage)
- ✅ **Accessibility**: Semantic HTML, proper ARIA
- ✅ **Responsive**: Mobile-first, 3 breakpoints
- ✅ **Backward Compatibility**: Zero breaking changes (Plan 002)

### Planning Standards

- Use hypothesis-driven approach
- Define measurable success criteria
- Include empirical validation methods
- No human time estimates
- Phase-by-phase implementation with confirmation

### Documentation Requirements

- ✅ Update CLAUDE.md with lessons learned
- ✅ Create validation reports in `./analysis/`
- ✅ Keep plans/README.md index current
- ✅ Document all public interfaces

## Quick Troubleshooting

### Common Issues

**"npm install fails with EACCES"**
```bash
mkdir -p .npm-cache
npm install --cache .npm-cache
```

**"Tests failing after changes"**
```bash
# Clean test artifacts
rm -rf dist-test/ dist-integration-test/ dist-validation-test/

# Rebuild and test
npm run build
npm test
```

**"Need to understand current implementation"**
```bash
/explore  # Run exploration command
```

**"Want to add a new feature"**
```bash
/plan [feature description]  # Create plan first
# Review plan
/implement ./plans/NNN-feature.md  # Then implement
```

**"GitHub Pages 404 errors"**
```bash
# Verify .nojekyll exists
ls dist/.nojekyll

# Check GitHub Pages source is "GitHub Actions"
# Settings → Pages → Source → "GitHub Actions"

# Verify workflow permissions
# Settings → Actions → General → "Read and write permissions"
```

**"CSS not loading on generated pages"**
```bash
# Verify CSS exists
ls static/css/styles.css

# Regenerate
npm run generate

# Verify copied to dist
ls dist/static/css/styles.css
```

## Data Models

Comprehensive data models documented in `requirements/data-models.md`.

**Key Interfaces**:
- `Event`: Event configuration and metadata
- `Attendee`: Attendee profile, sessions, connections, stats
- `Session`: Conference session details
- `Connection`: Networking connection data
- `CallToAction`: Re-engagement CTAs

**Example**:
```typescript
interface Attendee {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  eventId: string;
  sessions: Session[];
  connections: Connection[];
  stats: AttendeeStats;
  callsToAction: CallToAction[];
}
```

## Environment Configuration

No environment variables required for basic operation.

**Optional**:
- `NODE_ENV=development` for development builds
- Custom variables for analytics, API keys, etc.

## Security Considerations

✅ **Implemented**:
- Input validation via TypeScript type guards
- Path traversal prevention (validated attendee IDs)
- HTML entity encoding (Handlebars default)
- HTTPS enforcement on GitHub Pages

**Best Practices**:
- Never commit `.env` files
- Validate all external data at load time
- Use HTTPS for all external links
- Escape user-generated content (handled by Handlebars)

## Performance Guidelines

**Target**: < 2 seconds for full site generation
**Achieved**: 500ms for 12 pages

**Optimizations**:
1. Parallel page generation with `Promise.all()`
2. Single template compilation, multiple renders
3. Async file operations with `fs/promises`
4. Minimal dependencies (Handlebars only)

**Monitoring**:
```bash
# Time generation
time npm run generate

# Profile with Node
node --prof dist/generate.js
```

## Important Notes

### When Creating Plans

- Always validate assumptions empirically
- Store analysis artifacts in `./analysis/`
- Never include human time estimates
- Define clear success criteria
- Break into phases with confirmation points

### When Implementing

- Follow TDD strictly (RED-GREEN-REFACTOR)
- Seek confirmation between phases
- Validate all outcomes empirically
- Update documentation as you go
- Mark todos complete immediately after finishing

### When Exploring

- Validate claims with code inspection
- Note discrepancies between docs and reality
- Store findings in analysis directory
- Check actual generated output, not just templates

### When Testing

- Unit tests for individual functions
- Integration tests for complete pipelines
- HTML validation for output quality
- Performance tests for generation speed
- All tests must pass before moving to next phase

## Technology Stack

**Core**:
- Node.js 18.x / 20.x
- TypeScript 5.9.3 (strict mode)
- Handlebars 4.7.8

**Testing**:
- Vitest 1.6.1 (test framework)
- @vitest/coverage-v8 (coverage)
- html-validate 8.x (HTML validation)

**Build & Deploy**:
- GitHub Actions
- GitHub Pages
- TypeScript compiler (tsc)

**Development**:
- ESLint (linting)
- Prettier (formatting)
- http-server (local preview)

---

**Last Updated**: 2025-11-07
**Project Status**: ✅ Production Ready (v1.2.0 - Plan 008 Completed)
**Documentation Version**: 2.5
**Test Coverage**: 89.93%
**Total Tests**: 139 passing
**Pages Generated**: 24 (12 Event Tech Live + 12 AWS re:Invent)
**Lessons Learned**: 20 (10 from Plan 001, 5 from Plan 002, 1 from Plan 003, 1 from Plan 004, 2 from Plan 005, 1 from Plan 008)
