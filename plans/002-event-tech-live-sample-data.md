# Plan 002: Event Tech Live High-Quality Sample Data Enhancement

**Status:** Draft
**Created:** 2025-11-06
**Last Updated:** 2025-11-06
**Priority:** 🟡 High

## Overview

This plan enhances our sample data set by incorporating insights from the real Event Tech Live 2025 conference data (28 companies, 214 products) to create more realistic and valuable attendee wrap pages. Rather than using generic mock data, we'll generate attendees who experienced a real B2B event technology conference with actual exhibitors, products, and industry-specific sessions. This one-time enhancement will demonstrate the system's capability with production-quality data while maintaining our attendee-centric focus.

The Event Tech Live data provides authentic company names, product categories, and technology trends that make our wrap pages feel genuine. We'll extend our data model minimally to capture B2B-specific insights like "products explored" and "booth visits" while keeping the core attendee experience central. This approach creates sample pages that event organizers can immediately recognize as valuable for their attendees.

## Target Outcomes

### Primary Outcomes
1. **12 high-quality attendee profiles** based on Event Tech Live 2025 with realistic personas and engagement patterns
2. **Enhanced data model** with optional B2B fields (products explored, booth visits, sponsor interactions)
3. **Authentic wrap pages** featuring real companies, actual products, and industry-relevant achievements
4. **Updated event data** reflecting Event Tech Live's actual details (November 12-13, 2025, London)

### Success Criteria
- [ ] All 12 attendees have unique, realistic profiles with Event Tech Live context
- [ ] Sessions reference actual company specialties from the CSV data
- [ ] Connections use real company names and appropriate job titles
- [ ] Products explored match actual products from the CSV catalog
- [ ] CTAs include real sponsors/partners with authentic messaging
- [ ] Achievements reflect B2B event engagement (booth visits, product demos, sustainability)
- [ ] Generated pages pass all existing tests (85%+ coverage maintained)
- [ ] Pages feel authentic to someone familiar with Event Tech Live

### Validation Strategy

#### Empirical Validation Methods
- **Method 1: Data Authenticity Verification**
  - Tools/Commands: `grep -r "Choose 2 Rent\|Eventpack\|TransPerfect" data/attendees/`
  - Expected Results: Real company names appear in connections, sessions, and products
  - Acceptance Threshold: 100% of attendees reference at least 3 real companies

- **Method 2: Enhanced Field Usage**
  - Tools/Commands: `jq '.productsExplored | length' data/attendees/*.json | sort -u`
  - Expected Results: Each attendee has 3-15 products explored
  - Acceptance Threshold: All B2B fields populated appropriately

- **Method 3: Page Generation Success**
  - Tools/Commands: `npm run generate && npm test`
  - Expected Results: 12 pages generated, all tests pass, coverage ≥85%
  - Acceptance Threshold: No regression in functionality or quality

- **Method 4: Content Quality Check**
  - Tools/Commands: Manual review of 3 generated pages
  - Expected Results: Pages show Event Tech Live branding, real companies, authentic CTAs
  - Acceptance Threshold: Content feels production-ready, not generic

## Hypothesis-Driven Approach

### Hypothesis 1: Minimal data model extensions can capture B2B value without breaking existing functionality
**Reasoning:** Our current model is flexible enough to add optional fields for B2B events (products explored, booth visits) while maintaining backward compatibility. TypeScript's optional properties and Handlebars' conditional rendering make this seamless.

**Validation Method:**
- Experiment: Add optional fields to Attendee interface and test with both old and new data
- Expected Outcome: Existing tests pass, new fields render when present
- Validation Steps:
  1. Add optional fields to `src/types/index.ts`
  2. Update type guards to handle optional fields
  3. Run existing test suite
  4. Create test attendee with new fields
  5. Verify page generation works for both data types

**Success Criteria:**
- [ ] TypeScript compilation succeeds with no errors
- [ ] All 87 existing tests continue to pass
- [ ] New fields appear in generated HTML when present
- [ ] Old attendee data still generates correctly

**Failure Conditions:**
- Type guards reject valid data
- Fallback approach: Create separate B2B attendee type extending base type

### Hypothesis 2: Using real company data makes wrap pages significantly more valuable
**Reasoning:** Attendees will recognize actual vendors they met, products they explored, and speakers they heard. This authenticity increases engagement and demonstrates real value from the event.

**Validation Method:**
- Experiment: Generate pages with Event Tech Live data vs generic data
- Expected Outcome: Event Tech Live pages have higher information density and specificity
- Validation Steps:
  1. Generate page with generic "TechConf 2025" data
  2. Generate page with Event Tech Live data
  3. Compare specificity of content (real vs generic company names)
  4. Count authentic data points per page

**Success Criteria:**
- [ ] Event Tech Live pages reference 10+ real companies
- [ ] Products explored match actual CSV catalog
- [ ] Sessions align with company specialties
- [ ] CTAs use actual sponsor messaging

**Failure Conditions:**
- Pages feel too vendor-focused, lose attendee perspective
- Fallback approach: Balance vendor mentions with attendee achievements

### Hypothesis 3: Six personas can represent diverse attendee types at a B2B event
**Reasoning:** Different attendees have different goals (sourcing tech, learning, networking, sustainability). Creating personas ensures our sample data represents the full spectrum of event engagement.

**Validation Method:**
- Experiment: Create 6 personas with distinct engagement patterns
- Expected Outcome: Each persona has unique stats, sessions, and connections
- Validation Steps:
  1. Define 6 personas (Tech Scout, Sustainability Champion, etc.)
  2. Assign 2 attendees per persona
  3. Verify diversity in stats and engagement
  4. Check for realistic variation within personas

**Success Criteria:**
- [ ] Session counts vary from 5-15 across personas
- [ ] Connection patterns differ (vendor-heavy vs peer-heavy)
- [ ] Product exploration aligns with persona goals
- [ ] Achievements match engagement style

**Failure Conditions:**
- Personas feel too similar or unrealistic
- Fallback approach: Create 12 unique profiles without persona structure

## Implementation Details

### Phase 1: Data Model Enhancement
**Objective:** Extend the Attendee interface with optional B2B fields while maintaining backward compatibility

**Steps:**
1. Update TypeScript interfaces
   - File(s) affected: `src/types/index.ts`
   - Changes: Add optional fields for productsExplored, boothsVisited, sponsorInteractions
   - Validation: `npm run type-check` succeeds

2. Enhance type guards
   - File(s) affected: `src/types/index.ts`
   - Changes: Update isAttendee() to validate optional fields when present
   - Validation: Unit tests for type guards pass

3. Update Handlebars templates
   - File(s) affected: `templates/pages/attendee.hbs`
   - Changes: Add conditional sections for products explored and booth visits
   - Validation: Template compiles and renders both old and new data

4. Add B2B-specific partials
   - File(s) affected: `templates/partials/products.hbs`, `templates/partials/booths.hbs`
   - Changes: Create reusable components for B2B content
   - Validation: Partials render when data is present

**Validation Checkpoint:**
- [ ] TypeScript interfaces compile without errors
- [ ] Type guards accept both old and new data formats
- [ ] Templates render optional fields conditionally
- [ ] All existing tests pass (87/87)

### Phase 2: Event Tech Live Event Configuration
**Objective:** Replace generic event with authentic Event Tech Live 2025 details

**Steps:**
1. Create Event Tech Live event file
   - File(s) affected: `data/events/event-tech-live-2025.json`
   - Changes: Use actual event details from CSV (Nov 12-13, 2025, London)
   - Validation: JSON validates against Event interface

2. Add event branding and metadata
   - File(s) affected: `data/events/event-tech-live-2025.json`
   - Changes: Include actual website URL, description, stats from CSV
   - Validation: All required fields populated

3. Update static assets
   - File(s) affected: `static/images/event-tech-live-logo.png`
   - Changes: Add placeholder logo for Event Tech Live
   - Validation: Image file exists and is referenced correctly

**Validation Checkpoint:**
- [ ] Event file contains authentic Event Tech Live information
- [ ] Event loads successfully with dataLoader
- [ ] Event metadata reflects actual conference (28 companies, 214 products)

### Phase 3: Session Generation from Company Data
**Objective:** Create realistic sessions based on actual company specialties

**Steps:**
1. Extract session topics from company analysis
   - File(s) affected: `data/sessions/event-tech-live-sessions.json`
   - Changes: Create 30 sessions based on company expertise
   - Validation: Sessions align with company products/services

2. Map sessions to tracks
   - File(s) affected: Session data files
   - Changes: Organize into 9 tracks (Registration, Engagement, Sustainability, etc.)
   - Validation: Each track has 3-5 sessions

3. Assign realistic speakers
   - File(s) affected: Session speaker fields
   - Changes: Use actual company representatives as speakers
   - Validation: Speaker companies match session topics

**Validation Checkpoint:**
- [ ] 30 unique sessions created from company data
- [ ] Sessions distributed across 9 relevant tracks
- [ ] All sessions have speakers from appropriate companies
- [ ] Session times follow realistic conference schedule

### Phase 4: Attendee Profile Generation
**Objective:** Create 12 diverse attendee profiles using Event Tech Live context

**Steps:**
1. Generate Tech Scout personas (Attendees 2001-2002)
   - File(s) affected: `data/attendees/2001.json`, `data/attendees/2002.json`
   - Changes: High session count (10+), focus on innovation/AI tracks
   - Validation: Profiles show tech exploration focus

2. Generate Sustainability Champion personas (Attendees 2003-2004)
   - File(s) affected: `data/attendees/2003.json`, `data/attendees/2004.json`
   - Changes: Sustainability sessions, One Tribe/enviricard connections
   - Validation: Green achievements and eco-friendly products

3. Generate Registration Specialist personas (Attendees 2005-2006)
   - File(s) affected: `data/attendees/2005.json`, `data/attendees/2006.json`
   - Changes: Registration/check-in sessions, badge printer products
   - Validation: Operational focus in stats

4. Generate Learning Enthusiast personas (Attendees 2007-2008)
   - File(s) affected: `data/attendees/2007.json`, `data/attendees/2008.json`
   - Changes: Maximum sessions (13+), diverse tracks
   - Validation: High hours invested, variety in exploration

5. Generate Hybrid Event Producer personas (Attendees 2009-2010)
   - File(s) affected: `data/attendees/2009.json`, `data/attendees/2010.json`
   - Changes: Streaming/hybrid sessions, AV equipment products
   - Validation: Virtual/hybrid technology focus

6. Generate Networking Maven personas (Attendees 2011-2012)
   - File(s) affected: `data/attendees/2011.json`, `data/attendees/2012.json`
   - Changes: Fewer sessions (5-6), high connection count (15+)
   - Validation: Booth visits and sponsor interactions emphasized

**Validation Checkpoint:**
- [ ] All 12 attendees have complete, unique profiles
- [ ] Each persona type shows distinct engagement patterns
- [ ] Real company names used throughout
- [ ] Products explored match CSV catalog

### Phase 5: Authentic Connections and CTAs
**Objective:** Populate connections with real companies and CTAs with actual sponsor messaging

**Steps:**
1. Create connection pool from CSV companies
   - File(s) affected: All attendee connection arrays
   - Changes: Use real company names with appropriate titles
   - Validation: All connections traceable to CSV data

2. Add vendor/peer/speaker mix
   - File(s) affected: Connection distributions
   - Changes: 60% vendors, 30% peers, 10% speakers
   - Validation: Realistic professional network

3. Implement sponsor CTAs
   - File(s) affected: All attendee callsToAction arrays
   - Changes: Use actual sponsor offers (Choose 2 Rent discount, Erleah AI, etc.)
   - Validation: CTAs match company offerings

4. Add Event Tech Live 2026 CTA
   - File(s) affected: Primary CTA for all attendees
   - Changes: Include "Save the Date" for next year
   - Validation: Consistent re-engagement messaging

**Validation Checkpoint:**
- [ ] Every attendee has 3-15 connections with real companies
- [ ] CTAs use authentic sponsor messaging
- [ ] Connection titles are appropriate for B2B context
- [ ] All attendees have Event Tech Live 2026 as primary CTA

### Phase 6: Products and Achievements
**Objective:** Add product exploration data and relevant achievements

**Steps:**
1. Map products to attendees
   - File(s) affected: productsExplored field in attendee files
   - Changes: Add 3-15 products based on persona and sessions
   - Validation: Products match companies met and sessions attended

2. Create achievement categories
   - File(s) affected: stats.topAchievement field
   - Changes: Add B2B achievements (Booth Marathon, Green Champion, etc.)
   - Validation: Achievements align with engagement patterns

3. Add booth visit data
   - File(s) affected: boothsVisited field (optional)
   - Changes: List companies whose booths were visited
   - Validation: Booth visits correlate with connections

**Validation Checkpoint:**
- [ ] Products explored match attendee interests
- [ ] Achievements reflect actual engagement
- [ ] All product references exist in CSV data
- [ ] Booth visits align with connection data

### Phase 7: Testing and Validation
**Objective:** Ensure new data works with existing system and maintains quality

**Steps:**
1. Run generation with new data
   - File(s) affected: None (testing only)
   - Changes: `npm run generate` with Event Tech Live data
   - Validation: 12 pages generated successfully

2. Execute full test suite
   - File(s) affected: None (testing only)
   - Changes: `npm test` with new data
   - Validation: All 87 tests pass, coverage ≥85%

3. HTML validation
   - File(s) affected: None (testing only)
   - Changes: Validate generated pages
   - Validation: 0 HTML errors, W3C compliant

4. Manual review
   - File(s) affected: None (review only)
   - Changes: Inspect 3 generated pages
   - Validation: Content authentic, CTAs functional, design consistent

**Validation Checkpoint:**
- [ ] Generation completes in <2 seconds
- [ ] Test coverage maintained at 85%+
- [ ] HTML validation passes
- [ ] Pages look production-ready

## Dependencies

### Prerequisites
- [x] Plan 001 completed (system is production-ready)
- [x] Event Tech Live CSV data available in examples/
- [x] Analysis documents created (insights, quick reference, summary)
- [x] Current system generating successfully

### Related Plans
- `plans/001-github-pages-attendee-summary.md` - Base system this enhances

### External Dependencies
- None - using existing CSV data and current toolchain

## Risk Assessment

### High Risk Items
None identified - this is additive enhancement to working system

### Medium Risk Items
1. **Risk:** Breaking backward compatibility with data model changes
   - **Likelihood:** Low (using optional fields)
   - **Impact:** Medium (would affect existing tests)
   - **Mitigation:** All new fields are optional
   - **Contingency:** Keep changes isolated to new attendee files

2. **Risk:** Over-complicating templates with B2B content
   - **Likelihood:** Medium
   - **Impact:** Low (aesthetic only)
   - **Mitigation:** Use conditional rendering and partials
   - **Contingency:** Create separate B2B template if needed

3. **Risk:** Sample data becomes too Event Tech Live specific
   - **Likelihood:** Low
   - **Impact:** Low (it's intentionally specific)
   - **Mitigation:** Keep generic event data as alternative
   - **Contingency:** Maintain both data sets

## Rollback Plan

If implementation causes issues:

1. Remove new attendee files: `rm data/attendees/20*.json`
2. Remove new event file: `rm data/events/event-tech-live-2025.json`
3. Revert type definition changes: `git checkout src/types/index.ts`
4. Revert template changes: `git checkout templates/`
5. Run tests to confirm system stability: `npm test`

**Validation after rollback:**
- [ ] Original 12 attendees still generate
- [ ] All tests pass
- [ ] No references to Event Tech Live remain

## Testing Strategy

### Unit Tests
- [ ] Test coverage for new optional fields in type guards
- [ ] Test coverage for products/booths template helpers
- [ ] Test coverage for loading Event Tech Live event data

### Integration Tests
- [ ] Test generation with B2B-enhanced attendees
- [ ] Test generation mixing old and new attendee formats
- [ ] Test empty optional fields don't break generation

### Manual Testing
1. Generate all 12 Event Tech Live attendees
2. Verify real company names appear correctly
3. Check products explored section renders
4. Confirm CTAs link to actual sponsors
5. Validate achievements are appropriate

### Validation Commands
```bash
# Verify Event Tech Live data loads
node -e "const d = require('./dist/dataLoader'); d.loadEvent('event-tech-live-2025').then(console.log)"

# Check for real company names in generated pages
grep -r "Choose 2 Rent\|Eventpack\|TransPerfect" dist/attendees/

# Verify all attendees have products explored
jq '.productsExplored | length' data/attendees/20*.json

# Count unique companies referenced
grep -h "company" data/attendees/20*.json | sort -u | wc -l

# Verify generation succeeds
npm run generate

# Run tests to ensure no regression
npm test

# Check test coverage maintained
npm run test:coverage
```

## Post-Implementation

### Documentation Updates
- [ ] Update README.md to mention Event Tech Live sample data
- [ ] Document new optional fields in data-models.md
- [ ] Add examples of B2B wrap pages to docs
- [ ] Update CLAUDE.md with lessons learned

### Knowledge Capture
- [ ] Document real-world data integration process
- [ ] Note which Event Tech Live insights were most valuable
- [ ] Record persona-based generation approach
- [ ] List B2B-specific enhancements made

## Appendix

### References
- `analysis/event-tech-live-data-insights.md` - Comprehensive analysis
- `analysis/event-tech-live-quick-reference.md` - Copy-paste ready data
- `analysis/event-tech-live-csv-summary.md` - Technical CSV documentation
- `examples/event_live_conf_data/*.csv` - Source data files

### Alternative Approaches Considered
1. **Approach:** Complete system redesign for B2B events
   - **Pros:** Perfect fit for Event Tech Live data
   - **Cons:** Major effort, breaks existing system
   - **Why not chosen:** User wants one-time sample enhancement, not redesign

2. **Approach:** Simple find-replace of company names
   - **Pros:** Minimal effort
   - **Cons:** Misses valuable insights, feels shallow
   - **Why not chosen:** Doesn't leverage rich product and company data

3. **Approach:** Generate 100+ attendees
   - **Pros:** Shows scale
   - **Cons:** Excessive for demo, maintenance burden
   - **Why not chosen:** 12 quality profiles better than 100 generic ones

### Notes
- Event Tech Live represents the B2B event tech industry well
- Focus remains on attendee value, not vendor promotion
- Optional fields ensure backward compatibility
- This enhancement makes the demo system production-ready for B2B events
- Consider keeping both generic and Event Tech Live data for different demos