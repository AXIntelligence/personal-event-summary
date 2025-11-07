# Plan 007: AWS re:Invent Data Source Integration

**Status:** Draft
**Created:** 2025-11-07
**Last Updated:** 2025-11-07
**Priority:** 🟡 High

## Overview

This plan implements PRD-003, replacing the generic "TechConf 2025" data source with AWS re:Invent as a high-quality, real-world event example. This involves scraping https://reinvent.awsevents.com/ for authentic branding, creating 12 believable attendee profiles with AWS-themed sessions and connections, and removing the old generic event data.

The AWS re:Invent integration will: (1) demonstrate the system's capability to handle complex, enterprise-scale event websites, (2) provide a recognizable, professional reference implementation for potential clients, and (3) showcase realistic cloud/AWS-focused session content and networking patterns. This replacement eliminates the generic "TechConf" placeholder and establishes re:Invent alongside Event Tech Live as the two production-quality data sources.

Per the exploration report (2025-11-07), the system has 95% compatibility with AWS re:Invent due to Playwright's JavaScript rendering capabilities. The scraper successfully handles React-based sites, waits for network idle, and extracts computed styles identical to DevTools measurements.

## Target Outcomes

### Primary Outcomes

1. **AWS re:Invent Scraped Successfully**: EventStyleConfig JSON generated with authentic AWS branding (black #000000, orange #ff9900, Amazon Ember font)
2. **12 Believable Attendees Created**: Personas spanning cloud architects, DevOps engineers, startup founders, enterprise CTOs with 8-15 sessions each
3. **Realistic Session Content**: 60+ unique AWS sessions covering compute, AI/ML, serverless, containers, security, databases, and keynotes
4. **Authentic Connections**: 150+ networking connections referencing real AWS services, partner companies, and realistic job titles
5. **TechConf 2025 Removed**: Generic event-2025.json and attendees 1001-1012 deleted, reducing data source to two high-quality events

### Success Criteria

- [ ] Scraped config `style-configs/aws-reinvent-2025.json` passes schema validation (all required fields present, colors in #RRGGBB format)
- [ ] Scraped colors validated against DevTools inspection (±2 RGB tolerance for header background)
- [ ] Event JSON file `data/events/aws-reinvent-2025.json` created with accurate details (dates, location, scale)
- [ ] 12 attendee files created (3001-3012) with unique personas and engagement patterns
- [ ] All 60+ sessions have realistic titles, descriptions, and AWS service mentions
- [ ] Session tracks include: Compute, AI/ML, Serverless, Containers, Security, Database, Keynotes (7+ tracks)
- [ ] Connections reference believable AWS ecosystem companies (partners, consulting firms, AWS itself)
- [ ] Generated pages for attendees 3001-3012 pass HTML validation (0 errors)
- [ ] Old event-2025.json and attendees 1001-1012 deleted from repository
- [ ] All 139 tests passing after removal (updated fixtures if needed)
- [ ] Test coverage remains ≥89% after changes
- [ ] README.md updated to reference AWS re:Invent (not TechConf 2025)

### Validation Strategy

#### Empirical Validation Methods

**Method 1: Scraper Output Validation**
- **Tools/Commands:**
  ```bash
  # Scrape AWS re:Invent with extended timeout
  python -m event_style_scraper scrape \
    --url https://reinvent.awsevents.com/ \
    --timeout 90 \
    --output style-configs/aws-reinvent-2025.json

  # Validate JSON schema
  python -c "import json; config = json.load(open('style-configs/aws-reinvent-2025.json')); \
    assert config['eventId'] == 'aws-reinvent-2025'; \
    assert config['colors']['primary'].startswith('#'); \
    print('✓ Schema valid')"

  # Validate colors against DevTools
  python scripts/validate_scraped_colors.py \
    --url https://reinvent.awsevents.com/ \
    --config style-configs/aws-reinvent-2025.json \
    --selector header \
    --property backgroundColor \
    --expected "#000000"  # AWS black header
  ```
- **Expected Results:** Config file created, schema valid, colors match DevTools (±2 RGB), Amazon Ember font detected
- **Acceptance Threshold:** 100% schema compliance, colors within ±2 RGB units of DevTools measurement

**Method 2: Data Quality Validation**
- **Tools/Commands:**
  ```bash
  # Validate all attendee files load successfully
  node -e "
    const { loadAllAttendees } = require('./dist/dataLoader.js');
    loadAllAttendees().then(attendees => {
      const reinventAttendees = attendees.filter(a => a.eventId === 'aws-reinvent-2025');
      console.log('re:Invent attendees:', reinventAttendees.length);
      console.log('Total sessions:', reinventAttendees.reduce((sum, a) => sum + a.sessions.length, 0));
      console.log('Total connections:', reinventAttendees.reduce((sum, a) => sum + a.connections.length, 0));
      if (reinventAttendees.length !== 12) throw new Error('Expected 12 attendees');
    });
  "

  # Check for AWS service mentions in sessions
  grep -r "Lambda\|EC2\|S3\|SageMaker\|EKS\|DynamoDB" data/attendees/30*.json | wc -l
  # Expected: 40+ mentions (AWS services in session titles/descriptions)

  # Validate session diversity (multiple tracks)
  jq -r '.sessions[].track' data/attendees/3001.json | sort -u | wc -l
  # Expected: 4-6 unique tracks per attendee

  # Check connection realism (company diversity)
  jq -r '.connections[].company' data/attendees/30*.json | sort -u | wc -l
  # Expected: 60+ unique companies
  ```
- **Expected Results:** 12 attendees loaded, 100-150 total sessions, 150-200 total connections, 40+ AWS service mentions, 60+ unique companies
- **Acceptance Threshold:** ≥12 attendees, ≥90 sessions, ≥120 connections, ≥30 AWS service mentions

**Method 3: Page Generation and Validation**
- **Tools/Commands:**
  ```bash
  # Generate all pages (should now be 24 total: 12 Event Tech Live + 12 re:Invent)
  npm run generate

  # Verify re:Invent pages exist
  ls dist/attendees/30*/index.html | wc -l
  # Expected: 12

  # Validate HTML
  npm test -- tests/validation/htmlValidation.test.ts

  # Check AWS branding applied (black/orange colors)
  grep -E "color-primary.*#000000|#232f3e" dist/attendees/3001/index.html
  # Expected: AWS black or dark blue

  # Verify page contains AWS-specific content
  grep -i "reinvent\|AWS\|Amazon" dist/attendees/3001/index.html | wc -l
  # Expected: 15+ mentions
  ```
- **Expected Results:** 24 total pages generated, HTML validation 0 errors, AWS colors present, AWS/re:Invent mentioned 15+ times per page
- **Acceptance Threshold:** 100% page generation success, 0 HTML errors, AWS branding visible

**Method 4: Test Suite Validation**
- **Tools/Commands:**
  ```bash
  # Run full test suite
  npm test

  # Check coverage
  npm run test:coverage

  # Verify no broken references to old event-2025
  grep -r "event-2025" tests/ data/ src/ templates/
  # Expected: 0 results (all references removed)

  # Verify new event referenced
  grep -r "aws-reinvent-2025" tests/ data/
  # Expected: 12+ results (attendee files + event file)
  ```
- **Expected Results:** 139 tests passing (or more if new tests added), coverage ≥89%, no references to old event, new event referenced throughout
- **Acceptance Threshold:** 100% test pass rate, coverage unchanged or improved, clean migration

---

## Hypothesis-Driven Approach

### Hypothesis 1: Playwright Can Scrape AWS re:Invent Without Bot Detection

**Reasoning:** AWS re:Invent website likely uses bot detection given AWS's security focus. However, Playwright with headless mode and proper user agent should pass basic checks. The site is publicly accessible marketing content, not protected resources.

**Validation Method:**
- **Experiment:** Run scraper with default Playwright configuration, observe for 403/blocking errors
- **Expected Outcome:** Scraper completes successfully, returns HTML content with "re:Invent" title, extracts header styles
- **Validation Steps:**
  1. Run: `python -m event_style_scraper scrape --url https://reinvent.awsevents.com/ --timeout 90`
  2. Check output for "success": true
  3. Verify HTML contains "<title>AWS re:Invent" or similar
  4. Check computed_styles has header backgroundColor
  5. Confirm no 403 or CAPTCHA responses in logs

**Success Criteria:**
- [ ] Scraper returns success: true
- [ ] HTML content length > 50,000 characters (not a minimal error page)
- [ ] "re:Invent" or "AWS" appears in extracted HTML title
- [ ] Header computed styles include backgroundColor property
- [ ] No "Access Denied" or "CAPTCHA" in response

**Failure Conditions:**
- HTTP 403/429 status codes
- HTML content < 10,000 characters (likely error page)
- CAPTCHA challenge detected
- **Fallback:** Use Playwright stealth mode, add realistic user agent, reduce request frequency

### Hypothesis 2: AWS re:Invent Primary Color is Black (#000000)

**Reasoning:** AWS brand guidelines consistently use black headers with orange accents. Exploration report predicts #000000 (black) for header, #ff9900 (AWS orange) for accent. This aligns with AWS corporate branding visible on aws.amazon.com.

**Validation Method:**
- **Experiment:** Use DevTools color picker on https://reinvent.awsevents.com/ header element
- **Expected Outcome:** Header background-color is #000000 (black) or #232f3e (AWS dark blue)
- **Validation Steps:**
  1. Open https://reinvent.awsevents.com/ in Chrome
  2. Right-click header element → Inspect
  3. Check Computed → background-color property
  4. Convert rgb() to hex if needed
  5. Compare against scraped config primary color

**Success Criteria:**
- [ ] DevTools shows header backgroundColor: rgb(0, 0, 0) = #000000 OR rgb(35, 47, 62) = #232f3e
- [ ] Scraped config colors.primary matches DevTools value (±2 RGB units)
- [ ] Accent color is #ff9900 (AWS orange) OR similar warm orange

**Failure Conditions:**
- Header color is white, gray, or non-AWS brand color
- Scraped color differs from DevTools by >5 RGB units
- **Fallback:** Manually correct scraped config to match DevTools measurement (per Lesson 18)

### Hypothesis 3: 12 Attendees with 8-15 Sessions Each Provides Realistic Engagement Range

**Reasoning:** AWS re:Invent is a massive conference (60,000+ attendees, 2,000+ sessions over 5 days). Attendees typically attend 8-15 sessions depending on role (hands-on builders vs. executives). This range creates diverse personas while remaining believable.

**Validation Method:**
- **Experiment:** Create attendee personas with varied engagement levels, validate against real conference attendance patterns
- **Expected Outcome:** Session counts feel realistic (not too low/high), connections correlate with session count
- **Validation Steps:**
  1. Define 6 persona types: Cloud Architect (high), DevOps Engineer (high), Startup Founder (medium), CTO (low), Solutions Architect (high), ML Engineer (high)
  2. Assign sessions: High=12-15, Medium=10-12, Low=8-10
  3. Create personas 3001-3002 (Cloud Architects), 3003-3004 (DevOps), 3005-3006 (Founders), 3007-3008 (CTOs), 3009-3010 (SAs), 3011-3012 (ML Engineers)
  4. Check distribution: Mean ~11 sessions, Range 8-15
  5. Verify connections scale with sessions (more sessions = more connections)

**Success Criteria:**
- [ ] Average sessions per attendee: 10-12
- [ ] Session count range: 8-15 (no outliers)
- [ ] Connections per attendee: 10-25 (correlates with session count)
- [ ] Each persona feels distinct (different tracks, companies, achievements)
- [ ] No duplicate session IDs across attendees (but overlap is fine)

**Failure Conditions:**
- Average sessions <8 or >16 (unrealistic)
- All attendees have same session count (lacks diversity)
- Connections don't correlate with engagement level
- **Fallback:** Adjust session counts per persona, ensure 20-30% session overlap for realism

### Hypothesis 4: Removing TechConf 2025 Won't Break Existing Tests

**Reasoning:** TechConf 2025 (event-2025) is used in some tests as fixture data. However, most tests use Event Tech Live (event-tech-live-2025) or dynamically generated test data. Test suite should pass with minor fixture updates.

**Validation Method:**
- **Experiment:** Delete event-2025.json and attendees 1001-1012, run tests, identify failures
- **Expected Outcome:** 0-10 tests fail due to missing fixtures, easily fixed by updating test data to use event-tech-live-2025 or aws-reinvent-2025
- **Validation Steps:**
  1. Run: `npm test` (baseline, all passing)
  2. Delete: `data/events/event-2025.json`, `data/attendees/100*.json`
  3. Run: `npm test` (identify failures)
  4. Update failing tests to use event-tech-live-2025 or aws-reinvent-2025
  5. Run: `npm test` (verify all passing again)

**Success Criteria:**
- [ ] ≤10 tests fail initially after deletion
- [ ] All failed tests are fixture-related (data loading, not logic)
- [ ] Updated tests pass without changing assertions (only data source)
- [ ] Test coverage remains ≥89% after updates

**Failure Conditions:**
- >20 tests fail (indicates tight coupling to TechConf data)
- Logic tests fail (not just fixture tests)
- Test coverage drops below 85%
- **Fallback:** Create minimal test-only fixtures in tests/ directory, update dataLoader to support test fixtures

---

## Implementation Details

### Phase 1: Scrape AWS re:Invent Website

**Objective:** Generate EventStyleConfig JSON with authentic AWS branding

**Steps:**

1. **Scrape website with extended timeout**
   - File affected: `style-configs/aws-reinvent-2025.json` (created)
   - Changes: Run scraper CLI command
   - Command:
     ```bash
     python -m event_style_scraper scrape \
       --url https://reinvent.awsevents.com/ \
       --timeout 90 \
       --output style-configs/aws-reinvent-2025.json
     ```
   - Validation: Check file created, no errors in output

2. **Validate scraped output against DevTools**
   - File affected: None (validation only)
   - Changes: Use DevTools color picker to verify primary color
   - Steps:
     1. Open https://reinvent.awsevents.com/ in Chrome
     2. Inspect header element
     3. Note computed backgroundColor (expect #000000 or #232f3e)
     4. Compare against scraped config: `jq '.colors.primary' style-configs/aws-reinvent-2025.json`
   - Validation: Colors match within ±2 RGB units

3. **Fix snake_case to camelCase conversion**
   - File affected: `style-configs/aws-reinvent-2025.json`
   - Changes: Python scraper exports snake_case (event_id, brand_voice), TypeScript expects camelCase (eventId, brandVoice)
   - Manual fix required:
     ```bash
     # Backup original
     cp style-configs/aws-reinvent-2025.json style-configs/aws-reinvent-2025.json.backup

     # Convert (manual edit or use jq)
     jq '
       .eventId = .event_id | del(.event_id) |
       .eventName = .event_name | del(.event_name) |
       .sourceUrl = .source_url | del(.source_url) |
       .brandVoice = .brand_voice | del(.brand_voice)
     ' style-configs/aws-reinvent-2025.json.backup > style-configs/aws-reinvent-2025.json
     ```
   - Validation: TypeScript schema validation passes

4. **Manually correct colors if needed (Lesson 18)**
   - File affected: `style-configs/aws-reinvent-2025.json`
   - Changes: If DevTools shows #000000 but scraper extracted #232f3e, manually correct
   - Edit: `jq '.colors.primary = "#000000"' style-configs/aws-reinvent-2025.json > /tmp/fixed.json && mv /tmp/fixed.json style-configs/aws-reinvent-2025.json`
   - Validation: Grep for corrected color: `jq '.colors.primary' style-configs/aws-reinvent-2025.json`

5. **Test CSS generation with scraped config**
   - File affected: None (test only)
   - Changes: Verify TypeScript can read config and generate CSS
   - Command:
     ```bash
     node -e "
       const { generateEventCSS } = require('./dist/cssGenerator.js');
       const config = require('./style-configs/aws-reinvent-2025.json');
       const css = generateEventCSS(config);
       console.log(css.substring(0, 200));
     "
     ```
   - Validation: CSS output contains `--color-primary: #000000;` (or expected value)

**Validation Checkpoint:**
- [ ] `style-configs/aws-reinvent-2025.json` exists and is valid JSON
- [ ] eventId is "aws-reinvent-2025" (camelCase)
- [ ] colors.primary matches DevTools measurement (±2 RGB)
- [ ] typography includes "Amazon Ember" or system fonts
- [ ] brandVoice.tone is "professional" or "technical"
- [ ] TypeScript cssGenerator can parse config without errors

### Phase 2: Create Event JSON File

**Objective:** Add AWS re:Invent event metadata to data/events/

**Steps:**

1. **Research AWS re:Invent 2025 details**
   - File affected: None (research only)
   - Changes: Gather accurate dates, location, scale from https://reinvent.awsevents.com/
   - Expected info:
     - Dates: Late November/Early December 2025 (typically)
     - Location: Las Vegas, NV (Venetian, Wynn, MGM Grand, etc.)
     - Scale: 60,000+ attendees, 2,000+ sessions, 5 days
     - Website: https://reinvent.awsevents.com/
   - Validation: Cross-check dates/location against official website

2. **Create event JSON file**
   - File affected: `data/events/aws-reinvent-2025.json` (created)
   - Changes: New file with Event schema
   - Content:
     ```json
     {
       "id": "aws-reinvent-2025",
       "name": "AWS re:Invent 2025",
       "description": "AWS re:Invent is a learning conference hosted by Amazon Web Services for the global cloud computing community. Join 60,000+ builders, developers, and IT leaders for five days of keynotes, training, certification opportunities, and technical sessions across compute, AI/ML, serverless, containers, databases, security, and more.",
       "location": "Las Vegas, NV",
       "startDate": "2025-12-01T08:00:00Z",
       "endDate": "2025-12-05T18:00:00Z",
       "totalAttendees": 65000,
       "totalSessions": 2200,
       "websiteUrl": "https://reinvent.awsevents.com/",
       "logoUrl": null
     }
     ```
   - Validation: Load event in TypeScript: `node -e "const { loadEvent } = require('./dist/dataLoader.js'); loadEvent('aws-reinvent-2025').then(console.log);"`

3. **Validate event JSON schema**
   - File affected: None (validation only)
   - Changes: Ensure all required Event fields present and correct types
   - Command:
     ```bash
     node -e "
       const { isEvent } = require('./dist/types/index.js');
       const event = require('./data/events/aws-reinvent-2025.json');
       if (!isEvent(event)) throw new Error('Invalid event schema');
       console.log('✓ Event schema valid');
     "
     ```
   - Validation: Script succeeds, prints "Event schema valid"

**Validation Checkpoint:**
- [ ] `data/events/aws-reinvent-2025.json` exists and is valid JSON
- [ ] All required Event fields present (id, name, description, location, dates, totals, websiteUrl)
- [ ] Dates are in ISO 8601 format
- [ ] Event loads successfully via dataLoader
- [ ] isEvent() type guard returns true

### Phase 3: Create 12 Attendee Personas

**Objective:** Generate believable attendee data with AWS-themed sessions and connections

**Steps:**

1. **Define 6 persona types (2 attendees each)**
   - File affected: None (design only)
   - Changes: Document persona characteristics for consistency
   - Personas:
     1. **Cloud Architects** (3001-3002): 14-15 sessions, focus on compute/networking/security, senior roles, 20-25 connections
     2. **DevOps Engineers** (3003-3004): 12-13 sessions, focus on containers/CI-CD/serverless, mid-level, 18-22 connections
     3. **Startup Founders** (3005-3006): 10-11 sessions, focus on cost optimization/scaling/AI, exec roles, 22-26 connections (networking-heavy)
     4. **Enterprise CTOs** (3007-3008): 8-9 sessions, focus on keynotes/strategy/leadership, exec roles, 12-15 connections
     5. **Solutions Architects** (3009-3010): 13-14 sessions, focus on architecture/best practices/case studies, senior roles, 18-20 connections
     6. **ML Engineers** (3011-3012): 12-13 sessions, focus on AI/ML/SageMaker/Bedrock, mid-level, 16-20 connections
   - Validation: Each persona has distinct session focus and engagement pattern

2. **Create session pool (60+ unique sessions)**
   - File affected: None (content design)
   - Changes: Define AWS session titles, descriptions, speakers, tracks
   - Tracks: Compute, AI/ML, Serverless, Containers, Security, Database, Networking, Keynotes, Cost Optimization, Architecture
   - Session examples:
     - "ARC301: Building Multi-Region Active-Active Architectures" (Architecture)
     - "AIM302: Fine-Tuning Foundation Models with Amazon Bedrock" (AI/ML)
     - "SVS201: Serverless at Scale: Lambda Best Practices" (Serverless)
     - "CON301: Amazon EKS: Production-Grade Kubernetes" (Containers)
     - "SEC303: Zero Trust Security on AWS" (Security)
     - "DAT401: Amazon Aurora: Performance at Scale" (Database)
     - "CMP302: EC2 Graviton Processors: Price-Performance Optimization" (Compute)
     - "KEY01: AWS CEO Keynote" (Keynote)
   - Validation: 60+ unique session IDs, diverse tracks, realistic titles

3. **Create connection pool (80+ unique connections)**
   - File affected: None (content design)
   - Changes: Define realistic AWS ecosystem connections
   - Connection types:
     - AWS employees (Solutions Architects, Developer Advocates, Product Managers)
     - AWS partners (Datadog, Snowflake, MongoDB, HashiCorp, Terraform)
     - Consulting firms (Accenture, Deloitte, Slalom, Trek10)
     - Startups (seed-funded, Series A-C)
     - Enterprise tech companies (Fortune 500 tech leads)
   - Name diversity: Use realistic names from multiple backgrounds
   - Validation: 80+ unique connections, varied companies, realistic titles

4. **Generate attendee 3001 (Cloud Architect - High Engagement)**
   - File affected: `data/attendees/3001.json` (created)
   - Changes: New file with Attendee schema, 15 sessions, 25 connections
   - Profile:
     - Name: "Priya Sharma"
     - Title: "Senior Cloud Architect"
     - Company: "FinTech Innovations Inc"
     - Sessions: 15 (focus: Compute, Networking, Security, Architecture)
     - Connections: 25 (AWS SAs, partners, enterprise architects)
     - Stats: { sessionsAttended: 15, connectionsMade: 25, hoursAttended: 22.5, tracksExplored: 6, topAchievement: "Architecture Expert" }
     - CTAs: AWS training, re:Invent 2026, AWS Partner Network
   - Validation: File loads via dataLoader, passes isAttendee() type guard

5. **Generate attendee 3002 (Cloud Architect - High Engagement)**
   - File affected: `data/attendees/3002.json` (created)
   - Changes: Similar to 3001 but different name, company, session selection
   - Profile:
     - Name: "James Chen"
     - Company: "Global Retail Solutions"
     - Sessions: 14 (different mix than 3001, some overlap)
   - Validation: Same as 3001

6. **Generate attendees 3003-3004 (DevOps Engineers)**
   - Files affected: `data/attendees/3003.json`, `data/attendees/3004.json` (created)
   - Changes: 12-13 sessions focused on containers, CI/CD, serverless
   - Profile examples:
     - 3003: "Carlos Rodriguez", "DevOps Team Lead", "E-Commerce Platform"
     - 3004: "Aisha Okafor", "Senior DevOps Engineer", "Media Streaming Service"
   - Validation: Files load, sessions include EKS, Lambda, CodePipeline topics

7. **Generate attendees 3005-3006 (Startup Founders)**
   - Files affected: `data/attendees/3005.json`, `data/attendees/3006.json` (created)
   - Changes: 10-11 sessions, networking-heavy (25+ connections)
   - Profile examples:
     - 3005: "Emily Zhang", "Co-Founder & CTO", "AI Startup (Series A)"
     - 3006: "Michael Brown", "Founder & CEO", "SaaS Startup (Seed)"
   - Validation: High connection count relative to sessions, cost optimization focus

8. **Generate attendees 3007-3008 (Enterprise CTOs)**
   - Files affected: `data/attendees/3007.json`, `data/attendees/3008.json` (created)
   - Changes: 8-9 sessions, focus on keynotes and strategy
   - Profile examples:
     - 3007: "Sarah Johnson", "CTO", "Fortune 500 Manufacturing"
     - 3008: "David Kim", "VP of Engineering", "Global Insurance Company"
   - Validation: Includes KEY01, KEY02 keynotes, fewer technical deep-dives

9. **Generate attendees 3009-3010 (Solutions Architects)**
   - Files affected: `data/attendees/3009.json`, `data/attendees/3010.json` (created)
   - Changes: 13-14 sessions, architecture and best practices focus
   - Profile examples:
     - 3009: "Lisa Martinez", "Lead Solutions Architect", "Healthcare Provider"
     - 3010: "Robert Taylor", "Principal Architect", "Financial Services"
   - Validation: Sessions include ARC, SEC, NET tracks

10. **Generate attendees 3011-3012 (ML Engineers)**
    - Files affected: `data/attendees/3011.json`, `data/attendees/3012.json` (created)
    - Changes: 12-13 sessions, focus on AI/ML services
    - Profile examples:
      - 3011: "Fatima Al-Mansouri", "Machine Learning Engineer", "Autonomous Vehicles Startup"
      - 3012: "Kevin O'Brien", "Senior ML Engineer", "Advertising Technology"
    - Validation: Sessions include SageMaker, Bedrock, Rekognition, AI/ML track

**Validation Checkpoint:**
- [ ] 12 attendee files created (3001-3012)
- [ ] All files pass isAttendee() type guard
- [ ] Total sessions across all attendees: 120-150
- [ ] Total connections across all attendees: 200-250
- [ ] Session diversity: 60+ unique session IDs
- [ ] Connection diversity: 80+ unique connections
- [ ] AWS service mentions: 50+ (Lambda, S3, EC2, SageMaker, etc.)
- [ ] Realistic engagement range: 8-15 sessions per attendee

### Phase 4: Remove TechConf 2025 Data

**Objective:** Delete old generic event and its 12 attendees

**Steps:**

1. **Backup current state (safety)**
   - File affected: None (backup only)
   - Changes: Create git commit before deletion
   - Command:
     ```bash
     git add -A
     git commit -m "checkpoint: before removing TechConf 2025 data"
     ```
   - Validation: `git log -1` shows checkpoint commit

2. **Delete event file**
   - File affected: `data/events/event-2025.json` (deleted)
   - Changes: Remove file
   - Command: `rm data/events/event-2025.json`
   - Validation: `ls data/events/` shows only event-tech-live-2025.json and aws-reinvent-2025.json

3. **Delete attendee files 1001-1012**
   - Files affected: `data/attendees/1001.json` through `data/attendees/1012.json` (deleted)
   - Changes: Remove 12 files
   - Command: `rm data/attendees/100*.json`
   - Validation: `ls data/attendees/ | wc -l` shows 24 (12 Event Tech Live + 12 re:Invent)

4. **Search for hardcoded references**
   - Files affected: tests/, src/, README.md, CLAUDE.md (potentially)
   - Changes: Find any hardcoded "event-2025" or "1001"-"1012" references
   - Command:
     ```bash
     grep -r "event-2025" tests/ src/ README.md CLAUDE.md --exclude-dir=node_modules --exclude-dir=dist
     grep -r "\"100[0-9]\"" tests/ src/ --exclude-dir=node_modules --exclude-dir=dist
     ```
   - Validation: Note all matches for next step

5. **Update hardcoded references**
   - Files affected: Identified in step 4
   - Changes: Replace "event-2025" with "event-tech-live-2025" or "aws-reinvent-2025"
   - Replace "1001" with "2001" or "3001" (Event Tech Live or re:Invent attendees)
   - Validation: Re-run grep, expect 0 results

**Validation Checkpoint:**
- [ ] event-2025.json deleted
- [ ] Attendees 1001-1012 deleted
- [ ] No remaining references to "event-2025" in codebase
- [ ] No remaining references to attendee IDs 1001-1012
- [ ] 24 attendee files remain (2001-2012 + 3001-3012)

### Phase 5: Update Tests and Validate

**Objective:** Ensure all tests pass with new data, update fixtures as needed

**Steps:**

1. **Run test suite (identify failures)**
   - File affected: None (test only)
   - Changes: None
   - Command: `npm test`
   - Expected: 0-10 tests fail due to missing event-2025 fixtures
   - Validation: Note which test files fail

2. **Update failing unit tests**
   - Files affected: `tests/unit/dataLoader.test.ts`, `tests/unit/generate.test.ts` (potentially)
   - Changes: Replace event-2025 references with event-tech-live-2025 or aws-reinvent-2025
   - Example:
     ```typescript
     // Before:
     const event = await loadEvent('event-2025');

     // After:
     const event = await loadEvent('event-tech-live-2025');
     ```
   - Validation: Unit tests pass

3. **Update failing integration tests**
   - Files affected: `tests/integration/endToEnd.test.ts`, `tests/integration/styleIntegration.test.ts` (potentially)
   - Changes: Update fixture data to use new event IDs and attendee IDs
   - Example:
     ```typescript
     // Before:
     const attendee = await loadAttendee('1001');

     // After:
     const attendee = await loadAttendee('2001');  // Event Tech Live
     // OR
     const attendee = await loadAttendee('3001');  // AWS re:Invent
     ```
   - Validation: Integration tests pass

4. **Update validation tests if needed**
   - Files affected: `tests/validation/htmlValidation.test.ts` (potentially)
   - Changes: Validation tests generate pages for all attendees dynamically, should auto-adjust
   - Validation: HTML validation tests pass, now validate 24 pages instead of 24

5. **Add new tests for AWS re:Invent data**
   - Files affected: `tests/integration/endToEnd.test.ts` (add test)
   - Changes: Add test case validating AWS re:Invent attendee page generation
   - Example:
     ```typescript
     it('should generate valid page for AWS re:Invent attendee', async () => {
       const attendee = await loadAttendee('3001');
       expect(attendee.eventId).toBe('aws-reinvent-2025');
       expect(attendee.sessions.length).toBeGreaterThanOrEqual(8);

       await generateAttendeePage(attendee, event, hbs);
       const html = await readFile('dist/attendees/3001/index.html', 'utf-8');

       expect(html).toContain('AWS re:Invent');
       expect(html).toContain('Priya Sharma');
     });
     ```
   - Validation: New test passes

6. **Run full test suite (verify all passing)**
   - File affected: None (test only)
   - Changes: None
   - Command: `npm test`
   - Expected: 139+ tests passing (may increase if new tests added)
   - Validation: 100% pass rate

7. **Check test coverage**
   - File affected: None (coverage check)
   - Changes: None
   - Command: `npm run test:coverage`
   - Expected: ≥89% coverage (unchanged or improved)
   - Validation: Coverage meets or exceeds target

**Validation Checkpoint:**
- [ ] All tests passing (139+ tests)
- [ ] No references to event-2025 in test files
- [ ] Test coverage ≥89%
- [ ] New tests added for AWS re:Invent attendees
- [ ] HTML validation passes for all 24 pages

### Phase 6: Update Documentation

**Objective:** Update README, CLAUDE.md, and plans to reflect new data source

**Steps:**

1. **Update README.md**
   - File affected: `README.md`
   - Changes: Replace TechConf 2025 references with AWS re:Invent
   - Sections to update:
     - Project Overview: Mention "24 attendees across AWS re:Invent and Event Tech Live"
     - Examples: Update example commands to use attendee 3001 or 2001 (not 1001)
     - Data section: Reference aws-reinvent-2025.json
   - Validation: Preview README, verify changes make sense

2. **Update CLAUDE.md**
   - File affected: `CLAUDE.md`
   - Changes: Update current state, add lesson learned if applicable
   - Sections to update:
     - "Current State": 24 pages across 2 events (AWS re:Invent, Event Tech Live)
     - File structure example: Reference attendees/3001/ instead of 1001/
     - Add to Critical Lessons Learned if Plan 007 reveals insights
   - Validation: Read through updated sections, ensure accuracy

3. **Update plans/README.md**
   - File affected: `plans/README.md`
   - Changes: Add Plan 007 to index and recent updates
   - Entry:
     ```markdown
     | 007 | AWS re:Invent Data Source Integration | Complete | 2025-11-07 | Replace TechConf with AWS re:Invent, scrape branding, create 12 attendees |
     ```
   - Recent updates:
     ```markdown
     - **2025-11-07**: Completed Plan 007 - AWS re:Invent Data Source Integration ✅
       - Scraped https://reinvent.awsevents.com/ for authentic AWS branding
       - Created 12 believable attendee personas (3001-3012) with AWS-themed sessions
       - Removed generic TechConf 2025 data source (event-2025, attendees 1001-1012)
       - System now has 2 high-quality event sources: AWS re:Invent, Event Tech Live
       - All 139 tests passing with updated fixtures
     ```
   - Validation: Index is sorted by plan number, recent updates are chronological

4. **Update requirements/data-models.md**
   - File affected: `requirements/data-models.md`
   - Changes: Update example paths and IDs to reference new data
   - Example:
     ```markdown
     # Before:
     └── attendees/
         ├── 1001.json

     # After:
     └── attendees/
         ├── 2001.json  # Event Tech Live attendees
         ├── 3001.json  # AWS re:Invent attendees
     ```
   - Validation: Examples use valid attendee IDs

5. **Create Plan 007 completion report**
   - File affected: `analysis/plan-007-completion-report.md` (created)
   - Changes: Document outcomes, validation results, lessons learned
   - Sections:
     - Scraping results (success rate, color accuracy)
     - Data quality metrics (session count, connection count, AWS mentions)
     - Test results (pass rate, coverage)
     - Performance (generation time for 24 pages)
     - Lessons learned (any challenges encountered)
   - Validation: Report is comprehensive and factual

**Validation Checkpoint:**
- [ ] README.md references AWS re:Invent (not TechConf 2025)
- [ ] CLAUDE.md updated with current state
- [ ] plans/README.md includes Plan 007
- [ ] requirements/data-models.md uses valid attendee IDs
- [ ] Plan 007 completion report created in analysis/

### Phase 7: Generate Pages and Validate Output

**Objective:** Generate all 24 pages, verify AWS branding applied, validate HTML

**Steps:**

1. **Generate all attendee pages**
   - File affected: `dist/` directory (24 pages)
   - Changes: Regenerate entire site
   - Command: `npm run generate`
   - Expected: 24 pages generated in < 2 seconds
   - Validation: Check output for "Generated 24 attendee pages"

2. **Verify AWS re:Invent pages exist**
   - File affected: None (check only)
   - Changes: None
   - Command:
     ```bash
     ls dist/attendees/30*/index.html | wc -l
     # Expected: 12

     ls dist/attendees/*/index.html | wc -l
     # Expected: 24 (12 Event Tech Live + 12 re:Invent)
     ```
   - Validation: 12 re:Invent pages, 24 total pages

3. **Verify AWS branding applied**
   - File affected: None (check only)
   - Changes: None
   - Command:
     ```bash
     # Check for AWS colors in CSS variables
     grep -E "color-primary.*#000000|#232f3e" dist/attendees/3001/index.html

     # Check for AWS content
     grep -c "re:Invent\|AWS\|Amazon" dist/attendees/3001/index.html
     # Expected: 20+ mentions

     # Check for specific sessions
     grep "Lambda\|SageMaker\|EKS" dist/attendees/3001/index.html | wc -l
     # Expected: 5+ mentions
     ```
   - Validation: AWS colors present, re:Invent content abundant, AWS services mentioned

4. **Run HTML validation**
   - File affected: None (validation only)
   - Changes: None
   - Command: `npm test -- tests/validation/htmlValidation.test.ts`
   - Expected: 0 errors, 48-72 warnings (acceptable)
   - Validation: All 24 pages pass W3C validation

5. **Visual spot-check (manual)**
   - File affected: None (manual review)
   - Changes: None
   - Steps:
     1. `http-server dist -p 8080`
     2. Open http://localhost:8080/attendees/3001/
     3. Verify AWS branding visible (black/orange colors)
     4. Check sessions list shows AWS-themed content
     5. Verify connections list shows realistic names/companies
   - Validation: Page looks professional, branding applied, content realistic

6. **Performance benchmark**
   - File affected: None (benchmark)
   - Changes: None
   - Command:
     ```bash
     time npm run generate
     # Expected: < 2 seconds for 24 pages
     ```
   - Validation: Performance meets target (< 2s)

**Validation Checkpoint:**
- [ ] 24 pages generated successfully
- [ ] All 12 AWS re:Invent pages exist
- [ ] AWS branding visible (colors, fonts)
- [ ] re:Invent content present (sessions, connections)
- [ ] HTML validation: 0 errors
- [ ] Generation time: < 2 seconds
- [ ] Visual spot-check: Professional appearance

---

## Dependencies

### Prerequisites
- [ ] Python 3.13+ installed
- [ ] OpenAI API key configured in .env
- [ ] Playwright browsers installed (`npx playwright install`)
- [ ] All 139 tests passing before starting
- [ ] Plan 005 completed (Playwright scraping working)

### Related Plans
- `plans/005-playwright-scraping-tool.md` - Provides scraping capability needed for Phase 1
- `plans/003-python-scraping-layer.md` - CrewAI architecture used by scraper
- `plans/002-event-tech-live-data.md` - Established pattern for multi-event support

### External Dependencies
- https://reinvent.awsevents.com/ must be accessible (public website)
- OpenAI API for CrewAI agents (cost: ~$0.10 for re:Invent scrape)
- Chrome/Chromium for Playwright (installed locally)

---

## Risk Assessment

### High Risk Items

1. **Risk:** AWS re:Invent website blocks Playwright scraper (bot detection)
   - **Likelihood:** Low (public marketing site, not protected resources)
   - **Impact:** High (blocks Phase 1, entire plan)
   - **Mitigation:** Use Playwright stealth mode, add realistic user agent, respect robots.txt
   - **Contingency:** Manually create EventStyleConfig using DevTools inspection, skip scraping step

2. **Risk:** Scraped colors are incorrect (AI misidentifies primary color)
   - **Likelihood:** Medium (AI agents sometimes pick wrong element)
   - **Impact:** Medium (wrong branding on generated pages)
   - **Mitigation:** DevTools validation in Phase 1, manual correction per Lesson 18
   - **Contingency:** Use DevTools color picker to manually correct scraped config

3. **Risk:** Removing TechConf breaks many tests (tight coupling)
   - **Likelihood:** Low (most tests use Event Tech Live fixtures)
   - **Impact:** Medium (delays Phase 5, requires test rewrites)
   - **Mitigation:** Test removal on branch first, identify failures before committing
   - **Contingency:** Create test-only fixtures in tests/ directory, minimal impact on production data

### Medium Risk Items

1. **Risk:** Attendee data feels generic/unrealistic despite AWS theme
   - **Likelihood:** Low (have real AWS session examples to base on)
   - **Impact:** Medium (reduces demo quality)
   - **Mitigation:** Research actual re:Invent session catalog, use authentic titles/descriptions
   - **Contingency:** Iterate on attendee data post-implementation, refine session content

2. **Risk:** 12 attendees not enough to show diversity
   - **Likelihood:** Low (6 personas × 2 = good variety)
   - **Impact:** Low (still demonstrates capability)
   - **Mitigation:** Ensure personas span roles, industries, engagement levels
   - **Contingency:** Add 3-6 more attendees in follow-up plan if needed

3. **Risk:** OpenAI API cost higher than expected
   - **Likelihood:** Low (estimate $0.10, typical range $0.05-0.20)
   - **Impact:** Low ($$$, but single scrape)
   - **Mitigation:** Monitor token usage, use gpt-4o-mini if possible
   - **Contingency:** Budget $0.50 max for this plan, acceptable cost

### Low Risk Items

1. **Risk:** Generated pages exceed GitHub Pages file size limits
   - **Likelihood:** Very Low (24 pages × ~50KB = 1.2MB total)
   - **Impact:** Low (deployment fails)
   - **Mitigation:** Monitor dist/ directory size
   - **Contingency:** Minify HTML, reduce page size

2. **Risk:** Documentation updates introduce inconsistencies
   - **Likelihood:** Low (careful review process)
   - **Impact:** Low (confusing docs)
   - **Mitigation:** Cross-reference updated docs against actual data
   - **Contingency:** User reports, fix in follow-up commit

---

## Rollback Plan

If implementation fails or introduces regressions:

1. **Revert all changes**
   ```bash
   git reset --hard HEAD~N  # N = number of commits for Plan 007
   git clean -fd
   ```

2. **Restore TechConf 2025 data** (if deleted prematurely)
   ```bash
   git checkout HEAD~N -- data/events/event-2025.json
   git checkout HEAD~N -- data/attendees/100*.json
   ```

3. **Delete failed AWS re:Invent data**
   ```bash
   rm -f data/events/aws-reinvent-2025.json
   rm -f data/attendees/30*.json
   rm -f style-configs/aws-reinvent-2025.json
   ```

4. **Regenerate site with original data**
   ```bash
   npm run build
   npm run generate
   ```

5. **Verify rollback successful**
   ```bash
   npm test
   ls data/attendees/ | wc -l  # Should be 24 (if rolled back to Plan 002 state)
   ```

**Validation after rollback:**
- [ ] All tests passing
- [ ] Original data restored
- [ ] No AWS re:Invent references in codebase
- [ ] Site generates successfully

---

## Testing Strategy

### Unit Tests

- [ ] Test loading aws-reinvent-2025 event via dataLoader
- [ ] Test loading attendees 3001-3012 via dataLoader
- [ ] Test isAttendee() type guard with new attendee data
- [ ] Test isEvent() type guard with new event data
- [ ] Test CSS generation with AWS re:Invent config

### Integration Tests

- [ ] Test end-to-end generation of AWS re:Invent attendee pages
- [ ] Test style integration with AWS colors
- [ ] Test that Event Tech Live pages still generate correctly
- [ ] Test loadAllAttendees() returns 24 attendees across 2 events

### Manual Testing

1. **Scraping Validation**
   - Run scraper against https://reinvent.awsevents.com/
   - Check scraped colors against DevTools
   - Verify Amazon Ember font detected

2. **Data Quality Check**
   - Review attendee 3001 JSON file for realism
   - Check for AWS service mentions in sessions
   - Verify connection diversity (companies, titles)

3. **Visual Page Inspection**
   - Open generated page for attendee 3001
   - Verify AWS branding applied (colors)
   - Check session list shows AWS content
   - Verify connections list is realistic

4. **Cross-Event Validation**
   - Open Event Tech Live page (2001) alongside AWS re:Invent page (3001)
   - Verify different branding applied correctly
   - Confirm no style leakage between events

### Validation Commands

```bash
# Scrape AWS re:Invent
python -m event_style_scraper scrape --url https://reinvent.awsevents.com/ --timeout 90

# Validate schema
jq -e '.eventId and .colors and .typography and .brandVoice' style-configs/aws-reinvent-2025.json

# Load all attendees
node -e "const { loadAllAttendees } = require('./dist/dataLoader.js'); loadAllAttendees().then(a => console.log('Total:', a.length, 'Events:', [...new Set(a.map(x => x.eventId))].join(', ')));"

# Generate pages
npm run generate

# Validate HTML
npm test -- tests/validation/htmlValidation.test.ts

# Full test suite
npm test

# Check coverage
npm run test:coverage
```

---

## Post-Implementation

### Documentation Updates
- [x] Update README.md to reference AWS re:Invent
- [x] Update CLAUDE.md with current state (24 attendees, 2 events)
- [x] Update plans/README.md with Plan 007 entry
- [x] Update requirements/data-models.md with new attendee ID examples
- [ ] Create Plan 007 completion report in analysis/

### Knowledge Capture
- [ ] Document lessons learned in CLAUDE.md if applicable
  - If scraping challenges: Add to Lessons Learned
  - If bot detection: Document workaround
  - If data quality insights: Add best practices
- [ ] Update best practices for creating attendee personas
- [ ] Add AWS re:Invent as case study in docs/

### Validation Report
- [ ] Create `analysis/plan-007-validation-report.md`:
  - Scraping success rate: X/Y attempts
  - Color accuracy: DevTools vs scraped (±N RGB)
  - Data quality: Session count, connection count, AWS mentions
  - Test results: X/Y passing, Z% coverage
  - Performance: Generation time for 24 pages
  - HTML validation: 0 errors, N warnings

---

## Appendix

### References
- PRD-003: requirements/prd-003.md
- Exploration Report: analysis/exploration-report-2025-11-07-reinvent.md
- Plan 005: plans/005-playwright-scraping-tool.md (scraping capability)
- CLAUDE.md Lesson 18: Verify Scraper Output with DevTools
- AWS re:Invent website: https://reinvent.awsevents.com/

### Alternative Approaches Considered

1. **Approach:** Keep TechConf 2025 alongside AWS re:Invent (3 events total)
   - **Pros:** No deletion risk, more data sources
   - **Cons:** TechConf is generic placeholder, reduces quality perception, adds maintenance burden
   - **Why not chosen:** PRD-003 explicitly requests removal, focus on quality over quantity

2. **Approach:** Create 20-30 AWS re:Invent attendees (match Event Tech Live scale)
   - **Pros:** More demo data, shows scale
   - **Cons:** Diminishing returns after 12 personas, increases generation time, content creation effort
   - **Why not chosen:** 12 attendees sufficient to show diversity, keeps parity with Event Tech Live

3. **Approach:** Use AI to generate attendee data (GPT-4 writes JSON files)
   - **Pros:** Faster content creation, potentially more creative
   - **Cons:** AI may hallucinate unrealistic data, lacks human curation, quality control needed anyway
   - **Why not chosen:** Manual curation ensures realism and quality (per Lesson 17)

4. **Approach:** Scrape actual re:Invent session catalog from website
   - **Pros:** Maximally authentic session data
   - **Cons:** Scraping session catalog more complex than homepage, may hit rate limits, legal/ethical concerns
   - **Why not chosen:** Manual curation of session titles is sufficient, avoids scraping overreach

### Session Title Examples (60+ AWS re:Invent Sessions)

**Compute (CMP):**
- CMP301: Amazon EC2 Graviton: 40% Better Price-Performance
- CMP302: Spot Instances at Scale: Best Practices and Patterns
- CMP303: EC2 Image Builder: Automated AMI Pipelines

**AI/ML (AIM):**
- AIM301: Amazon Bedrock: Building with Foundation Models
- AIM302: Fine-Tuning LLMs: From Prototype to Production
- AIM303: Amazon SageMaker: Real-Time Inference at Scale
- AIM304: Amazon Rekognition: Computer Vision Applications

**Serverless (SVS):**
- SVS201: AWS Lambda: Performance Optimization Techniques
- SVS202: Step Functions: Orchestrating Serverless Workflows
- SVS203: EventBridge: Event-Driven Architectures

**Containers (CON):**
- CON301: Amazon EKS: Production-Grade Kubernetes
- CON302: ECS vs EKS: Choosing the Right Container Service
- CON303: Fargate: Serverless Containers

**Security (SEC):**
- SEC301: Zero Trust Security on AWS
- SEC302: AWS IAM: Advanced Access Control Patterns
- SEC303: GuardDuty and Security Hub: Threat Detection at Scale

**Database (DAT):**
- DAT401: Amazon Aurora: Global Database at Scale
- DAT402: DynamoDB: Single-Digit Millisecond Performance
- DAT403: Redshift: Petabyte-Scale Data Warehousing

**Architecture (ARC):**
- ARC301: Multi-Region Active-Active Architectures
- ARC302: Well-Architected Framework: Best Practices
- ARC303: Disaster Recovery Strategies on AWS

**Networking (NET):**
- NET201: VPC Design Patterns for Scalable Architectures
- NET202: AWS Transit Gateway: Simplified Network Management
- NET203: CloudFront: Global Content Delivery at Scale

**Cost Optimization (COP):**
- COP101: Cost Optimization: FinOps Best Practices
- COP102: Reserved Instances and Savings Plans: Maximizing Savings
- COP103: Cost Allocation Tags: Chargeback and Showback

**Keynotes (KEY):**
- KEY01: AWS CEO Keynote: The Future of Cloud Computing
- KEY02: AWS CTO Keynote: Technical Innovations Unveiled
- KEY03: Customer Success Stories: Transforming with AWS

### Connection Examples (80+ AWS Ecosystem Connections)

**AWS Employees:**
- "Sarah Chen", "Senior Solutions Architect", "Amazon Web Services"
- "Michael Rodriguez", "Principal Developer Advocate", "Amazon Web Services"
- "Aisha Okafor", "Product Manager - Lambda", "Amazon Web Services"

**AWS Partners:**
- "David Kim", "Solutions Engineer", "Datadog"
- "Emily Zhang", "Technical Account Manager", "Snowflake"
- "James Patterson", "Sales Engineer", "MongoDB"
- "Lisa Martinez", "Cloud Architect", "HashiCorp"

**Consulting Firms:**
- "Robert Taylor", "AWS Practice Lead", "Accenture"
- "Jennifer Lee", "Cloud Solutions Architect", "Deloitte Digital"
- "Carlos Mendez", "Principal Consultant", "Slalom Consulting"
- "Amanda Foster", "Solutions Architect", "Trek10"

**Startups:**
- "Kevin O'Brien", "Co-Founder & CTO", "AI Startup (Series B)"
- "Fatima Al-Mansouri", "VP of Engineering", "FinTech Startup (Series A)"
- "Thomas Anderson", "Founder", "SaaS Startup (Seed)"

**Enterprise:**
- "Maria Silva", "Director of Cloud Architecture", "Fortune 500 Retail"
- "John Williams", "Lead Cloud Engineer", "Global Bank"
- "Priya Patel", "Senior DevOps Engineer", "Telecom Provider"

### Notes

- **Session authenticity:** While session IDs (CMP301, AIM302) follow AWS format, exact titles may differ from actual re:Invent agenda. This is acceptable for demo purposes.
- **Connection realism:** Names and companies are fictional but plausible. LinkedIn URLs are omitted to avoid creating false profiles.
- **Scraping cost:** Estimated $0.10 for single re:Invent scrape based on Plan 005 experience with example.com ($0.05) and eventtechlive.com ($0.08). AWS site may be slightly larger/slower.
- **Performance impact:** Adding 12 attendees should not materially impact generation time (< 2s for 24 pages vs < 1s for 12 pages).
- **Future expansion:** If AWS re:Invent proves valuable, could add more attendees (3013-3024) in follow-up plan, or add other major tech conferences (Google Cloud Next, Microsoft Build).

---

**Plan Status:** ✏️ **Draft - Awaiting Confirmation to Proceed**

**Estimated Complexity:** Medium (3-4 implementation sessions)
**Key Success Factors:**
1. Successful scraping without bot detection
2. High-quality, believable attendee content
3. Clean removal of TechConf data without breaking tests
4. DevTools validation of scraped colors

**Next Steps:**
- [ ] Review plan for completeness
- [ ] Validate target outcomes are measurable
- [ ] Confirm scraping approach is sound
- [ ] Approve content creation strategy
- [ ] **Obtain explicit confirmation to proceed with implementation**
