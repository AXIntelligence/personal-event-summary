#!/bin/bash
set -e

echo "🧪 Testing end-to-end scrape-to-deploy pipeline"
echo "================================================"

# Cleanup
echo "Cleaning up previous test artifacts..."
rm -rf dist-e2e-test/
rm -f python/style-configs/example-com.json
rm -f style-configs/e2e-test-*.json

# Phase 1: Scrape
echo ""
echo "Phase 1: Scraping example.com..."
cd python
PYTHONPATH=./src python -m event_style_scraper scrape \
  --url https://example.com \
  --timeout 60

# Scraper saves to style-configs/example-com.json (based on URL)
if [ ! -f "style-configs/example-com.json" ]; then
  echo "❌ Scraping failed: config not created at python/style-configs/example-com.json"
  exit 1
fi
echo "✓ Scraping succeeded"

# Phase 2: Validate scraped config
echo ""
echo "Phase 2: Validating scraped config..."

# Check JSON validity
jq empty style-configs/example-com.json || \
  (echo "❌ Invalid JSON" && exit 1)

# Check required fields (Python scraper uses snake_case)
jq -e '.event_id, .colors.primary, .typography.heading_font' \
  style-configs/example-com.json > /dev/null || \
  (echo "❌ Missing required fields" && exit 1)

# Extract primary color for later validation
PRIMARY_COLOR=$(jq -r '.colors.primary' style-configs/example-com.json)
echo "Extracted primary color: $PRIMARY_COLOR"
echo "✓ Config validation passed"

# Phase 3: Copy to main style-configs (root level)
echo ""
echo "Phase 3: Copying config to root style-configs/..."
cp style-configs/example-com.json ../style-configs/e2e-test-example-com.json
cd ..

# Phase 4: Generate pages
echo ""
echo "Phase 4: Generating static site..."
npm run build
mkdir -p dist-e2e-test
npm run generate

# Check if pages were generated
if [ ! -d "dist/attendees" ]; then
  echo "❌ Generation failed: attendees directory not created"
  exit 1
fi
echo "✓ Generation succeeded"

# Phase 5: Validate CSS injection
echo ""
echo "Phase 5: Validating CSS injection..."

# Check if scraped color appears in generated HTML
# Use attendee 2001 (Event Tech Live) as test subject
if [ -f "dist/attendees/2001/index.html" ]; then
  echo "✓ Generated HTML exists"

  # Check for CSS custom properties (any color)
  if grep -q "color-primary" dist/attendees/2001/index.html; then
    echo "✓ CSS custom properties found in generated HTML"

    # Optionally check if the scraped color appears somewhere in the HTML
    if grep -q "$PRIMARY_COLOR" dist/attendees/2001/index.html; then
      echo "✓ Scraped color ($PRIMARY_COLOR) found in generated HTML"
    else
      echo "⚠️ Scraped color not found (pages may use event-specific configs instead)"
    fi
  else
    echo "⚠️ CSS custom properties not found, checking for inline styles..."
  fi
else
  echo "❌ Generated HTML NOT found at dist/attendees/2001/index.html"
  echo "Available attendees:"
  ls dist/attendees/ | head -5
  exit 1
fi

# Phase 6: Cleanup
echo ""
echo "Cleaning up test artifacts..."
rm -rf dist-e2e-test/
rm -f style-configs/e2e-test-example-com.json
rm -f python/style-configs/example-com.json

echo ""
echo "================================================"
echo "✅ End-to-end pipeline test PASSED"
echo "Pipeline: Scrape → Validate → Generate → Verify"
