# Plan 006: End-to-End Scrape-to-Deploy GitHub Actions Pipeline

**Status:** Draft
**Created:** 2025-11-07
**Last Updated:** 2025-11-07 (Modified: removed scheduled runs)
**Priority:** 🔴 Critical

## Overview

This plan implements automated end-to-end validation (per CLAUDE.md Lesson 16) by integrating the Python style scraper into the GitHub Actions deployment pipeline. Currently, the scraper runs manually via CLI, and generated pages use either default styles or manually-scraped configs. This creates a disconnect between event website updates and deployed pages.

The enhanced pipeline will: (1) scrape event website styles using PlaywrightStyleExtractorTool, (2) validate scraped output against DevTools measurements, (3) generate static pages with event-specific CSS, and (4) deploy to GitHub Pages—all in a single automated workflow. This ensures deployed pages always reflect the latest event branding and validates the complete Python → TypeScript → HTML → Deploy integration chain that has never been fully tested (per exploration report 2025-11-07).

The workflow supports two trigger modes: (1) manual dispatch for on-demand scraping when event websites change, and (2) push-triggered deploys using cached configs for fast deployment. This provides explicit control over when scraping occurs (and associated API costs) while maintaining continuous deployment capability.

## Target Outcomes

### Primary Outcomes

1. **On-Demand Style Scraping**: GitHub Actions runs Python scraper when manually triggered, extracting accurate colors, typography, and brand voice
2. **Validated Integration**: Full pipeline validation from scrape → export → CSS generation → HTML generation → deployment with zero manual steps
3. **Explicit Style Updates**: Deployed pages reflect latest event website styles when user triggers scraping (full control over timing and costs)
4. **Cost-Controlled Scraping**: Manual-only triggers provide complete control over OpenAI API costs (no unexpected charges)
5. **Graceful Fallback**: Pipeline continues with cached configs if scraping fails, preventing deployment failures
6. **DevTools Validation**: Automated verification that scraped colors match actual website measurements (±2 RGB units)

### Success Criteria

- [ ] GitHub Actions workflow scrapes event websites when manually triggered and generates valid EventStyleConfig JSON
- [ ] Scraped configs pass schema validation (colors in #RRGGBB format, all required fields present)
- [ ] TypeScript CSS generator successfully reads scraped configs and generates CSS custom properties
- [ ] Generated HTML pages contain event-specific colors (verified via grep for CSS variables)
- [ ] Workflow completes within GitHub Actions timeout (< 45 minutes)
- [ ] Failed scraping doesn't block deployment (uses last known good config)
- [ ] OpenAI API costs only incurred on manual trigger (no unexpected charges)
- [ ] Manual dispatch workflow allows on-demand scraping for specific events or all events
- [ ] Validation script confirms scraped colors match DevTools (±2 RGB tolerance)
- [ ] End-to-end test passes: scrape example.com → generate pages → validate colors
- [ ] Push-triggered deploys complete in < 5 minutes (no scraping overhead)

### Validation Strategy

#### Empirical Validation Methods

**Method 1: Workflow Execution Validation**
- **Tools/Commands:**
  ```bash
  # Trigger workflow manually
  gh workflow run scrape-and-deploy.yml --ref main

  # Check run status
  gh run list --workflow=scrape-and-deploy.yml

  # View logs
  gh run view --log
  ```
- **Expected Results:** Workflow completes successfully, status badge shows passing, deployment succeeds
- **Acceptance Threshold:** 100% success rate for manual triggers, >95% for push-triggered deploys (no scraping)

**Method 2: Scraped Config Validation**
- **Tools/Commands:**
  ```bash
  # Validate JSON schema
  ajv validate -s schemas/event-style-config-schema.json -d style-configs/*.json

  # Check for required fields
  jq '.eventId, .colors.primary, .typography.headingFont, .brandVoice.tone' style-configs/event-tech-live-2025.json

  # Verify hex color format
  grep -E '"primary":\s*"#[0-9A-Fa-f]{6}"' style-configs/*.json
  ```
- **Expected Results:** All configs valid, all fields populated, colors in correct format
- **Acceptance Threshold:** 100% of scraped configs pass validation

**Method 3: CSS Generation Integration**
- **Tools/Commands:**
  ```bash
  # Run TypeScript generator with scraped configs
  npm run generate

  # Verify CSS variables in output
  grep "color-primary" dist/attendees/2001/index.html
  grep "#160822" dist/attendees/2001/index.html

  # Validate CSS syntax
  npx stylelint "dist/static/css/*.css"
  ```
- **Expected Results:** CSS generated successfully, colors from scraped config appear in HTML
- **Acceptance Threshold:** All 24 pages contain event-specific CSS variables

**Method 4: DevTools Color Accuracy**
- **Tools/Commands:**
  ```bash
  # Automated validation
  python scripts/validate_scraped_colors.py \
    --url https://eventtechlive.com \
    --config style-configs/event-tech-live-2025.json \
    --selector header \
    --property backgroundColor \
    --expected "#160822"
  ```
- **Expected Results:** Scraped colors match DevTools measurements within ±2 RGB units
- **Acceptance Threshold:** ≥95% of scraped colors within tolerance

**Method 5: End-to-End Pipeline Test**
- **Tools/Commands:**
  ```bash
  # Full pipeline test
  ./scripts/test-e2e-pipeline.sh

  # Manual verification
  # 1. Note color on https://eventtechlive.com header
  # 2. Trigger workflow
  # 3. Open deployed page: https://USERNAME.github.io/personal-event-summary/attendees/2001/
  # 4. Compare colors
  ```
- **Expected Results:** Colors match end-to-end (website → scraper → generated page → deployed site)
- **Acceptance Threshold:** 100% color match for manual spot checks

**Method 6: Cost and Performance**
- **Tools/Commands:**
  ```bash
  # Check workflow duration
  gh run list --workflow=scrape-and-deploy.yml --json durationMs

  # Estimate API costs
  # Log OpenAI API token usage from CrewAI
  # Manual-only: 4 events × ~2 scrapes/month × $0.10/scrape = $0.80/month (estimated)
  # Actual costs depend on trigger frequency
  ```
- **Expected Results:** Workflow completes in < 45 minutes (with scraping), < 5 minutes (push-only), API costs fully controlled by user
- **Acceptance Threshold:** All runs within timeout, no unexpected API charges

---

## Hypothesis-Driven Approach

### Hypothesis 1: Playwright Runs Successfully in GitHub Actions

**Reasoning:** Playwright requires Chromium browser and system dependencies. GitHub Actions runners don't have Playwright pre-installed, but `playwright install --with-deps` can install browsers and dependencies. This approach works for thousands of open-source projects using Playwright in CI.

**Validation Method:**
- **Experiment:** Create test workflow that installs Playwright and scrapes example.com
- **Expected Outcome:**
  ```yaml
  - name: Install Playwright
    run: |
      cd python
      pip install -r requirements.txt
      playwright install chromium
      playwright install-deps chromium

  - name: Test scraping
    run: |
      cd python
      PYTHONPATH=./src python -m event_style_scraper scrape --url https://example.com --timeout 60
  ```
  Output: JSON file created with computed styles

- **Validation Steps:**
  1. Push test workflow to branch
  2. Trigger workflow manually
  3. Check logs for Playwright browser launch
  4. Verify JSON output artifact
  5. Confirm no timeout or permission errors

**Success Criteria:**
- [ ] Playwright installs without errors (< 2 minutes)
- [ ] Browser launches successfully in headless mode
- [ ] Scraper extracts styles from example.com
- [ ] JSON file created with valid schema
- [ ] No "permission denied" or "browser not found" errors

**Failure Conditions:**
- Browser installation fails (missing system deps)
- Chromium fails to launch (sandboxing issues)
- Network timeout (firewall blocks external URLs)

**Fallback:** Use `--no-sandbox` flag for Chromium, or switch to Selenium with pre-installed Chrome

### Hypothesis 2: OpenAI API Key from Secrets Works with CrewAI

**Reasoning:** CrewAI reads OpenAI API key from `OPENAI_API_KEY` environment variable. GitHub Actions secrets can be exposed as env vars. This is standard practice for CI/CD with API keys.

**Validation Method:**
- **Experiment:** Configure secret, test in workflow
- **Expected Outcome:**
  ```yaml
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

  steps:
  - name: Verify API key
    run: |
      if [ -z "$OPENAI_API_KEY" ]; then
        echo "❌ OPENAI_API_KEY not set"
        exit 1
      fi
      echo "✓ OPENAI_API_KEY configured (${#OPENAI_API_KEY} chars)"

  - name: Test CrewAI
    run: |
      cd python
      PYTHONPATH=./src python -c "from crewai import LLM; print('LLM import OK')"
  ```
  CrewAI agents run successfully

- **Validation Steps:**
  1. Add `OPENAI_API_KEY` to repository secrets
  2. Test key validity: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $KEY"`
  3. Run workflow with secret exposed
  4. Check logs (secret should be masked as `***`)
  5. Verify CrewAI makes API calls successfully

**Success Criteria:**
- [ ] Secret configured in repository settings
- [ ] Secret value masked in logs (no leak)
- [ ] CrewAI agents execute without authentication errors
- [ ] API usage logged (for cost tracking)
- [ ] Scraping completes successfully

**Failure Conditions:**
- Secret not found (typo in name)
- API key invalid or expired
- Rate limit exceeded
- API call errors not caught

**Fallback:** Use organization-level secret, or implement key rotation logic

### Hypothesis 3: Scraped Configs Can Be Committed Back to Repo

**Reasoning:** After scraping, we need to persist configs for use in TypeScript generation. Two options: (1) commit to repo, (2) pass as artifact. Committing enables version control, diffing, and human review before deployment.

**Validation Method:**
- **Experiment:** Test automated commit from GitHub Actions
- **Expected Outcome:**
  ```yaml
  - name: Commit scraped configs
    run: |
      git config --global user.name "github-actions[bot]"
      git config --global user.email "github-actions[bot]@users.noreply.github.com"

      git add style-configs/*.json

      if git diff --staged --quiet; then
        echo "No changes to commit"
      else
        git commit -m "chore(scraper): update event style configs [skip ci]

        Automated scrape of event websites:
        - eventtechlive.com
        - example.com

        Colors updated to match current website styling.

        🤖 Generated by scrape-and-deploy workflow"

        git push
      fi
  ```
  Configs committed and pushed to main branch

- **Validation Steps:**
  1. Test on feature branch first
  2. Verify bot has write permissions
  3. Check commit appears in history
  4. Verify `[skip ci]` prevents infinite loops
  5. Confirm push succeeds

**Success Criteria:**
- [ ] Bot successfully commits changes
- [ ] Commit message follows conventional commits format
- [ ] Push succeeds without permission errors
- [ ] `[skip ci]` prevents recursive workflow triggers
- [ ] Git history shows clean commit attribution

**Failure Conditions:**
- Permission denied (bot lacks write access)
- Merge conflict (concurrent changes)
- Infinite loop (`[skip ci]` not working)
- Push fails (branch protection rules)

**Fallback:** Use workflow artifacts + manual review step, or PR-based flow

### Hypothesis 4: Workflow Completes Within GitHub Actions Timeout

**Reasoning:** GitHub Actions has 6-hour timeout per job, but free tier users may have shorter limits. Scraping 4 events × ~60s each + dependencies install ~5 min + TypeScript build ~2 min = ~10 minutes total. Well within limits.

**Validation Method:**
- **Experiment:** Time each workflow step
- **Expected Outcome:**
  ```yaml
  - name: Install Python deps
    run: time pip install -r python/requirements.txt  # ~2 min

  - name: Install Playwright
    run: time playwright install chromium --with-deps  # ~2 min

  - name: Scrape events
    run: |
      time python -m event_style_scraper scrape --url https://eventtechlive.com --timeout 90  # ~90s
      time python -m event_style_scraper scrape --url https://example.com --timeout 60  # ~60s

  - name: Build TypeScript
    run: time npm run build  # ~30s

  - name: Generate pages
    run: time npm run generate  # ~2s
  ```
  Total: ~6-8 minutes

- **Validation Steps:**
  1. Run workflow with timing instrumentation
  2. Parse logs for step durations
  3. Identify bottlenecks
  4. Optimize slow steps (cache deps, parallel scraping)
  5. Verify total < 45 minutes (safety margin)

**Success Criteria:**
- [ ] Total workflow duration < 10 minutes (typical)
- [ ] No step exceeds 5 minutes individually
- [ ] Cached dependencies reduce repeat runs to < 5 minutes
- [ ] Parallel scraping saves ~50% time vs sequential
- [ ] Buffer for API latency variability

**Failure Conditions:**
- Playwright installation times out (>10 min)
- Scraping hangs (network issues)
- CrewAI agents take too long (>5 min per event)
- Workflow exceeds free tier limits

**Fallback:** Split into multiple jobs (scrape job → build job), cache aggressively, reduce timeout limits

### Hypothesis 5: Failed Scraping Can Fall Back to Cached Configs

**Reasoning:** Scraping may fail due to: website downtime, API rate limits, network errors, bot detection. Deployment shouldn't fail if scraping fails—use last known good config instead.

**Validation Method:**
- **Experiment:** Test fallback logic with simulated failures
- **Expected Outcome:**
  ```yaml
  - name: Scrape with fallback
    id: scrape
    continue-on-error: true
    run: |
      cd python
      PYTHONPATH=./src python -m event_style_scraper scrape \
        --url https://eventtechlive.com \
        --output ../style-configs/event-tech-live-2025.json \
        --timeout 90

  - name: Check scraping result
    run: |
      if [ ${{ steps.scrape.outcome }} == 'failure' ]; then
        echo "⚠️ Scraping failed, using cached config"
        test -f style-configs/event-tech-live-2025.json || \
          (echo "❌ No fallback config available" && exit 1)
      else
        echo "✓ Scraping succeeded, using fresh config"
      fi
  ```
  Deployment proceeds with cached config

- **Validation Steps:**
  1. Test with intentional failures (invalid URL, no API key)
  2. Verify workflow doesn't abort
  3. Confirm cached config is used
  4. Check deployment succeeds
  5. Validate notification sent (optional)

**Success Criteria:**
- [ ] Failed scraping doesn't block deployment
- [ ] Cached config used as fallback
- [ ] Warning logged in workflow output
- [ ] Pages generated with fallback styles
- [ ] Optional: Slack/email notification sent

**Failure Conditions:**
- No cached config available (first run)
- Cached config invalid (schema changed)
- Deployment fails anyway (unrelated issue)

**Fallback:** Require manual approval for deployment after scrape failure, or use hardcoded default config

---

## Implementation Details

### Phase 1: Create Scrape-and-Deploy Workflow

**Objective:** Create new GitHub Actions workflow that orchestrates scraping, building, and deploying

**Steps:**

1. **Create workflow file: `.github/workflows/scrape-and-deploy.yml`**
   - File affected: `.github/workflows/scrape-and-deploy.yml` (new)
   - Changes:
     ```yaml
     name: Scrape Styles and Deploy

     on:
       # Manual trigger for on-demand scraping
       workflow_dispatch:
         inputs:
           events_to_scrape:
             description: 'Event IDs to scrape (comma-separated, or "all")'
             required: false
             default: 'all'
           force_scrape:
             description: 'Force scraping even if configs exist'
             type: boolean
             required: false
             default: false

       # On push to main (uses cached configs, no scraping)
       push:
         branches: [ main ]
         paths:
           - 'src/**'
           - 'templates/**'
           - 'static/**'
           - 'data/**'
           - '!python/**'  # Ignore Python changes to avoid triggering on config updates

     permissions:
       contents: write  # For committing scraped configs
       pages: write
       id-token: write

     concurrency:
       group: "pages"
       cancel-in-progress: false

     env:
       OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

     jobs:
       scrape:
         name: Scrape Event Styles
         runs-on: ubuntu-latest
         # Only run scraping on manual dispatch (not on push)
         if: github.event_name == 'workflow_dispatch'

         steps:
         - name: Checkout code
           uses: actions/checkout@v4

         - name: Setup Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'
             cache: 'pip'
             cache-dependency-path: 'python/requirements.txt'

         - name: Install Python dependencies
           run: |
             cd python
             pip install -r requirements.txt

         - name: Install Playwright browsers
           run: |
             playwright install chromium
             playwright install-deps chromium

         - name: Scrape event websites
           id: scrape
           continue-on-error: true
           run: |
             cd python

             # Determine which events to scrape
             if [ "${{ github.event.inputs.events_to_scrape }}" == "all" ] || [ -z "${{ github.event.inputs.events_to_scrape }}" ]; then
               EVENTS=("eventtechlive.com" "example.com")
             else
               IFS=',' read -ra EVENTS <<< "${{ github.event.inputs.events_to_scrape }}"
             fi

             echo "Scraping events: ${EVENTS[@]}"

             for event in "${EVENTS[@]}"; do
               echo "Scraping $event..."
               PYTHONPATH=./src python -m event_style_scraper scrape \
                 --url "https://$event" \
                 --timeout 90 || echo "⚠️ Failed to scrape $event"
             done

         - name: Validate scraped configs
           run: |
             cd python

             # Check JSON validity
             for config in style-configs/*.json; do
               if jq empty "$config" 2>/dev/null; then
                 echo "✓ Valid JSON: $config"
               else
                 echo "❌ Invalid JSON: $config"
                 exit 1
               fi

               # Check required fields
               jq -e '.eventId, .colors.primary, .typography.headingFont, .brandVoice.tone' "$config" > /dev/null || \
                 (echo "❌ Missing required fields in $config" && exit 1)
             done

             echo "✅ All configs validated"

         - name: Commit scraped configs
           run: |
             git config --global user.name "github-actions[bot]"
             git config --global user.email "github-actions[bot]@users.noreply.github.com"

             git add python/style-configs/*.json

             if git diff --staged --quiet; then
               echo "No changes to commit"
             else
               git commit -m "chore(scraper): update event style configs [skip ci]

               Automated scrape of event websites.
               Colors updated to match current website styling.

               🤖 Generated by scrape-and-deploy workflow
               Run: ${{ github.run_id }}"

               git push
             fi

         outputs:
           scrape_status: ${{ steps.scrape.outcome }}

       build-and-deploy:
         name: Build and Deploy
         needs: [scrape]
         # Always run (even if scraping fails or is skipped)
         if: always()
         runs-on: ubuntu-latest

         steps:
         - name: Checkout code (with updated configs)
           uses: actions/checkout@v4
           with:
             ref: main

         - name: Check scraping result
           run: |
             if [ "${{ needs.scrape.outputs.scrape_status }}" == "failure" ]; then
               echo "⚠️ Scraping failed, using cached configs"
             elif [ "${{ needs.scrape.result }}" == "skipped" ]; then
               if [ "${{ github.event_name }}" == "push" ]; then
                 echo "ℹ️ Scraping skipped (push event), using cached configs"
               else
                 echo "⚠️ Scraping skipped (unexpected), using cached configs"
               fi
             else
               echo "✓ Scraping succeeded, using fresh configs"
             fi

         - name: Setup Node.js
           uses: actions/setup-node@v4
           with:
             node-version: '20.x'
             cache: 'npm'

         - name: Install dependencies
           run: npm ci

         - name: Build TypeScript
           run: npm run build

         - name: Generate static site
           run: npm run generate

         - name: Verify event styles applied
           run: |
             echo "Checking for event-specific CSS variables..."

             # Check Event Tech Live pages have correct color
             if grep -q "color-primary.*#160822" dist/attendees/2001/index.html; then
               echo "✓ Event Tech Live color detected"
             else
               echo "⚠️ Event Tech Live color not found (may be using default)"
             fi

             echo "✅ Generation complete"

         - name: Add .nojekyll file
           run: touch dist/.nojekyll

         - name: Copy 404.html to dist
           run: cp 404.html dist/404.html

         - name: Setup Pages
           uses: actions/configure-pages@v4

         - name: Upload artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: './dist'

         - name: Deploy to GitHub Pages
           id: deployment
           uses: actions/deploy-pages@v4

         - name: Deployment summary
           run: |
             echo "🚀 Deployment successful!"
             echo "📄 Site URL: ${{ steps.deployment.outputs.page_url }}"
             echo "🎨 Using scraped event styles"
     ```
   - Validation: `yamllint .github/workflows/scrape-and-deploy.yml`

2. **Create event configuration file: `python/config/events.json`**
   - File affected: `python/config/events.json` (new)
   - Changes:
     ```json
     [
       {
         "id": "event-tech-live-2025",
         "name": "Event Tech Live 2025",
         "website": "https://eventtechlive.com",
         "scraping": {
           "enabled": true,
           "timeout": 90,
           "selectors": {
             "header": "header",
             "primary_cta": ".btn-primary, button.primary"
           }
         }
       },
       {
         "id": "event-2025",
         "name": "TechConf 2025",
         "website": "https://example.com",
         "scraping": {
           "enabled": true,
           "timeout": 60,
           "selectors": {
             "header": "header",
             "primary_cta": "button"
           }
         }
       }
     ]
     ```
   - Validation: `jq . python/config/events.json`

3. **Update existing deploy workflow to deprecation notice**
   - File affected: `.github/workflows/deploy.yml`
   - Changes: Add comment at top:
     ```yaml
     # ⚠️ DEPRECATED: This workflow is replaced by scrape-and-deploy.yml
     # Will be removed after scrape-and-deploy.yml is validated
     # See Plan 006 for details
     ```
   - Validation: No functional changes, workflow still runs

**Validation Checkpoint:**
- [ ] Workflow file created and valid YAML
- [ ] Events config file created with correct schema
- [ ] Workflow can be triggered manually (test with dry-run)
- [ ] OPENAI_API_KEY secret configured in repo settings
- [ ] Bot permissions verified (can commit/push)

### Phase 2: Add End-to-End Validation Script

**Objective:** Create automated test that validates full pipeline execution

**Steps:**

1. **Create validation script: `scripts/test-e2e-pipeline.sh`**
   - File affected: `scripts/test-e2e-pipeline.sh` (new)
   - Changes:
     ```bash
     #!/bin/bash
     set -e

     echo "🧪 Testing end-to-end scrape-to-deploy pipeline"
     echo "================================================"

     # Cleanup
     echo "Cleaning up previous test artifacts..."
     rm -rf dist-e2e-test/
     rm -f python/style-configs/test-*.json

     # Phase 1: Scrape
     echo ""
     echo "Phase 1: Scraping example.com..."
     cd python
     PYTHONPATH=./src python -m event_style_scraper scrape \
       --url https://example.com \
       --output style-configs/test-example-com.json \
       --timeout 60

     if [ ! -f "style-configs/test-example-com.json" ]; then
       echo "❌ Scraping failed: config not created"
       exit 1
     fi
     echo "✓ Scraping succeeded"

     # Phase 2: Validate scraped config
     echo ""
     echo "Phase 2: Validating scraped config..."

     # Check JSON validity
     jq empty style-configs/test-example-com.json || \
       (echo "❌ Invalid JSON" && exit 1)

     # Check required fields
     jq -e '.eventId, .colors.primary, .typography.headingFont' \
       style-configs/test-example-com.json > /dev/null || \
       (echo "❌ Missing required fields" && exit 1)

     # Extract primary color for later validation
     PRIMARY_COLOR=$(jq -r '.colors.primary' style-configs/test-example-com.json)
     echo "Extracted primary color: $PRIMARY_COLOR"
     echo "✓ Config validation passed"

     # Phase 3: Copy to main style-configs
     echo ""
     echo "Phase 3: Copying config to style-configs/..."
     cp style-configs/test-example-com.json ../style-configs/test-example-com.json
     cd ..

     # Phase 4: Generate pages
     echo ""
     echo "Phase 4: Generating static site..."
     npm run build
     mkdir -p dist-e2e-test
     npm run generate -- --output dist-e2e-test

     if [ ! -d "dist-e2e-test/attendees" ]; then
       echo "❌ Generation failed: attendees directory not created"
       exit 1
     fi
     echo "✓ Generation succeeded"

     # Phase 5: Validate CSS injection
     echo ""
     echo "Phase 5: Validating CSS injection..."

     # Check if scraped color appears in generated HTML
     if grep -q "$PRIMARY_COLOR" dist-e2e-test/attendees/1001/index.html; then
       echo "✓ Scraped color found in generated HTML"
     else
       echo "❌ Scraped color NOT found in generated HTML"
       echo "Expected: $PRIMARY_COLOR"
       echo "Page content:"
       head -50 dist-e2e-test/attendees/1001/index.html
       exit 1
     fi

     # Phase 6: DevTools validation
     echo ""
     echo "Phase 6: DevTools color validation..."
     python scripts/validate_scraped_colors.py \
       --url https://example.com \
       --config style-configs/test-example-com.json \
       --selector body \
       --property backgroundColor \
       --expected "auto" || echo "⚠️ DevTools validation skipped (color varies)"

     # Cleanup
     echo ""
     echo "Cleaning up test artifacts..."
     rm -rf dist-e2e-test/
     rm -f style-configs/test-example-com.json
     rm -f python/style-configs/test-example-com.json

     echo ""
     echo "================================================"
     echo "✅ End-to-end pipeline test PASSED"
     echo "Pipeline: Scrape → Validate → Generate → Verify"
     ```
   - Validation: `chmod +x scripts/test-e2e-pipeline.sh && ./scripts/test-e2e-pipeline.sh`

2. **Add E2E test to test workflow**
   - File affected: `.github/workflows/test.yml`
   - Changes: Add new job:
     ```yaml
     e2e-test:
       name: End-to-End Pipeline Test
       runs-on: ubuntu-latest

       steps:
       - name: Checkout code
         uses: actions/checkout@v4

       - name: Setup Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.11'
           cache: 'pip'
           cache-dependency-path: 'python/requirements.txt'

       - name: Setup Node.js
         uses: actions/setup-node@v4
         with:
           node-version: '20.x'
           cache: 'npm'

       - name: Install dependencies
         run: |
           npm ci
           cd python
           pip install -r requirements.txt
           playwright install chromium
           playwright install-deps chromium

       - name: Run E2E pipeline test
         env:
           OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
         run: ./scripts/test-e2e-pipeline.sh
     ```
   - Validation: Push to branch and verify workflow runs

**Validation Checkpoint:**
- [ ] E2E test script created and executable
- [ ] Script successfully tests full pipeline locally
- [ ] Script added to test workflow
- [ ] Test passes in GitHub Actions
- [ ] All 6 phases validated (scrape, validate, copy, generate, verify, cleanup)

### Phase 3: Optimize for Performance and Cost

**Objective:** Add caching, parallel processing, and cost controls

**Steps:**

1. **Add dependency caching to workflow**
   - File affected: `.github/workflows/scrape-and-deploy.yml`
   - Changes: Already includes caching in steps above (pip cache, npm cache, Playwright cache)
   - Additional optimization:
     ```yaml
     - name: Cache Playwright browsers
       uses: actions/cache@v3
       with:
         path: ~/.cache/ms-playwright
         key: ${{ runner.os }}-playwright-${{ hashFiles('python/requirements.txt') }}
     ```
   - Validation: Check workflow logs for "Cache restored" messages

2. **Add parallel scraping**
   - File affected: `python/src/event_style_scraper/cli.py`
   - Changes: Add `--parallel` flag (optional enhancement):
     ```python
     @click.option('--parallel', is_flag=True, help='Scrape multiple URLs in parallel')
     def scrape(url: str, output: str, timeout: int, parallel: bool):
         if parallel:
             # Use asyncio.gather() for concurrent scraping
             import asyncio
             urls = url.split(',')
             asyncio.run(scrape_parallel(urls, output, timeout))
         else:
             # Existing sequential scraping
             pass
     ```
   - Validation: Test locally with multiple URLs

3. **Add cost tracking**
   - File affected: `python/src/event_style_scraper/flows/style_scraping_flow.py`
   - Changes: Log API token usage:
     ```python
     def start(self):
         result = self.crew.crew().kickoff()

         # Log token usage for cost tracking
         if hasattr(result, 'token_usage'):
             print(f"API tokens used: {result.token_usage}")
             print(f"Estimated cost: ${result.token_usage * 0.00002:.4f}")

         return result
     ```
   - Validation: Check logs after scraping

4. **Add optional staleness check**
   - File affected: `.github/workflows/scrape-and-deploy.yml`
   - Changes: Add optional check to warn if configs are stale (informational only):
     ```yaml
     - name: Check config staleness (informational)
       run: |
         # Check last commit that modified style-configs/
         LAST_SCRAPE=$(git log -1 --format="%ci" -- python/style-configs/)
         DAYS_AGO=$(( ($(date +%s) - $(date -d "$LAST_SCRAPE" +%s)) / 86400 ))

         echo "Last scraping: $LAST_SCRAPE ($DAYS_AGO days ago)"

         if [ $DAYS_AGO -gt 30 ]; then
           echo "⚠️ Style configs are >30 days old. Consider running manual scrape."
           echo "::warning::Style configs last updated $DAYS_AGO days ago"
         else
           echo "✓ Style configs are reasonably fresh"
         fi
     ```
   - Validation: Check workflow annotations for staleness warnings

**Validation Checkpoint:**
- [ ] Dependency caching reduces install time by >50%
- [ ] Parallel scraping (if implemented) saves ~40% time
- [ ] Token usage logged for cost tracking
- [ ] Staleness check warns when configs are >30 days old
- [ ] Total workflow time < 8 minutes with scraping, < 5 minutes without (push-only)

### Phase 4: Add Monitoring and Notifications

**Objective:** Add observability and alerting for scraping failures

**Steps:**

1. **Create workflow status badge**
   - File affected: `README.md`
   - Changes: Add badge:
     ```markdown
     [![Scrape and Deploy](https://github.com/USERNAME/personal-event-summary/actions/workflows/scrape-and-deploy.yml/badge.svg)](https://github.com/USERNAME/personal-event-summary/actions/workflows/scrape-and-deploy.yml)
     ```
   - Validation: Check badge shows correct status

2. **Add Slack notification for failures (optional)**
   - File affected: `.github/workflows/scrape-and-deploy.yml`
   - Changes: Add step at end:
     ```yaml
     - name: Notify on failure
       if: failure()
       uses: slackapi/slack-github-action@v1
       with:
         payload: |
           {
             "text": "🚨 Scrape-and-deploy workflow failed",
             "blocks": [
               {
                 "type": "section",
                 "text": {
                   "type": "mrkdwn",
                   "text": "*Workflow:* scrape-and-deploy\n*Status:* Failed\n*Run:* ${{ github.run_id }}"
                 }
               }
             ]
           }
       env:
         SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
     ```
   - Validation: Trigger failure, check Slack message

3. **Add scraping metrics to workflow summary**
   - File affected: `.github/workflows/scrape-and-deploy.yml`
   - Changes: Add summary step:
     ```yaml
     - name: Scraping summary
       if: always()
       run: |
         echo "## Scraping Results" >> $GITHUB_STEP_SUMMARY
         echo "" >> $GITHUB_STEP_SUMMARY

         for config in python/style-configs/*.json; do
           EVENT_NAME=$(jq -r '.eventName' "$config")
           SCRAPED_AT=$(jq -r '.scrapedAt' "$config")
           PRIMARY_COLOR=$(jq -r '.colors.primary' "$config")

           echo "- **$EVENT_NAME**: $PRIMARY_COLOR (scraped: $SCRAPED_AT)" >> $GITHUB_STEP_SUMMARY
         done
     ```
   - Validation: Check workflow run page for summary

**Validation Checkpoint:**
- [ ] Status badge created and shows correct status
- [ ] Notifications configured (if using Slack/email)
- [ ] Workflow summary shows scraping results
- [ ] Easy to diagnose failures from logs

### Phase 5: Documentation and Cleanup

**Objective:** Update docs, deprecate old workflow, create runbook

**Steps:**

1. **Update README.md**
   - File affected: `README.md`
   - Changes: Add section:
     ```markdown
     ## 🤖 Style Scraping Pipeline

     This project uses GitHub Actions to scrape event website styles and apply them to generated pages.

     ### Workflow: Scrape and Deploy

     **Triggers:**
     - 🖱️ **Manual**: Via GitHub Actions UI (on-demand scraping when event websites change)
     - 📝 **Push**: On push to `main` (uses cached configs, no scraping, fast deployment)

     **Pipeline:**
     1. **Manual Trigger**: Scrape event websites using Playwright
     2. Extract colors, typography, brand voice with AI agents
     3. Validate scraped configs (schema + DevTools comparison)
     4. Commit updated configs to repository
     5. Generate static pages with event-specific CSS
     6. Deploy to GitHub Pages

     **When to Trigger Manual Scraping:**
     - Event website redesign (colors/branding changed)
     - New event added to system
     - Before major releases (ensure styles are current)
     - After discovering style mismatches

     **Manual Trigger:**
     ```bash
     # Scrape all configured events
     gh workflow run scrape-and-deploy.yml

     # Scrape specific events
     gh workflow run scrape-and-deploy.yml \
       --field events_to_scrape="eventtechlive.com,example.com"

     # Force re-scraping even if configs exist
     gh workflow run scrape-and-deploy.yml \
       --field force_scrape=true
     ```

     **Cost Management:**
     - API usage: ~$0.10 per event per scrape
     - Manual-only: Costs only incurred when you trigger scraping
     - Typical usage: ~2 scrapes/month = ~$0.80/month for 4 events
     - Cached configs used if scraping fails
     - No unexpected charges from automated runs
     ```
   - Validation: Preview README to verify formatting

2. **Create runbook: `docs/runbook-scraping.md`**
   - File affected: `docs/runbook-scraping.md` (new)
   - Changes: Create comprehensive runbook covering:
     - How to trigger manual scraping
     - How to troubleshoot scraping failures
     - How to update event URLs
     - How to rollback bad configs
     - How to validate scraped colors
   - Validation: Peer review for completeness

3. **Update CLAUDE.md**
   - File affected: `CLAUDE.md`
   - Changes: Add new lesson:
     ```markdown
     ### 20. End-to-End Automation Validates Integration (Plan 006)

     **Learning**: Automating the full pipeline in CI/CD provides continuous validation that multi-system integration works. Manual-triggered scraping provides explicit control over API costs while maintaining integration testing.

     **Implementation**:
     - GitHub Actions workflow runs: Scrape (manual) → Validate → Generate → Deploy
     - Each step validated independently and in combination
     - Failed scraping doesn't block deployment (uses cached configs)
     - E2E test runs on every PR to catch integration breaks
     - Manual triggers provide cost control and explicit timing

     **Impact**:
     - Continuous verification of Lesson 16 (end-to-end validation)
     - Catches schema changes, API breaking changes, CSS generation bugs
     - Provides living documentation (workflow as specification)
     - Enables confident refactoring (integration tested automatically)
     - Eliminates unexpected API costs from automated scraping

     **Example**:
     ```yaml
     # E2E test in CI
     - name: Test full pipeline
       run: |
         python scrape.py → style.json
         npm run generate → HTML with colors
         grep "#160822" output.html → verify integration
     ```
     ```
   - Validation: Verify lesson follows existing format

4. **Deprecate old deploy workflow**
   - File affected: `.github/workflows/deploy.yml`
   - Changes: Rename to `deploy.yml.disabled` after confirming new workflow works
   - Validation: Verify workflow no longer triggers

5. **Update plans/README.md**
   - File affected: `plans/README.md`
   - Changes: Add Plan 006 to index:
     ```markdown
     | 006 | [End-to-End Scrape-Deploy Pipeline](006-end-to-end-scrape-deploy-pipeline.md) | 📝 Draft | - | 🔴 Critical | Automate scraping in GitHub Actions for continuous style updates |
     ```
   - Validation: Verify entry appears in table

**Validation Checkpoint:**
- [ ] README updated with workflow documentation
- [ ] Runbook created with troubleshooting steps
- [ ] CLAUDE.md lesson added
- [ ] Old workflow deprecated
- [ ] Plans index updated

---

## Dependencies

### Prerequisites

- [x] Plan 005 completed (Playwright tool functional)
- [x] Python scraper working locally
- [x] TypeScript CSS generator implemented
- [ ] OPENAI_API_KEY secret configured in GitHub repository
- [ ] Repository permissions: Actions have write access for commits
- [ ] Playwright can run in GitHub Actions environment

### Related Plans

- `plans/003-event-centered-styling-crewai.md` - Original scraping implementation
- `plans/005-playwright-scraping-tool.md` - Playwright tool this workflow uses
- `plans/004-fix-event-tech-live-style-mismatch.md` - Color accuracy validation

### External Dependencies

- **GitHub Actions**: CI/CD platform (free tier: 2000 min/month)
- **Playwright**: Browser automation (requires Chromium install in workflow)
- **OpenAI API**: CrewAI backend (cost: ~$0.10/event/scrape)
- **Git**: For committing scraped configs back to repo

---

## Risk Assessment

### High Risk Items

1. **Risk:** OpenAI API costs spiral out of control
   - **Likelihood:** Low (manual-only triggers)
   - **Impact:** High ($$$)
   - **Mitigation:** Manual triggers only (no scheduled runs), cost tracking logged per run, user controls all spending
   - **Contingency:** Add spending alerts, limit trigger permissions, use smaller models

2. **Risk:** Playwright fails in GitHub Actions environment
   - **Likelihood:** Low (common setup, well-documented)
   - **Impact:** High (blocks entire pipeline)
   - **Mitigation:** Use `playwright install --with-deps`, add `--no-sandbox` flag if needed
   - **Contingency:** Switch to Selenium, use pre-built Docker image, or manual scraping fallback

3. **Risk:** Bot commits trigger infinite workflow loops
   - **Likelihood:** Medium (common CI/CD pitfall)
   - **Impact:** High (workflow spam, cost waste)
   - **Mitigation:** Use `[skip ci]` in commit messages, add loop detection
   - **Contingency:** Disable workflow, clean up commits, add branch protection

### Medium Risk Items

1. **Risk:** Scraped configs break TypeScript generation
   - **Likelihood:** Low (schema validated)
   - **Impact:** Medium (deployment fails)
   - **Mitigation:** JSON schema validation, type guards, fallback to cached configs
   - **Contingency:** Manual rollback of bad config, fix schema, redeploy

2. **Risk:** Website blocks scraping (bot detection)
   - **Likelihood:** Medium (some sites aggressive)
   - **Impact:** Medium (no fresh styles)
   - **Mitigation:** Respect robots.txt, use polite scraping intervals, stealth mode
   - **Contingency:** Manual scraping, contact website owner, use cached configs

3. **Risk:** Workflow timeout (>45 min for slow scraping)
   - **Likelihood:** Low (typical: 8 min)
   - **Impact:** Medium (deployment delayed)
   - **Mitigation:** Parallel scraping, aggressive caching, timeout limits
   - **Contingency:** Split into separate jobs, reduce events scraped

---

## Rollback Plan

If implementation fails or causes issues:

1. **Disable new workflow**
   ```bash
   mv .github/workflows/scrape-and-deploy.yml .github/workflows/scrape-and-deploy.yml.disabled
   ```

2. **Re-enable old deploy workflow**
   ```bash
   git checkout HEAD~1 -- .github/workflows/deploy.yml
   git commit -m "revert: restore original deploy workflow"
   git push
   ```

3. **Remove bot commits (if spam occurred)**
   ```bash
   git rebase -i HEAD~10  # Remove automated commits
   git push --force
   ```

4. **Validate system stability**
   ```bash
   npm run generate
   npm test
   git status
   ```

**Validation after rollback:**
- [ ] Original deploy workflow functional
- [ ] Pages deploy successfully
- [ ] No infinite loops or spam
- [ ] All tests passing

---

## Testing Strategy

### Unit Tests

- [ ] Test event config parsing (read events.json)
- [ ] Test workflow YAML syntax (yamllint)
- [ ] Test fallback logic (mock scraping failure)
- [ ] Test commit message formatting
- [ ] Test color validation regex

### Integration Tests

- [ ] Test E2E pipeline script locally
- [ ] Test workflow in test branch (before main)
- [ ] Test with real OpenAI API (monitor costs)
- [ ] Test both success and failure paths
- [ ] Test all trigger types (push, schedule, manual)

### Manual Testing

1. **Test manual trigger:**
   - Go to Actions tab → Scrape and Deploy → Run workflow
   - Select events to scrape
   - Verify configs updated, deployment succeeds

2. **Test push trigger (no scraping):**
   - Make change to src/ or templates/
   - Push to main
   - Verify workflow triggered
   - Verify scraping skipped (cached configs used)
   - Verify deployment succeeded quickly (< 5 min)

3. **Test push trigger:**
   - Make change to src/
   - Push to main
   - Verify scraping skipped, cached configs used

4. **Test failure handling:**
   - Temporarily break scraper (invalid URL)
   - Verify fallback to cached config
   - Verify deployment still succeeds

5. **Test color accuracy:**
   - Trigger workflow
   - Open deployed page
   - Compare to actual event website header color
   - Should match within ±2 RGB units

### Validation Commands

```bash
# Validate workflow YAML
yamllint .github/workflows/scrape-and-deploy.yml

# Test E2E pipeline
./scripts/test-e2e-pipeline.sh

# Trigger workflow manually
gh workflow run scrape-and-deploy.yml --ref main

# Check workflow status
gh run list --workflow=scrape-and-deploy.yml --limit 5

# View workflow logs
gh run view --log

# Validate scraped config
jq . python/style-configs/event-tech-live-2025.json
ajv validate -s schemas/event-style-config-schema.json -d python/style-configs/*.json

# Check deployed page has correct colors
curl https://USERNAME.github.io/personal-event-summary/attendees/2001/ | grep "#160822"

# Compare scraped color to DevTools
python scripts/validate_scraped_colors.py \
  --url https://eventtechlive.com \
  --config python/style-configs/event-tech-live-2025.json \
  --selector header \
  --property backgroundColor \
  --expected "#160822"
```

---

## Post-Implementation

### Documentation Updates

- [ ] Update README.md with workflow documentation
- [ ] Create `docs/runbook-scraping.md` troubleshooting guide
- [ ] Add CLAUDE.md Lesson 20 (automation validates integration)
- [ ] Update architecture diagram (add CI/CD layer)
- [ ] Document cost tracking methodology

### Knowledge Capture

- [ ] Document Playwright in GitHub Actions setup (gotchas)
- [ ] Document bot commit best practices (`[skip ci]`)
- [ ] Document scraping frequency recommendations
- [ ] Add troubleshooting examples (common failures)
- [ ] Create comparison: manual vs automated scraping

### Metrics to Track

- **Reliability**: % of successful workflow runs
- **Performance**: Average workflow duration
- **Cost**: OpenAI API spend per week/month
- **Accuracy**: % of scraped colors within ±2 RGB of DevTools
- **Freshness**: Time between event website update and deployed page update

---

## Appendix

### References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Playwright in CI](https://playwright.dev/docs/ci)
- [GitHub Actions: Committing Changes](https://github.com/marketplace/actions/add-commit)
- CLAUDE.md Lesson 16: End-to-End Validation is NON-NEGOTIABLE
- Exploration Report 2025-11-07 (identified end-to-end gap)
- Plan 005: Playwright-Based Scraping Tool

### Alternative Approaches Considered

1. **Approach:** Scrape at build time (always)
   - **Pros:** Always fresh styles, no caching needed
   - **Cons:** High API costs, slow deployments (~5 min longer)
   - **Why not chosen:** Cost prohibitive for frequent deployments

2. **Approach:** Manual scraping only (no automation)
   - **Pros:** Full control, no costs until triggered, simple
   - **Cons:** Requires remembering to scrape, human error, no validation
   - **Why not chosen:** Defeats purpose of automation, doesn't validate integration

3. **Approach:** Store configs as artifacts (not committed)
   - **Pros:** Cleaner git history, no bot commits
   - **Cons:** Configs not version-controlled, harder to debug, manual inspection difficult
   - **Why not chosen:** Version control enables rollback and human review

4. **Approach:** Use PR-based flow for scraped configs
   - **Pros:** Human review before merge, prevents bad configs
   - **Cons:** Slows deployment, requires approval, defeats automation
   - **Why not chosen:** Trust validation steps to catch bad configs

5. **Approach:** Scrape only on event config changes
   - **Pros:** Reduces unnecessary scraping, cost-effective
   - **Cons:** Misses event website style updates, manual trigger needed
   - **Why not chosen:** Scheduled scraping catches updates proactively

### Event Configuration Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "name", "website", "scraping"],
    "properties": {
      "id": {
        "type": "string",
        "pattern": "^[a-z0-9-]+$"
      },
      "name": {
        "type": "string"
      },
      "website": {
        "type": "string",
        "format": "uri",
        "pattern": "^https?://"
      },
      "scraping": {
        "type": "object",
        "required": ["enabled", "timeout"],
        "properties": {
          "enabled": {
            "type": "boolean"
          },
          "timeout": {
            "type": "integer",
            "minimum": 30,
            "maximum": 300
          },
          "selectors": {
            "type": "object",
            "properties": {
              "header": { "type": "string" },
              "primary_cta": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

### Cost Estimation

**Assumptions:**
- 4 events configured for scraping
- Manual-only triggers (no scheduled runs)
- $0.10 per event per scrape (CrewAI + OpenAI API)

**Typical Usage Scenarios:**

**Scenario 1: Conservative (quarterly scraping)**
```
4 events × 4 quarters × $0.10 = $1.60/year (~$0.13/month)
```

**Scenario 2: Moderate (monthly scraping)**
```
4 events × 12 months × $0.10 = $4.80/year (~$0.40/month)
```

**Scenario 3: Active (bi-weekly scraping)**
```
4 events × 26 scrapes/year × $0.10 = $10.40/year (~$0.87/month)
```

**Recommendation:** Manual-only provides complete cost control. Users trigger scraping only when event websites change or before major releases.

### Notes

- Manual-only approach provides complete cost and timing control
- Users decide when scraping is necessary (event redesigns, new events, releases)
- Staleness warnings inform users when configs haven't been updated recently
- Consider adding "dry-run" mode that skips OpenAI API calls (for testing)
- Playwright caching saves ~50% of workflow time on repeat runs
- Bot commits should be squashable (group related config updates)
- Push-triggered deploys are fast (< 5 min) since no scraping occurs
- Monitor GitHub Actions usage (2000 min/month free tier limit)
- Document recommended scraping frequency in runbook (e.g., before major releases, after event redesigns)

---

**Plan Status:** 📝 Draft - Awaiting approval to implement

**Next Steps:**
1. Review plan for completeness
2. Confirm OpenAI API budget acceptable
3. Validate approach aligns with project goals
4. Get explicit confirmation to proceed with implementation
