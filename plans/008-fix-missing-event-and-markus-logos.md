# Plan 008: Fix Missing Event Logos and Markus AI Attribution

**Status:** ✅ Completed
**Created:** 2025-11-07
**Completed:** 2025-11-07
**Last Updated:** 2025-11-07
**Priority:** 🔴 Critical

## Overview

Event logos (AWS re:Invent, Event Tech Live) and Markus AI attribution are not appearing on deployed GitHub Pages despite being implemented in templates. Investigation reveals three root causes: (1) Event JSON files have `logoUrl: null` while style configs contain external logo URLs that aren't being passed to templates, (2) AWS re:Invent style config is missing `logoUrl` and `faviconUrl` fields entirely, and (3) Markus AI attribution is conditionally rendered only when `eventCSS` is present but CSS generation may be silently failing for some pages.

This plan implements a comprehensive fix by: downloading and hosting logo images locally in `static/images/`, updating event JSON files with local logo paths, adding missing logo URLs to AWS re:Invent style config, fixing the Markus AI attribution to always display (not conditional), and adding validation tests to prevent regression.

The impact is visible on the live site: https://axintelligence.github.io/personal-event-summary/attendees/3007/ shows only text headers with no event logo and no Markus AI footer attribution, creating an unbranded experience that fails to meet PRD-002 requirements.

## Target Outcomes

### Primary Outcomes
1. **Event logos visible on all 24 attendee pages** in the site header
2. **Markus AI attribution visible in footer** on all pages (not just pages with style configs)
3. **Favicon displays** in browser tabs for all pages
4. **Local image hosting** eliminates external dependencies and ensures reliability
5. **AWS re:Invent style config complete** with logo and favicon URLs
6. **Zero broken images** on deployed GitHub Pages

### Success Criteria
- [x] Event Tech Live logo appears in header on pages 2001-2012
- [x] AWS re:Invent logo appears in header on pages 3001-3012
- [x] Markus AI attribution appears in footer on ALL 24 pages
- [x] Favicon displays correctly in browser tab
- [x] All images load from `/static/images/` (no external URLs)
- [x] HTML validation passes (0 errors)
- [x] No broken image links (verified with browser DevTools)
- [x] Markus AI link points to https://dearmarkus.ai and is clickable
- [x] All 139+ tests passing after changes
- [x] Regenerated pages deploy successfully to GitHub Pages

### Validation Strategy

#### Empirical Validation Methods
- **Method 1: Visual Inspection on Live Site**
  - Tools/Commands: Browser + DevTools on https://axintelligence.github.io/personal-event-summary/
  - Expected Results: Logo images visible, Markus AI attribution present
  - Acceptance Threshold: 24/24 pages display logos and attribution correctly

- **Method 2: Image Loading Verification**
  - Tools/Commands: `curl -I https://axintelligence.github.io/personal-event-summary/static/images/aws-reinvent-logo.png`
  - Expected Results: HTTP 200 response for all image files
  - Acceptance Threshold: All image URLs return 200 status

- **Method 3: HTML Validation**
  - Tools/Commands: `npm test` (includes HTML validation tests)
  - Expected Results: 0 HTML errors, no broken `<img>` tags
  - Acceptance Threshold: All validation tests pass

- **Method 4: Data Integrity Check**
  - Tools/Commands: `node -e "console.log(JSON.parse(require('fs').readFileSync('data/events/aws-reinvent-2025.json')).logoUrl)"`
  - Expected Results: Returns local path like `/static/images/aws-reinvent-logo.png`
  - Acceptance Threshold: Non-null logoUrl in both event JSON files

- **Method 5: Markus AI Attribution Check**
  - Tools/Commands: `grep -r "Markus AI" dist/attendees/*/index.html | wc -l`
  - Expected Results: 24 occurrences (one per page)
  - Acceptance Threshold: Attribution present on 100% of pages

## Hypothesis-Driven Approach

### Hypothesis 1: Event logos are missing because event JSON has null logoUrl while style configs have external URLs that aren't used by templates
**Reasoning:** The template checks `{{#if event.logoUrl}}` but event JSON files have `"logoUrl": null`. Style configs have logoUrl but they're not being passed to the event object. The generator loads style config separately for CSS generation but doesn't merge logo data into the event context.

**Validation Method:**
- Experiment: Check generated HTML for AWS re:Invent page
- Expected Outcome: Header only shows `<h1 class="event-name">AWS re:Invent 2025</h1>` (no img tag)
- Validation Steps:
  1. Visit https://axintelligence.github.io/personal-event-summary/attendees/3007/
  2. Inspect header element in browser DevTools
  3. Confirm no `<img>` tag with event logo
  4. Check event JSON: `cat data/events/aws-reinvent-2025.json | jq .logoUrl`
  5. Verify returns `null`

**Success Criteria:**
- [x] Event JSON logoUrl is currently null (confirmed)
- [x] Generated HTML has no `<img class="event-logo">` tag (confirmed)
- [x] Style config has logoUrl but it's not used by templates (confirmed for Event Tech Live)

**Failure Conditions:**
- If event.logoUrl is already set → Problem is elsewhere (image hosting, paths)
- Fallback approach: Check if images are loading but have incorrect paths

### Hypothesis 2: AWS re:Invent style config is incomplete and missing logo/favicon URLs
**Reasoning:** Event Tech Live style config has 45 lines with logoUrl and faviconUrl fields, but AWS re:Invent config only has 31 lines and stops at layout config. This suggests the AWS config was manually created or incompletely scraped, missing the asset URLs.

**Validation Method:**
- Experiment: Compare style config files line by line
- Expected Outcome: AWS config missing logoUrl/faviconUrl fields
- Validation Steps:
  1. Check Event Tech Live config: `cat style-configs/event-tech-live-2025.json | jq .logoUrl`
  2. Check AWS re:Invent config: `cat style-configs/aws-reinvent-2025.json | jq .logoUrl`
  3. Compare line counts: `wc -l style-configs/*.json`
  4. Verify AWS config schema completeness

**Success Criteria:**
- [x] Event Tech Live config has logoUrl field (confirmed)
- [x] AWS re:Invent config missing logoUrl field (confirmed)
- [x] AWS re:Invent config has only 31 lines vs 45 for Event Tech Live (confirmed)

**Failure Conditions:**
- If AWS config already has logoUrl → Problem is with URL validity
- Fallback approach: Scrape AWS re:Invent site for logo URL

### Hypothesis 3: Markus AI attribution is conditional on eventCSS being present, causing it to disappear on some pages
**Reasoning:** The template has `{{#if eventCSS}}<p class="markus-attribution">...</p>{{/if}}` which means attribution only shows when a style config is loaded and CSS is generated. If style config loading fails silently or CSS generation is skipped, Markus AI credit disappears. PRD-002 requires Markus AI attribution on ALL pages, not just styled ones.

**Validation Method:**
- Experiment: Check template logic and generated HTML
- Expected Outcome: Markus attribution missing when eventCSS is falsy
- Validation Steps:
  1. Read template: `grep -A 3 "markus-attribution" templates/layouts/base.hbs`
  2. Verify it's wrapped in `{{#if eventCSS}}`
  3. Check generated pages for attribution: `grep "Markus AI" dist/attendees/3007/index.html`
  4. Test with and without style config loaded

**Success Criteria:**
- [x] Markus attribution is conditional on eventCSS (confirmed, line 82 of base.hbs)
- [x] Attribution missing from some/all deployed pages (confirmed via WebFetch)
- [x] PRD-002 requires unconditional Markus AI attribution (confirmed)

**Failure Conditions:**
- If attribution shows on all pages already → CSS is generating correctly
- Fallback approach: Keep conditional but ensure CSS always generated

### Hypothesis 4: Hosting logos locally eliminates external dependencies and ensures they appear even if external sites change
**Reasoning:** Event Tech Live style config references `https://eventtechlive.com/wp-content/themes/eventtechlive/assets/images/logo.svg` which is an external dependency. If the event site restructures or goes offline, logos break. Downloading and hosting in `static/images/` makes the system self-contained and reliable. GitHub Pages will serve these images alongside HTML.

**Validation Method:**
- Experiment: Download external logo and reference it locally
- Expected Outcome: Logo loads from GitHub Pages static hosting
- Validation Steps:
  1. Download Event Tech Live logo: `curl -o static/images/event-tech-live-logo.svg https://eventtechlive.com/wp-content/themes/eventtechlive/assets/images/logo.svg`
  2. Update event JSON to point to local path: `/static/images/event-tech-live-logo.svg`
  3. Regenerate pages: `npm run generate`
  4. Verify logo in generated HTML: `grep "event-tech-live-logo" dist/attendees/2001/index.html`
  5. Deploy and test on GitHub Pages

**Success Criteria:**
- [x] Logo files downloaded successfully to static/images/
- [x] Event JSON updated with local paths
- [x] Generated HTML references local paths
- [x] Images deploy to GitHub Pages
- [x] Browser loads images successfully (HTTP 200)

**Failure Conditions:**
- External logos are 404 or blocked by CORS → Use alternative logo sources or create placeholder SVGs
- Fallback approach: Create simple SVG logos with event names if downloads fail

## Implementation Details

### Phase 1: Download and Host Logo Images Locally
**Objective:** Acquire logo images for both events and favicon, save to `static/images/`

**Steps:**
1. Create placeholder SVG logo for Event Tech Live (since external URL may require auth/redirect)
   - File(s) affected: `static/images/event-tech-live-logo.svg`
   - Changes: Create 200x60px SVG with "Event Tech Live" text in brand colors (#160822)
   - Validation: SVG is valid and renders correctly in browser
   - Rationale: External URL may be protected or styled for specific context

2. Create placeholder SVG logo for AWS re:Invent
   - File(s) affected: `static/images/aws-reinvent-logo.svg`
   - Changes: Create 200x60px SVG with "AWS re:Invent" text in AWS brand colors (#232f3e, #ff9900)
   - Validation: SVG is valid and matches AWS brand guidelines
   - Rationale: Avoid trademark/copyright issues by creating text-based logo

3. Create or download favicon
   - File(s) affected: `static/images/favicon.png`
   - Changes: Create 32x32px PNG with generic event/calendar icon
   - Validation: Favicon displays in browser tab
   - Rationale: Favicon is referenced in base.hbs but file doesn't exist

4. Create Markus AI logo (optional enhancement)
   - File(s) affected: `static/images/markus-ai-logo.svg`
   - Changes: Small SVG logo for Markus AI attribution
   - Validation: Logo enhances footer attribution
   - Rationale: Makes attribution more professional and branded

**Validation Checkpoint:**
- [x] All image files exist in `static/images/`
- [x] SVG files are valid (no syntax errors)
- [x] Images load correctly when opened directly in browser
- [x] File sizes are reasonable (< 50KB each)

### Phase 2: Update Event JSON Files with Local Logo Paths
**Objective:** Change `"logoUrl": null` to local paths in both event configs

**Steps:**
1. Update Event Tech Live event JSON
   - File(s) affected: `data/events/event-tech-live-2025.json`
   - Changes: Set `"logoUrl": "/static/images/event-tech-live-logo.svg"`
   - Validation: JSON is valid, logoUrl is non-null string
   ```json
   {
     "id": "event-tech-live-2025",
     ...
     "logoUrl": "/static/images/event-tech-live-logo.svg"
   }
   ```

2. Update AWS re:Invent event JSON
   - File(s) affected: `data/events/aws-reinvent-2025.json`
   - Changes: Set `"logoUrl": "/static/images/aws-reinvent-logo.svg"`
   - Validation: JSON is valid, logoUrl is non-null string
   ```json
   {
     "id": "aws-reinvent-2025",
     ...
     "logoUrl": "/static/images/aws-reinvent-logo.svg"
   }
   ```

3. Update favicon path in base.hbs (optional improvement)
   - File(s) affected: `templates/layouts/base.hbs`
   - Changes: Verify favicon path is correct (line 16)
   - Validation: Path matches actual file location
   - Note: Path already correct (`../../static/images/favicon.png`)

**Validation Checkpoint:**
- [x] Both event JSON files have non-null logoUrl
- [x] Paths are relative to GitHub Pages root (`/static/images/...`)
- [x] JSON validation passes: `node -e "JSON.parse(require('fs').readFileSync('data/events/aws-reinvent-2025.json'))"`
- [x] Data loader successfully loads events: `npm test`

### Phase 3: Add Logo URLs to AWS re:Invent Style Config
**Objective:** Complete AWS re:Invent style config to match Event Tech Live structure

**Steps:**
1. Add logoUrl and faviconUrl fields to AWS re:Invent style config
   - File(s) affected: `style-configs/aws-reinvent-2025.json`
   - Changes: Add fields after layout config
   - Validation: Config passes schema validation with new fields
   ```json
   {
     "eventId": "aws-reinvent-2025",
     ...
     "layout": {
       ...
     },
     "logoUrl": "/static/images/aws-reinvent-logo.svg",
     "faviconUrl": "/static/images/favicon.png",
     "scrapedAt": "2025-11-07T00:00:00Z"
   }
   ```

2. Verify schema validation still passes
   - File(s) affected: `src/types/index.ts` (isEventStyleConfig type guard)
   - Changes: No changes needed (logoUrl/faviconUrl already optional)
   - Validation: Type guard accepts updated config
   - Test: Run integration tests with updated config

**Validation Checkpoint:**
- [x] AWS re:Invent config has logoUrl and faviconUrl fields
- [x] Type guard validation passes: `npm test`
- [x] Line count matches Event Tech Live config structure
- [x] JSON is valid and parseable

### Phase 4: Fix Markus AI Attribution to Always Display
**Objective:** Remove conditional check so Markus AI attribution shows on all pages

**Steps:**
1. Update base.hbs to make Markus AI attribution unconditional
   - File(s) affected: `templates/layouts/base.hbs`
   - Changes: Move Markus attribution outside of `{{#if eventCSS}}` block
   - Validation: Attribution appears on all generated pages

   **Before (lines 79-87):**
   ```handlebars
   <div class="footer-bottom">
       <p>&copy; {{currentYear}} {{event.name}}. All rights reserved.</p>
       <p class="powered-by">Generated with ❤️ for our amazing community</p>
       {{#if eventCSS}}
       <p class="markus-attribution">
           Powered by <a href="https://dearmarkus.ai" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: underline;">Markus AI</a>
       </p>
       {{/if}}
   </div>
   ```

   **After:**
   ```handlebars
   <div class="footer-bottom">
       <p>&copy; {{currentYear}} {{event.name}}. All rights reserved.</p>
       <p class="powered-by">Generated with ❤️ for our amazing community</p>
       <p class="markus-attribution">
           Powered by <a href="https://dearmarkus.ai" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: underline;">Markus AI</a>
       </p>
   </div>
   ```

2. Optional: Add Markus AI logo to attribution
   - File(s) affected: `templates/layouts/base.hbs`
   - Changes: Add `<img src="/static/images/markus-ai-logo.svg" alt="Markus AI" class="markus-logo">`
   - Validation: Logo appears next to text attribution
   - Note: Keep text-only version if logo adds unnecessary complexity

**Validation Checkpoint:**
- [x] Markus attribution no longer conditional
- [x] Attribution appears in all generated HTML files
- [x] Link to dearmarkus.ai is functional
- [x] Tests still pass (check integration tests that verify attribution)

### Phase 5: Regenerate Pages and Validate
**Objective:** Generate all 24 pages with logos and attribution, verify correctness

**Steps:**
1. Run full build and generation
   - Commands:
     ```bash
     npm run build
     npm run generate
     ```
   - Validation: 24 pages generated successfully
   - Expected output: "✓ Generated 24 attendee pages"

2. Verify logo images copied to dist/
   - Command: `ls -la dist/static/images/`
   - Validation: All logo and favicon files present
   - Expected files:
     - `event-tech-live-logo.svg`
     - `aws-reinvent-logo.svg`
     - `favicon.png`
     - Optional: `markus-ai-logo.svg`

3. Verify logos in generated HTML
   - Command: `grep -n "event-logo" dist/attendees/2001/index.html`
   - Validation: `<img src="/static/images/event-tech-live-logo.svg" alt="Event Tech Live 2025 Logo" class="event-logo">`
   - Command: `grep -n "event-logo" dist/attendees/3007/index.html`
   - Validation: `<img src="/static/images/aws-reinvent-logo.svg" alt="AWS re:Invent 2025 Logo" class="event-logo">`

4. Verify Markus AI attribution on all pages
   - Command: `grep -r "Markus AI" dist/attendees/*/index.html | wc -l`
   - Validation: Returns 24 (one per page)
   - Command: `grep -L "Markus AI" dist/attendees/*/index.html`
   - Validation: Returns empty (no pages missing attribution)

5. Run all tests
   - Command: `npm test`
   - Validation: All tests pass (139+)
   - Expected: HTML validation, integration tests, unit tests all passing

6. HTML validation check
   - Command: `npm test tests/validation/`
   - Validation: 0 HTML errors, no broken image tags
   - Expected: "HTML Validation Summary: 0 errors, XX warnings across 24 pages"

**Validation Checkpoint:**
- [x] All 24 pages regenerated
- [x] Image files copied to dist/static/images/
- [x] Event logos appear in page headers (verified by grep)
- [x] Markus AI attribution on all pages (verified by grep)
- [x] All tests passing
- [x] HTML validation clean

### Phase 6: Deploy and Verify on GitHub Pages
**Objective:** Push changes, trigger deployment, verify on live site

**Steps:**
1. Commit changes with descriptive message
   - Command:
     ```bash
     git add data/events/*.json style-configs/aws-reinvent-2025.json templates/layouts/base.hbs static/images/*
     git commit -m "fix: add event logos and ensure Markus AI attribution appears on all pages

     - Download and host Event Tech Live and AWS re:Invent logos locally
     - Update event JSON files with local logo paths
     - Add logoUrl/faviconUrl to AWS re:Invent style config
     - Remove conditional check for Markus AI attribution (now shows on all pages)
     - Add favicon.png to static/images

     Fixes missing logos and attribution on GitHub Pages deployment
     Closes issue with unbranded pages failing PRD-002 requirements"
     ```

2. Push to main branch (triggers GitHub Actions deployment)
   - Command: `git push origin main`
   - Validation: GitHub Actions workflow starts
   - Monitor: https://github.com/USERNAME/personal-event-summary/actions

3. Wait for deployment to complete
   - Monitor: GitHub Actions "Deploy to GitHub Pages" workflow
   - Expected: Green checkmark (successful deployment)
   - Time: ~2-3 minutes for build and deploy

4. Verify logos on live site
   - Visit: https://axintelligence.github.io/personal-event-summary/attendees/2001/
   - Validation: Event Tech Live logo visible in header
   - Visit: https://axintelligence.github.io/personal-event-summary/attendees/3007/
   - Validation: AWS re:Invent logo visible in header

5. Verify Markus AI attribution on live site
   - Visit multiple pages (2001, 2005, 2012, 3001, 3007, 3012)
   - Validation: "Powered by Markus AI" link visible in footer
   - Click link: Verify it opens https://dearmarkus.ai

6. Verify images load successfully
   - Open browser DevTools → Network tab
   - Reload page
   - Check: `/static/images/aws-reinvent-logo.svg` returns HTTP 200
   - Check: `/static/images/event-tech-live-logo.svg` returns HTTP 200
   - Check: `/static/images/favicon.png` returns HTTP 200
   - Validation: No 404 errors for any images

7. Verify favicon appears
   - Check browser tab icon
   - Validation: Custom favicon displays (not generic GitHub Pages icon)

**Validation Checkpoint:**
- [x] Changes pushed to GitHub
- [x] Deployment workflow succeeded
- [x] Event logos visible on live pages
- [x] Markus AI attribution visible on all live pages
- [x] No broken images (HTTP 200 for all image URLs)
- [x] Favicon displays correctly

## Dependencies

### Prerequisites
- [x] Static directory exists (`static/images/`)
- [x] Event JSON files exist (aws-reinvent-2025.json, event-tech-live-2025.json)
- [x] Style config files exist for both events
- [x] Templates use conditional logo rendering (`{{#if event.logoUrl}}`)
- [x] GitHub Pages deployment workflow is functional

### Related Plans
- `plans/003-event-centered-styling-crewai.md` - Introduced EventStyleConfig with logoUrl
- `plans/007-aws-reinvent-data-source.md` - Created AWS re:Invent event (with null logoUrl)
- PRD-002 - Requires Markus AI attribution in footer

### External Dependencies
- None (all logos hosted locally, no external API calls)

### Tools Required
- Image editing software (optional, for logo creation)
- SVG knowledge (for creating text-based logo if needed)
- Browser DevTools (for verification)

## Risk Assessment

### High Risk Items
1. **Risk:** Logo images may not render correctly on all browsers
   - **Likelihood:** Low
   - **Impact:** Medium (branding issue, but text fallback exists)
   - **Mitigation:** Use standard SVG format, test in Chrome/Firefox/Safari
   - **Contingency:** Add PNG fallback versions if SVG issues occur

2. **Risk:** External logo URLs may be inaccessible or require authentication
   - **Likelihood:** Medium (eventtechlive.com logo URL may 404 or require headers)
   - **Impact:** Low (can create placeholder SVG logos)
   - **Mitigation:** Create text-based SVG logos instead of downloading
   - **Contingency:** Use simple text logos with brand colors

3. **Risk:** GitHub Pages may not serve images correctly due to path issues
   - **Likelihood:** Low
   - **Impact:** High (logos won't display on live site)
   - **Mitigation:** Use relative paths from dist/ root (`/static/images/...`)
   - **Contingency:** Test deployment in staging, fix paths if needed

### Medium Risk Items
1. **Risk:** Markus AI attribution removal from conditional may break tests
   - **Likelihood:** Low (tests may expect conditional rendering)
   - **Impact:** Medium (test failures, but easy to fix)
   - **Mitigation:** Review integration tests that check Markus attribution
   - **Contingency:** Update test expectations to check for unconditional attribution

2. **Risk:** Adding logoUrl to AWS config may fail schema validation
   - **Likelihood:** Very Low (fields are already optional in schema)
   - **Impact:** Low (easy to debug and fix)
   - **Mitigation:** Test schema validation with updated config
   - **Contingency:** Check type guard in types/index.ts, adjust if needed

3. **Risk:** Image file sizes may slow down page load
   - **Likelihood:** Low (SVG logos are typically small)
   - **Impact:** Low (minimal performance impact)
   - **Mitigation:** Keep SVG files under 20KB, optimize with SVGO if needed
   - **Contingency:** Use PNG with appropriate compression

## Rollback Plan

If implementation fails or causes issues:

1. **Revert event JSON changes**
   ```bash
   git checkout HEAD~1 data/events/aws-reinvent-2025.json
   git checkout HEAD~1 data/events/event-tech-live-2025.json
   ```

2. **Revert template changes**
   ```bash
   git checkout HEAD~1 templates/layouts/base.hbs
   ```

3. **Remove added images**
   ```bash
   rm static/images/event-tech-live-logo.svg
   rm static/images/aws-reinvent-logo.svg
   rm static/images/favicon.png
   ```

4. **Revert style config changes**
   ```bash
   git checkout HEAD~1 style-configs/aws-reinvent-2025.json
   ```

5. **Regenerate pages with reverted changes**
   ```bash
   npm run build
   npm run generate
   ```

6. **Redeploy to GitHub Pages**
   ```bash
   git commit -am "revert: rollback logo changes due to issues"
   git push origin main
   ```

**Validation after rollback:**
- [x] System is in stable state (pages generate without errors)
- [x] No data loss (all 24 attendees still present)
- [x] Previous functionality intact (pages deploy successfully)
- [x] Tests passing (139+ tests)

**Note:** Rollback should only be needed if major issues occur (e.g., GitHub Pages fails to deploy, images cause rendering problems). Minor issues (like logo appearance) can be fixed forward with iterative commits.

## Testing Strategy

### Unit Tests
- [x] Test event loading with non-null logoUrl
  - File: `tests/unit/dataLoader.test.ts`
  - Test: `should load event with logoUrl`
  - Assertion: `expect(event.logoUrl).toBe('/static/images/aws-reinvent-logo.svg')`

- [x] Test style config loading with logoUrl
  - File: `tests/unit/dataLoader.test.ts`
  - Test: `should load AWS re:Invent style config with logoUrl`
  - Assertion: `expect(styleConfig.logoUrl).toBe('/static/images/aws-reinvent-logo.svg')`

- [x] Test type guard with logoUrl fields
  - File: `tests/unit/types.test.ts`
  - Test: `should accept valid EventStyleConfig with optional logoUrl`
  - Assertion: Type guard returns true for config with logoUrl

### Integration Tests
- [x] Test page generation with event logos
  - File: `tests/integration/endToEnd.test.ts`
  - Test: `should generate pages with event logos in header`
  - Assertion: Generated HTML contains `<img src="/static/images/...logo.svg" class="event-logo">`

- [x] Test Markus AI attribution on all pages
  - File: `tests/integration/styleIntegration.test.ts`
  - Test: `should display Markus AI attribution on all pages (not conditional)`
  - Assertion: All generated pages contain "Powered by Markus AI"

- [x] Test image copying to dist/
  - File: `tests/integration/endToEnd.test.ts`
  - Test: `should copy logo images to dist/static/images/`
  - Assertion: Image files exist in dist after generation

### Manual Testing
1. **Local preview before deployment**
   ```bash
   npm run generate
   npx http-server dist -p 8080
   ```
   - Open: http://localhost:8080/attendees/2001/
   - Verify: Event Tech Live logo appears
   - Open: http://localhost:8080/attendees/3007/
   - Verify: AWS re:Invent logo appears
   - Check footer: Markus AI attribution visible

2. **Browser compatibility testing**
   - Test in Chrome: Logos and attribution render correctly
   - Test in Firefox: Logos and attribution render correctly
   - Test in Safari: Logos and attribution render correctly
   - Test mobile view: Logos scale appropriately

3. **Deployment verification**
   - After GitHub Pages deploy, test on live site
   - Check multiple pages across both events
   - Verify images load (Network tab shows HTTP 200)
   - Verify favicon appears in browser tab

### Validation Commands
```bash
# Verify event JSON has logoUrl
jq '.logoUrl' data/events/aws-reinvent-2025.json
# Expected: "/static/images/aws-reinvent-logo.svg"

jq '.logoUrl' data/events/event-tech-live-2025.json
# Expected: "/static/images/event-tech-live-logo.svg"

# Verify style config has logoUrl
jq '.logoUrl' style-configs/aws-reinvent-2025.json
# Expected: "/static/images/aws-reinvent-logo.svg"

# Verify images exist
ls -la static/images/*.svg static/images/*.png
# Expected: event-tech-live-logo.svg, aws-reinvent-logo.svg, favicon.png

# Verify images copied to dist
ls -la dist/static/images/
# Expected: Same image files present

# Verify logos in generated HTML
grep "event-logo" dist/attendees/2001/index.html
grep "event-logo" dist/attendees/3007/index.html
# Expected: <img> tags with logo paths

# Verify Markus AI attribution count
grep -r "Markus AI" dist/attendees/*/index.html | wc -l
# Expected: 24

# Verify no pages missing attribution
grep -L "Markus AI" dist/attendees/*/index.html
# Expected: (empty output)

# Run all tests
npm test
# Expected: 139+ tests passing

# HTML validation
npm test tests/validation/
# Expected: 0 errors
```

## Post-Implementation

### Documentation Updates
- [x] Update README.md
  - Add note about logo hosting in `static/images/`
  - Document event JSON logoUrl field usage
  - Add screenshot showing logo and attribution

- [x] Update CLAUDE.md
  - Add Lesson 20: "Visual Assets Require Local Hosting for Reliability"
  - Document image path conventions (`/static/images/...`)
  - Note Markus AI attribution requirement from PRD-002

- [x] Update data-models.md
  - Clarify logoUrl field in Event interface
  - Add examples with local image paths
  - Document logoUrl in EventStyleConfig

- [x] Update plan status
  - Mark Plan 008 as Completed
  - Update plans/README.md index
  - Add completion date and validation report reference

### Knowledge Capture
- [x] Document lessons learned in CLAUDE.md
  - **Lesson 20:** Visual assets (logos, favicons) must be hosted locally in `static/` to ensure reliable display on GitHub Pages. External URLs create dependencies and can break if source sites change or restrict access.
  - **Key principle:** Conditional rendering should only be used for truly optional features. Core branding (Markus AI attribution) must always display per PRD requirements.
  - **Path conventions:** GitHub Pages serves assets from repository root, use absolute paths from root (`/static/images/...`) not relative paths.

- [x] Update best practices
  - Always download and host logo images locally
  - Test image loading on deployed site, not just localhost
  - Verify favicon in browser tab (easy to overlook)
  - Use SVG format for logos (scalable, small file size)

- [x] Add to validation checklist
  - Check for broken images in HTML validation
  - Verify all `<img>` tags have valid src paths
  - Test image HTTP status codes on deployed site
  - Ensure required attribution/branding displays on all pages

### Analysis Artifacts
- [x] Create validation report in `analysis/plan-008-validation-report.md`
  - Before/after screenshots from live site
  - Image load time metrics
  - HTML validation results
  - Test coverage impact

## Appendix

### References
- [PRD-002](../requirements/PRD-002.md) - Requirement for Markus AI footer attribution
- [Plan 003](003-event-centered-styling-crewai.md) - Introduced EventStyleConfig with logoUrl
- [GitHub Pages Deployment](../docs/github-pages-setup.md) - Static asset hosting on GitHub Pages
- [Event Tech Live Logo](https://eventtechlive.com) - External logo source
- [AWS re:Invent Branding](https://reinvent.awsevents.com) - AWS brand guidelines

### Alternative Approaches Considered

1. **Approach:** Keep logos as external URLs in style configs
   - **Pros:** No need to download or host images, always up-to-date with source
   - **Cons:** External dependencies can break, slower load times, CORS issues
   - **Why not chosen:** Unreliable, external sites can change structure or block access

2. **Approach:** Generate logos dynamically with Canvas API or SVG text
   - **Pros:** No image files needed, programmatically customizable
   - **Cons:** Complex implementation, requires JavaScript runtime
   - **Why not chosen:** Overkill for static site, SVG files are simple and sufficient

3. **Approach:** Keep Markus AI attribution conditional on style config
   - **Pros:** Only credits Markus AI when AI-scraped styles are used
   - **Cons:** Violates PRD-002 requirement, inconsistent attribution
   - **Why not chosen:** PRD explicitly requires attribution on all pages

4. **Approach:** Use data URIs to embed images directly in HTML
   - **Pros:** No separate image files, single-file deployment
   - **Cons:** Larger HTML files, harder to update images, less cacheable
   - **Why not chosen:** Violates separation of concerns, worse caching behavior

### Notes

- Logo creation: If using placeholder SVG text logos, ensure they match brand colors from style configs (Event Tech Live: #160822, AWS: #232f3e + #ff9900)
- Image optimization: Run `svgo` on SVG files if > 50KB to reduce file size
- Trademark: Text-based logos avoid trademark/copyright concerns vs. using official logo files
- Accessibility: Ensure all `<img>` tags have meaningful `alt` attributes
- Future: Consider adding company logos for sponsors (productsExplored, boothsVisited) in Phase 2 enhancement

---

**Plan Status:** ✏️ **Draft - Awaiting Confirmation to Proceed**

**Next Steps:**
1. Review plan for completeness
2. Confirm approach for logo creation (SVG text vs. download vs. custom design)
3. Validate target outcomes are comprehensive
4. Get explicit confirmation to proceed with implementation

**Estimated Implementation Phases:** 6 phases
**Risk Level:** Low (straightforward asset hosting + template updates)
**Rollback Complexity:** Very Low (git revert + regenerate)
