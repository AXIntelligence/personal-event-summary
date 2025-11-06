# Setup Guide

Complete setup instructions for the Personal Event Summary project.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Project Configuration](#project-configuration)
- [Adding Event and Attendee Data](#adding-event-and-attendee-data)
- [Running Tests](#running-tests)
- [Building and Generating](#building-and-generating)
- [GitHub Pages Deployment](#github-pages-deployment)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Node.js** (v18.x or v20.x)
   ```bash
   # Check version
   node --version

   # Should output: v18.x.x or v20.x.x
   ```

   **Installation**:
   - macOS: `brew install node@20`
   - Ubuntu: `sudo apt install nodejs npm`
   - Windows: Download from [nodejs.org](https://nodejs.org/)

2. **npm** (v9.x or higher)
   ```bash
   # Check version
   npm --version

   # Should output: 9.x.x or higher
   ```

3. **Git**
   ```bash
   # Check version
   git --version
   ```

### Recommended Tools

- **VS Code** with extensions:
  - TypeScript and JavaScript Language Features
  - Handlebars
  - ESLint
  - Prettier

## Local Development Setup

### 1. Clone the Repository

```bash
# Clone via HTTPS
git clone https://github.com/USERNAME/personal-event-summary.git

# Or via SSH
git clone git@github.com:USERNAME/personal-event-summary.git

# Navigate to project directory
cd personal-event-summary
```

### 2. Install Dependencies

```bash
# Install all npm dependencies
npm install

# Expected output:
# added XXX packages in Xs
```

**Common npm install issues**:
- If you get EACCES errors, don't use `sudo`. Instead:
  ```bash
  mkdir -p .npm-cache
  npm install --cache .npm-cache
  ```

### 3. Verify Installation

```bash
# Check that TypeScript is installed
npx tsc --version
# Should output: Version 5.9.3

# Check that Vitest is installed
npx vitest --version
# Should output: Vitest v1.6.1 or higher
```

### 4. Build TypeScript

```bash
# Compile TypeScript to JavaScript
npm run build

# Expected output:
# (no errors = successful compilation)

# Verify dist directory was created
ls dist/
# Should show: dataLoader.js  generate.js  types/
```

### 5. Run Tests

```bash
# Run all tests
npm test

# Expected output:
# ✓ tests/unit/dataLoader.test.ts  (21 tests)
# ✓ tests/unit/generate.test.ts  (31 tests)
# ✓ tests/integration/endToEnd.test.ts  (21 tests)
# ✓ tests/validation/htmlValidation.test.ts  (14 tests)
#
# Test Files  4 passed (4)
# Tests  87 passed (87)
```

### 6. Generate Static Site

```bash
# Generate all attendee pages
npm run generate

# Expected output:
# Starting page generation...
#
# Generating pages for 12 attendees...
# ✓ Generated 12 attendee pages
# ✓ Copied static assets
#
# ✅ Generation complete!
#    Pages generated: 12
#    Output directory: /path/to/personal-event-summary/dist
```

### 7. View Generated Pages

Open generated pages in your browser:

```bash
# macOS
open dist/attendees/1001/index.html

# Linux
xdg-open dist/attendees/1001/index.html

# Windows
start dist/attendees/1001/index.html
```

Or use a local server:

```bash
# Install a simple HTTP server (if not already installed)
npm install -g http-server

# Serve the dist directory
http-server dist -p 8080

# Open in browser: http://localhost:8080/attendees/1001/
```

## Project Configuration

### Directory Structure

After setup, your project should look like this:

```
personal-event-summary/
├── node_modules/          # Dependencies (gitignored)
├── dist/                  # Generated output (gitignored)
│   ├── attendees/
│   │   ├── 1001/
│   │   │   └── index.html
│   │   └── ...
│   └── static/
│       └── css/
│           └── styles.css
├── data/                  # Source data
│   ├── events/
│   │   └── event-2025.json
│   └── attendees/
│       ├── 1001.json
│       └── ...
├── src/                   # TypeScript source
│   ├── dataLoader.ts
│   ├── generate.ts
│   └── types/
│       └── index.ts
├── templates/             # Handlebars templates
│   ├── layouts/
│   ├── pages/
│   └── partials/
├── static/                # Static assets
│   ├── css/
│   └── images/
└── tests/                 # Test files
    ├── unit/
    ├── integration/
    └── validation/
```

### Environment Variables

This project doesn't require environment variables for basic operation. If you need to add environment variables:

1. Create `.env` file in project root
2. Add variables:
   ```
   NODE_ENV=development
   CUSTOM_VAR=value
   ```
3. Update `.gitignore` to include `.env`

## Adding Event and Attendee Data

### Adding a New Event

1. Create JSON file in `data/events/`:
   ```bash
   cp data/events/event-2025.json data/events/event-2026.json
   ```

2. Edit the file with event details:
   ```json
   {
     "id": "event-2026",
     "name": "TechConf 2026",
     "startDate": "2026-03-15T09:00:00Z",
     "endDate": "2026-03-17T18:00:00Z",
     "venue": {
       "name": "Moscone Center",
       "city": "San Francisco",
       "state": "CA",
       "country": "USA"
     },
     "stats": {
       "totalAttendees": 5500,
       "totalSessions": 150
     }
   }
   ```

### Adding Attendees

1. Create JSON file in `data/attendees/`:
   ```bash
   # Copy template
   cp data/attendees/1001.json data/attendees/2001.json
   ```

2. Edit with attendee details:
   ```json
   {
     "id": "2001",
     "firstName": "Jane",
     "lastName": "Doe",
     "email": "jane.doe@example.com",
     "company": "Acme Corp",
     "title": "Senior Engineer",
     "eventId": "event-2026",
     "achievement": "Early Bird Attendee",
     "registeredAt": "2026-01-15T10:00:00Z",
     "sessions": [...],
     "connections": [...],
     "stats": {...},
     "callsToAction": [...]
   }
   ```

3. Regenerate pages:
   ```bash
   npm run build
   npm run generate
   ```

### Data Validation

The system automatically validates all data:

```bash
# Run tests to verify data integrity
npm test tests/unit/dataLoader.test.ts

# If validation fails, check error messages for details
```

## Running Tests

### All Tests

```bash
# Run complete test suite
npm test

# Run with coverage
npm run test:coverage

# Run with detailed output
npm test -- --reporter=verbose
```

### Specific Test Suites

```bash
# Unit tests only
npm test tests/unit/

# Integration tests only
npm test tests/integration/

# HTML validation only
npm test tests/validation/

# Specific file
npm test tests/unit/dataLoader.test.ts
```

### Watch Mode

```bash
# Run tests in watch mode (re-run on file changes)
npx vitest watch
```

### Test Coverage

```bash
# Generate coverage report
npm run test:coverage

# View HTML coverage report
open coverage/index.html  # macOS
xdg-open coverage/index.html  # Linux
```

**Coverage targets**:
- Minimum: 70%
- Target: 80%
- Current: 85.42% ✅

## Building and Generating

### Development Build

```bash
# Build TypeScript (watch mode)
npx tsc --watch

# In another terminal, regenerate on changes
npm run generate
```

### Production Build

```bash
# Clean build
rm -rf dist/
npm run build
npm run generate
```

### Type Checking

```bash
# Check types without compiling
npm run type-check

# Expected output: (no errors = success)
```

### Performance Testing

```bash
# Time the generation process
time npm run generate

# Should complete in < 2 seconds for 12 pages
```

## GitHub Pages Deployment

### Initial Setup

1. **Push to GitHub**:
   ```bash
   git remote add origin git@github.com:USERNAME/personal-event-summary.git
   git branch -M main
   git push -u origin main
   ```

2. **Configure GitHub Pages**:
   - See [github-pages-setup.md](github-pages-setup.md) for detailed instructions
   - Set source to "GitHub Actions"
   - Ensure workflow permissions are correct

3. **Verify Deployment**:
   - Go to Actions tab
   - Watch deploy workflow run
   - Visit site URL: `https://USERNAME.github.io/personal-event-summary/`

### Manual Deployment Trigger

```bash
# Via GitHub CLI
gh workflow run deploy.yml

# Or via web interface: Actions → Deploy to GitHub Pages → Run workflow
```

### Deployment Verification

After deployment:

```bash
# Test key URLs (replace USERNAME/REPO)
curl -I https://USERNAME.github.io/REPO/attendees/1001/
# Should return: HTTP/2 200

curl -I https://USERNAME.github.io/REPO/static/css/styles.css
# Should return: HTTP/2 200
```

## Troubleshooting

### Installation Issues

**Problem**: npm install fails with EACCES errors

**Solution**:
```bash
mkdir -p .npm-cache
npm install --cache .npm-cache
```

---

**Problem**: TypeScript compilation fails

**Solution**:
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript version
npx tsc --version

# Rebuild
npm run build
```

### Test Failures

**Problem**: Tests fail after code changes

**Solution**:
```bash
# Clean test artifacts
rm -rf dist-test/ dist-integration-test/ dist-validation-test/

# Rebuild and test
npm run build
npm test
```

---

**Problem**: HTML validation tests fail

**Solution**:
1. Check generated HTML in `dist/attendees/`
2. Validate manually at [validator.w3.org](https://validator.w3.org/)
3. Fix template issues in `templates/`
4. Regenerate and test

### Generation Issues

**Problem**: No pages generated

**Solution**:
```bash
# Check for data files
ls data/attendees/
# Should show: 1001.json, 1002.json, ...

# Check for build output
ls dist/
# Should show: dataLoader.js, generate.js

# Rebuild
npm run build
npm run generate
```

---

**Problem**: CSS not loading in generated pages

**Solution**:
```bash
# Verify CSS file exists
ls static/css/styles.css

# Check that it's copied to dist
ls dist/static/css/styles.css

# If missing, regenerate
npm run generate
```

### GitHub Pages Issues

**Problem**: 404 errors on GitHub Pages

**Solution**:
1. Verify `.nojekyll` exists:
   ```bash
   ls dist/.nojekyll
   ```
2. Check workflow logs in Actions tab
3. Ensure Pages source is "GitHub Actions" not "Deploy from a branch"
4. Clear browser cache and retry

---

**Problem**: Workflow fails with permission errors

**Solution**:
1. Go to Settings → Actions → General
2. Set Workflow permissions to "Read and write permissions"
3. Re-run failed workflow

### Performance Issues

**Problem**: Generation takes too long

**Solution**:
```bash
# Profile generation
time npm run generate

# If > 2 seconds for 12 pages:
# 1. Check for large image files in static/
# 2. Review template complexity
# 3. Check disk I/O performance
```

## Advanced Configuration

### Custom Handlebars Helpers

Add helpers in `src/generate.ts`:

```typescript
hbs.registerHelper('customHelper', (value: string) => {
  return value.toUpperCase();
});
```

### Custom CSS Themes

1. Duplicate `static/css/styles.css`
2. Modify CSS variables:
   ```css
   :root {
     --color-primary: #your-color;
     --font-family: 'Your Font', sans-serif;
   }
   ```
3. Update template to reference new CSS

### Adding Analytics

Add to `templates/layouts/base.hbs`:

```html
<head>
  <!-- ... existing head content ... -->

  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'GA_MEASUREMENT_ID');
  </script>
</head>
```

## Getting Help

- **Documentation**: Check [docs/](.) and [CLAUDE.md](../CLAUDE.md)
- **Issues**: Open issue on [GitHub Issues](https://github.com/USERNAME/personal-event-summary/issues)
- **Examples**: Review mock data in `data/` directories

## Next Steps

After setup:
1. ✅ Customize event data
2. ✅ Add your attendees
3. ✅ Customize CSS styling
4. ✅ Configure GitHub Pages
5. ✅ Deploy and share URLs
6. ✅ Monitor analytics (if configured)

---

**Last Updated**: 2025-11-06
