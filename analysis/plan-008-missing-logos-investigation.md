# Plan 008: Missing Logos Investigation Report

**Date:** 2025-11-07
**Investigation Method:** Code inspection, live site verification, WebFetch analysis
**Issue:** Event logos and Markus AI attribution not appearing on GitHub Pages

## Executive Summary

Event logos for AWS re:Invent and Event Tech Live are not displaying on the deployed GitHub Pages site (https://axintelligence.github.io/personal-event-summary/), and the Markus AI attribution footer is missing. Investigation reveals three root causes that require coordinated fixes.

## Issue Details

### Reported Problems
1. **AWS re:Invent logo** not visible on pages 3001-3012
2. **Event Tech Live logo** not visible on pages 2001-2012
3. **Markus AI logo/attribution** not appearing in footer
4. **User report:** https://axintelligence.github.io/personal-event-summary/attendees/3007/

### WebFetch Verification
Live site inspection confirms:
- No actual images present in HTML
- No broken image tags detected (images simply not rendered)
- Markus AI mentioned in attribution text at bottom, but no logo shown
- AWS re:Invent logo not visually represented
- Page appears text-only without visual branding

## Root Cause Analysis

### Root Cause 1: Event JSON Files Have Null logoUrl

**Evidence:**
```json
// data/events/aws-reinvent-2025.json
{
  "id": "aws-reinvent-2025",
  "name": "AWS re:Invent 2025",
  ...
  "logoUrl": null  // ❌ NULL VALUE
}

// data/events/event-tech-live-2025.json
{
  "id": "event-tech-live-2025",
  "name": "Event Tech Live 2025",
  ...
  "logoUrl": null  // ❌ NULL VALUE
}
```

**Template Logic:**
```handlebars
<!-- templates/layouts/base.hbs line 38 -->
{{#if event.logoUrl}}
<img src="{{event.logoUrl}}" alt="{{event.name}} Logo" class="event-logo">
{{else}}
<h1 class="event-name">{{event.name}}</h1>
{{/if}}
```

**Impact:** Since `event.logoUrl` is null, the `{{#if}}` check fails and only the text `<h1>` tag is rendered. No logo image appears.

### Root Cause 2: AWS re:Invent Style Config Missing Logo Fields

**Evidence:**
```bash
$ wc -l style-configs/*.json
  45 style-configs/event-tech-live-2025.json
  31 style-configs/aws-reinvent-2025.json  # ❌ 14 lines shorter
```

**Event Tech Live config (COMPLETE):**
```json
{
  "eventId": "event-tech-live-2025",
  ...
  "layout": { ... },
  "logoUrl": "https://eventtechlive.com/wp-content/themes/eventtechlive/assets/images/logo.svg",
  "faviconUrl": "https://eventtechlive.com/wp-content/uploads/2022/03/favicon.ico",
  "scrapedAt": "2024-06-08T00:00:00Z"
}
```

**AWS re:Invent config (INCOMPLETE):**
```json
{
  "eventId": "aws-reinvent-2025",
  ...
  "layout": {
    "gridSystem": "grid",
    "spacingUnit": "8px",
    "borderRadius": "2px",
    "containerWidth": "1280px"
  }
  // ❌ NO logoUrl field
  // ❌ NO faviconUrl field
  // ❌ NO scrapedAt field
}
```

**Impact:** Even if the style config logoUrl was used by templates (it's not), AWS re:Invent wouldn't have logo data.

### Root Cause 3: Markus AI Attribution is Conditional on eventCSS

**Evidence:**
```handlebars
<!-- templates/layouts/base.hbs lines 82-86 -->
<div class="footer-bottom">
    <p>&copy; {{currentYear}} {{event.name}}. All rights reserved.</p>
    <p class="powered-by">Generated with ❤️ for our amazing community</p>
    {{#if eventCSS}}  <!-- ❌ CONDITIONAL CHECK -->
    <p class="markus-attribution">
        Powered by <a href="https://dearmarkus.ai" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: underline;">Markus AI</a>
    </p>
    {{/if}}
</div>
```

**Logic Flow:**
1. `generate.ts` loads style config: `const styleConfig = await loadStyleConfig(event.id);`
2. Generates CSS: `const eventCSS = styleConfig ? generateEventCSS(styleConfig) : null;`
3. Passes to template: `eventCSS` is either CSS string or null
4. Template checks: `{{#if eventCSS}}`
5. If null or empty → No Markus AI attribution rendered

**Impact:** If CSS generation fails silently or style config is missing, Markus AI attribution disappears. This violates PRD-002 requirement: "In the footer let's call out that this system is powered by Markus ai"

### Root Cause 4: No Image Files in static/images/

**Evidence:**
```bash
$ ls -la static/images/
total 0
drwxr-xr-x  2 carlos.cubas  staff   64 Nov  5 23:33 .
drwxr-xr-x  4 carlos.cubas  staff  128 Nov  5 23:33 ..

# ❌ Directory is EMPTY
```

**Expected Files (not present):**
- `event-tech-live-logo.svg` or `.png`
- `aws-reinvent-logo.svg` or `.png`
- `favicon.png` (referenced in base.hbs line 16)
- `markus-ai-logo.svg` (optional)

**Impact:** Even if event JSON had logoUrl pointing to local paths, the actual image files don't exist.

### Root Cause 5: Style Config Logos Not Passed to Event Object

**Architecture Issue:**

```typescript
// src/generate.ts line 86-89
const render = async (attendee: Attendee, event: Event) => {
    // Load style config if available (Plan 003)
    const styleConfig = await loadStyleConfig(event.id);
    const eventCSS = styleConfig ? generateEventCSS(styleConfig) : null;

    // First render the attendee page content
    const pageContent = attendeeTemplate({ attendee, event });  // ❌ event passed as-is

    // Then render the full page with layout
    const fullPageTemplate = hbs.compile(baseLayout);
    return fullPageTemplate({
        body: pageContent,
        attendee,
        event,  // ❌ Still has null logoUrl
        eventCSS,  // ✅ CSS is passed
        pageTitle: `${attendee.firstName} ${attendee.lastName} - ${event.name}`,
        description: `${attendee.firstName}'s personalized ${event.name} experience summary`
    });
};
```

**Problem:** Style config has `logoUrl` but it's never merged into the `event` object that gets passed to the template. The template checks `event.logoUrl` which is from the event JSON (null), not the style config.

**Impact:** Two separate data sources (event JSON, style config) both have logoUrl fields, but they're not coordinated. Template uses event.logoUrl (null) while style config logoUrl (external URL) is ignored.

## Validation Data

### Live Site Verification
- **URL Tested:** https://axintelligence.github.io/personal-event-summary/attendees/3007/
- **Attendee:** Sarah Johnson (AWS re:Invent, ID 3007)
- **Expected:** AWS re:Invent logo in header, Markus AI attribution in footer
- **Actual:** Text-only header "AWS re:Invent 2025", no Markus AI attribution visible
- **Favicon:** Generic GitHub Pages icon (custom favicon.png doesn't exist)

### Code Grep Results
```bash
# Event JSON logoUrl values
$ jq '.logoUrl' data/events/*.json
null
null

# Style config logoUrl values
$ jq '.logoUrl' style-configs/event-tech-live-2025.json
"https://eventtechlive.com/wp-content/themes/eventtechlive/assets/images/logo.svg"

$ jq '.logoUrl' style-configs/aws-reinvent-2025.json
(no such field - jq returns null)

# Image files in static
$ ls static/images/
(empty)

# Markus AI attribution in template
$ grep -n "markus-attribution" templates/layouts/base.hbs
83:                <p class="markus-attribution">
```

## Reproduction Steps

1. **Clone repository and generate locally:**
   ```bash
   git clone https://github.com/axintelligence/personal-event-summary.git
   cd personal-event-summary
   npm install
   npm run generate
   ```

2. **Inspect generated HTML:**
   ```bash
   # Check for event logo
   grep "event-logo" dist/attendees/3007/index.html
   # Result: (no matches - logo not rendered)

   # Check for Markus AI attribution
   grep "Markus AI" dist/attendees/3007/index.html
   # Result: (no matches - attribution not rendered)
   ```

3. **Serve locally and verify visually:**
   ```bash
   npx http-server dist -p 8080
   # Open: http://localhost:8080/attendees/3007/
   # Observe: Text-only header, no logo, no Markus AI footer
   ```

4. **Deploy to GitHub Pages reproduces issue:**
   - Push to main branch triggers deployment
   - Live site shows same missing logos/attribution
   - Confirms issue is in data/templates, not hosting

## Solution Design

### Fix Strategy

**Phase 1: Host Images Locally**
- Create SVG logo files for both events
- Add favicon.png
- Store in `static/images/` directory
- Ensures reliability, no external dependencies

**Phase 2: Update Event JSON**
- Set `logoUrl: "/static/images/event-tech-live-logo.svg"` in event-tech-live-2025.json
- Set `logoUrl: "/static/images/aws-reinvent-logo.svg"` in aws-reinvent-2025.json
- Paths are relative to GitHub Pages root

**Phase 3: Complete AWS re:Invent Style Config**
- Add `"logoUrl": "/static/images/aws-reinvent-logo.svg"`
- Add `"faviconUrl": "/static/images/favicon.png"`
- Add `"scrapedAt": "2025-11-07T00:00:00Z"`
- Matches Event Tech Live config structure

**Phase 4: Fix Markus AI Attribution**
- Remove `{{#if eventCSS}}` conditional wrapper
- Make attribution unconditional (PRD-002 requirement)
- Optionally add Markus AI logo to attribution

**Phase 5: Regenerate and Validate**
- Run `npm run generate`
- Verify logos in generated HTML
- Verify Markus AI attribution on all 24 pages
- Deploy and test on GitHub Pages

### Why This Approach?

**Local Hosting Benefits:**
- No external dependencies (eventtechlive.com can change)
- Faster load times (served from same domain)
- No CORS issues
- Reliable (GitHub Pages controls hosting)

**Event JSON vs Style Config:**
- Event JSON is authoritative for event data
- Style config supplements with visual customization
- Template uses event.logoUrl (correct pattern)
- Solution: Update event JSON, not template logic

**Unconditional Markus AI:**
- PRD-002 explicitly requires attribution on all pages
- Conditional rendering violates requirement
- Simple fix: Remove `{{#if eventCSS}}` wrapper

## Test Impact

**Affected Tests:**
- Integration tests may expect Markus AI conditional on eventCSS
- HTML validation will now check for logo `<img>` tags
- Image file existence tests needed

**Required Test Updates:**
```typescript
// tests/integration/styleIntegration.test.ts
// BEFORE:
it('should display Markus AI attribution when style config present', ...)

// AFTER:
it('should always display Markus AI attribution on all pages', ...)
```

## Risk Assessment

**Low Risk:**
- Changes are straightforward (add images, update JSON, remove conditional)
- No breaking changes to API or data model
- Easy rollback (git revert + regenerate)

**Validation:**
- Visual inspection on deployed site (can't miss logos)
- Automated tests will catch broken image paths
- HTML validation prevents broken `<img>` tags

## References

- **Live Issue:** https://axintelligence.github.io/personal-event-summary/attendees/3007/
- **PRD-002:** Requirements for Markus AI attribution
- **Plan 003:** Introduced EventStyleConfig with logoUrl
- **Plan 007:** Created AWS re:Invent event (with null logoUrl)
- **Template:** `templates/layouts/base.hbs` lines 38-42 (logo), 82-86 (attribution)

---

**Investigation Complete:** 2025-11-07
**Root Causes Identified:** 5 (null logoUrl, incomplete config, conditional attribution, no image files, data not merged)
**Solution Complexity:** Low (6 phases, straightforward implementation)
**Next Step:** Review Plan 008 and proceed with implementation
