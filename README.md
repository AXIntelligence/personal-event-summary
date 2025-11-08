# Personal Event Summary

[![Test Suite](https://github.com/USERNAME/personal-event-summary/actions/workflows/test.yml/badge.svg)](https://github.com/USERNAME/personal-event-summary/actions/workflows/test.yml)
[![Scrape and Deploy](https://github.com/USERNAME/personal-event-summary/actions/workflows/scrape-and-deploy.yml/badge.svg)](https://github.com/USERNAME/personal-event-summary/actions/workflows/scrape-and-deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Note**: Replace `USERNAME` in the badge URLs with your GitHub username

A static site generator for creating personalized event summary pages for attendees. Built with Node.js, TypeScript, and Handlebars, designed to be deployed on GitHub Pages.

## ✨ Features

- 🎨 **Personalized Pages**: Generate unique, beautiful summary pages for each event attendee
- 📊 **Session Tracking**: Display sessions attended, speakers, duration, and tracks
- 🤝 **Connection Highlights**: Showcase networking connections made during the event
- 📈 **Engagement Stats**: Visual statistics showing attendance metrics
- 🎯 **Call-to-Actions**: Drive re-engagement with customizable CTAs
- 🏢 **B2B Event Support**: Optional fields for products explored, booth visits, and sponsor interactions
- 📱 **Responsive Design**: Mobile-first CSS with breakpoints for tablet and desktop
- ⚡ **Fast Generation**: Generates 24+ pages in under 1 second
- 🔒 **Type-Safe**: Full TypeScript implementation with runtime type guards
- ✅ **W3C Valid HTML5**: All pages pass HTML validation
- ♿ **Accessible**: Semantic HTML with proper ARIA attributes
- 🔄 **Multi-Event**: Support for multiple concurrent events with different configurations

## 🚀 Live Demo

### Event Tech Live 2025 (London)
- [Attendee 2001 - Aisha Patel (Tech Scout)](https://USERNAME.github.io/personal-event-summary/attendees/2001/) - 10 sessions, 22 connections
- [Attendee 2009 - Olivia Williams (Hybrid Producer)](https://USERNAME.github.io/personal-event-summary/attendees/2009/) - 10 sessions, 19 connections
- [Attendee 2012 - Marcus Anderson (Networking Maven)](https://USERNAME.github.io/personal-event-summary/attendees/2012/) - 5 sessions, 28 connections

### AWS re:Invent 2025 (Las Vegas)
- [Attendee 3001 - Priya Sharma (Cloud Architect)](https://USERNAME.github.io/personal-event-summary/attendees/3001/) - 11 sessions, 15 connections
- [Attendee 3006 - Emma Thompson (Solutions Architect)](https://USERNAME.github.io/personal-event-summary/attendees/3006/) - 9 sessions, 14 connections
- [Attendee 3012 - Olivia Martinez (Startup Founder)](https://USERNAME.github.io/personal-event-summary/attendees/3012/) - 6 sessions, 25 connections

*Examples include real company names, products explored, booth visits, and sponsor interactions*

## 📋 Requirements

- **Node.js**: 18.x or 20.x
- **npm**: 9.x or higher
- **TypeScript**: 5.x

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/USERNAME/personal-event-summary.git
cd personal-event-summary

# Install dependencies
npm install

# Build TypeScript
npm run build

# Generate static site
npm run generate
```

## 📁 Project Structure

```
personal-event-summary/
├── data/                      # Event and attendee data
│   ├── events/
│   │   ├── event-tech-live-2025.json  # Event Tech Live config
│   │   └── aws-reinvent-2025.json     # AWS re:Invent config
│   ├── sessions/
│   │   ├── event-tech-live-2025-sessions.json  # 30 B2B sessions
│   │   └── aws-reinvent-2025-sessions.json     # 30 AWS sessions
│   └── attendees/
│       ├── 2001-2012.json    # Event Tech Live attendees (12)
│       └── 3001-3012.json    # AWS re:Invent attendees (12)
├── src/                       # TypeScript source code
│   ├── types/
│   │   └── index.ts          # Type definitions + B2B interfaces
│   ├── dataLoader.ts         # Data loading with validation
│   └── generate.ts           # Page generation engine
├── templates/                 # Handlebars templates
│   ├── layouts/
│   │   └── base.hbs          # Base HTML layout
│   ├── pages/
│   │   └── attendee.hbs      # Attendee page template
│   └── partials/
│       ├── cta.hbs           # CTA component
│       ├── products.hbs      # Products explored (B2B)
│       └── booths.hbs        # Booths visited (B2B)
├── static/                    # Static assets
│   ├── css/
│   │   └── styles.css        # Responsive styles (14KB)
│   └── images/
├── tests/                     # Test suite (139 tests)
│   ├── unit/                 # Unit tests (70)
│   ├── integration/          # End-to-end tests (55)
│   └── validation/           # HTML validation tests (14)
├── dist/                      # Generated static site (24 pages)
├── analysis/                  # Validation reports
├── docs/                      # Documentation
│   └── github-pages-setup.md # Deployment guide
└── .github/workflows/         # CI/CD pipelines
    ├── test.yml              # Automated testing
    └── deploy.yml            # GitHub Pages deployment
```

## 🎯 Usage

### Generate Pages Locally

```bash
# Generate all attendee pages
npm run generate

# Output will be in dist/ directory
```

### Run Tests

```bash
# Run all tests
npm test

# Run with coverage report
npm run test:coverage

# Run only unit tests
npm test tests/unit/

# Run integration tests
npm test tests/integration/

# Run HTML validation
npm test tests/validation/
```

### Development

```bash
# Build TypeScript in watch mode
npx tsc --watch

# Run type checking
npm run type-check
```

## 📊 Test Coverage

**Overall Coverage**: 89.93% (exceeds 85% target)

| File | Statements | Branches | Functions | Lines |
|------|------------|----------|-----------|-------|
| dataLoader.ts | 73.94% | 64.70% | 60% | 73.94% |
| generate.ts | 88.72% | 59.09% | 100% | 88.72% |
| types/index.ts | 100% | 93.18% | 100% | 100% |

**Test Suite**: 139 tests passing
- 18 unit tests (types - includes B2B validation)
- 21 unit tests (cssGenerator - includes style config)
- 21 unit tests (dataLoader)
- 31 unit tests (generate)
- 13 integration tests (styleIntegration)
- 21 integration tests (endToEnd)
- 14 validation tests (HTML/accessibility)

## 🤖 Automated Style Scraping Pipeline

This project uses GitHub Actions to automatically scrape event website styles and apply them to generated pages.

### Workflow: Scrape and Deploy

**Triggers:**
- 🖱️ **Manual Dispatch**: Via GitHub Actions UI (on-demand scraping when event websites change)
- 📝 **Push to main**: Automatic deployment using cached style configs (no scraping, fast)

**Pipeline Flow:**
```
Manual Trigger → Scrape Event Websites → Validate JSON → Commit Configs → Generate Pages → Deploy
Push to main   → (Skip Scraping)       → Use Cached Configs → Generate Pages → Deploy
```

### Manual Scraping

Trigger scraping when:
- Event website redesign (colors/branding changed)
- New event added to system
- Before major releases (ensure styles are current)
- After discovering style mismatches

**Using GitHub CLI:**
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

**Using GitHub UI:**
1. Go to Actions → "Scrape Styles and Deploy"
2. Click "Run workflow"
3. Select events to scrape or choose "all"
4. Click "Run workflow"

### Cost Management

- **API Usage**: ~$0.10 per event per scrape (OpenAI API via CrewAI)
- **Manual-Only Triggers**: Costs only incurred when you manually trigger scraping
- **Typical Usage**: ~2 scrapes/month = ~$0.80/month for 4 events
- **Cached Configs**: Used if scraping fails (graceful fallback)
- **No Unexpected Charges**: No automated/scheduled scraping runs

### Pipeline Features

**Performance:**
- First run: ~5-7 min (install Playwright + scrape)
- Cached run: ~3-5 min (50% faster with browser caching)
- Push-only: <5 min (no scraping overhead)

**Monitoring:**
- Workflow status badge in README
- Scraping summary with event names, colors, timestamps
- Staleness warnings (configs >30 days old)
- Cost tracking (token usage logged)

**Validation:**
- JSON schema validation (all required fields present)
- Color format validation (#RRGGBB hex codes)
- End-to-end pipeline test (runs on push to main/develop)
- CSS injection verification (colors appear in generated HTML)

### Configuration

**Add New Events:**

1. Update `python/config/events.json`:
```json
{
  "id": "my-event-2025",
  "name": "My Conference 2025",
  "website": "https://myconference.com",
  "scraping": {
    "enabled": true,
    "timeout": 90,
    "selectors": {
      "header": "header",
      "primary_cta": ".btn-primary"
    }
  }
}
```

2. Run manual scraping workflow
3. Scraped config will be saved to `python/style-configs/my-event-2025.json`
4. Generate pages with event-specific styling

## 🎨 Customization

### Adding Attendees

Create a JSON file in `data/attendees/` following this structure:

```json
{
  "id": "2001",
  "firstName": "Aisha",
  "lastName": "Patel",
  "email": "aisha.patel@example.com",
  "eventId": "event-tech-live-2025",
  "sessions": [
    {
      "id": "session-01",
      "title": "AI-Powered Networking: From Random Encounters to Intentional Connections",
      "description": "Exploring how AI is revolutionizing event networking...",
      "speakers": ["Sarah Johnson", "Marcus Williams"],
      "durationMinutes": 60,
      "track": "AI & Innovation"
    }
  ],
  "connections": [
    {
      "name": "Marcus Rodriguez",
      "title": "CTO",
      "company": "ExpoPlatform",
      "linkedIn": "https://linkedin.com/in/marcusrodriguez"
    }
  ],
  "stats": {
    "sessionsAttended": 10,
    "connectionsMade": 22,
    "hoursAttended": 8.5,
    "tracksExplored": 5
  },
  "callsToAction": [
    {
      "text": "Save the Date: Event Tech Live 2026",
      "url": "https://eventtechlive.com/2026",
      "type": "primary",
      "trackingId": "cta-etl-2026"
    }
  ],

  // Optional B2B fields (for trade shows, conferences with exhibitors)
  "productsExplored": [
    {
      "name": "Erleah AI Networking",
      "company": "Braindate by Erleah",
      "category": "AI & Innovation"
    }
  ],
  "boothsVisited": [
    {
      "company": "ExpoPlatform",
      "timeSpentMinutes": 25,
      "productsViewed": ["AI Matchmaking", "Smart Badge System"]
    }
  ],
  "sponsorInteractions": [
    {
      "sponsor": "ExpoPlatform",
      "type": "demo_request",
      "timestamp": "2025-11-12T14:30:00Z"
    }
  ]
}
```

**Note**: `productsExplored`, `boothsVisited`, and `sponsorInteractions` are optional fields for B2B events with exhibitors.

### Modifying Templates

Edit Handlebars templates in `templates/`:
- `layouts/base.hbs` - HTML structure
- `pages/attendee.hbs` - Page content
- `partials/cta.hbs` - CTA component

### Styling

Modify `static/css/styles.css` to customize:
- Color scheme (CSS variables)
- Typography
- Layout and spacing
- Responsive breakpoints

## 🚀 Deployment

### GitHub Pages

1. Push your repository to GitHub
2. Configure GitHub Pages (see [docs/github-pages-setup.md](docs/github-pages-setup.md))
3. Push to `main` branch - site deploys automatically

**Deployment URL**: `https://USERNAME.github.io/REPOSITORY/`

### Manual Deployment

Generate the site and deploy the `dist/` directory to any static hosting:

```bash
npm run generate
# Deploy dist/ directory to your hosting provider
```

Supported platforms:
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static web server

## 🔧 Configuration

### Event Data

Edit event config files in `data/events/` to configure:
- Event name and dates
- Venue information
- Total attendee count
- Total sessions
- Branding

Examples:
- `data/events/event-tech-live-2025.json` - Event Tech Live configuration
- `data/events/aws-reinvent-2025.json` - AWS re:Invent configuration

### Template Helpers

Available Handlebars helpers:
- `{{formatDate date}}` - Format ISO dates
- `{{substring text start end}}` - Extract substring
- `{{currentYear}}` - Get current year

## 📖 Documentation

- [GitHub Pages Setup Guide](docs/github-pages-setup.md)
- [Data Models Reference](requirements/data-models.md)
- [Development Workflow](CLAUDE.md)
- [Plan 001: Initial Implementation](plans/001-github-pages-attendee-summary.md) ✅ Completed
- [Plan 002: Event Tech Live Sample Data](plans/002-event-tech-live-sample-data.md) ✅ Completed
- [Plan 007: AWS re:Invent Data & TechConf Removal](plans/007-end-to-end-scrape-deploy-pipeline.md) ✅ Completed
- [Validation Report: Plan 002](analysis/plan-002-validation-report.md)

## 🧪 Quality Standards

This project follows strict quality standards:

- ✅ **Test-Driven Development**: All code written test-first (RED-GREEN-REFACTOR)
- ✅ **89.93% Test Coverage**: Exceeds 85% target (139 tests passing)
- ✅ **W3C Valid HTML5**: Zero validation errors across 24 pages
- ✅ **Type Safety**: Full TypeScript with strict mode (100% types coverage)
- ✅ **Accessibility**: WCAG 2.1 AA compliant with semantic HTML
- ✅ **Performance**: < 1s generation for 24+ pages
- ✅ **Responsive Design**: Mobile-first with 3 breakpoints
- ✅ **Multi-Event Support**: Simultaneous Event Tech Live & AWS re:Invent
- ✅ **Backward Compatibility**: Optional B2B fields don't break existing data

## 🛣️ Roadmap

Potential future enhancements:
- [ ] Index page listing all attendees
- [ ] Search functionality
- [ ] Analytics integration (Google Analytics, Plausible)
- [ ] PDF export of summary pages
- [ ] Social sharing meta tags optimization
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] QR code generation for each attendee

## 🐛 Troubleshooting

### Build Failures

```bash
# Clean and reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Rebuild TypeScript
npm run build
```

### Test Failures

```bash
# Clean test artifacts
rm -rf dist-test/ dist-integration-test/ dist-validation-test/

# Run tests again
npm test
```

### GitHub Pages 404 Errors

- Ensure `.nojekyll` exists in dist/
- Verify GitHub Pages source is set to "GitHub Actions"
- Check workflow permissions in repository settings

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Create a plan using `/plan [feature description]`
2. Review and discuss the plan
3. Implement using TDD methodology
4. Ensure all tests pass and coverage remains above 80%
5. Update documentation
6. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

Built with:
- [Node.js](https://nodejs.org/) - JavaScript runtime
- [TypeScript](https://www.typescriptlang.org/) - Type-safe JavaScript
- [Handlebars](https://handlebarsjs.com/) - Template engine
- [Vitest](https://vitest.dev/) - Fast unit test framework
- [html-validate](https://html-validate.org/) - HTML validation

## 📧 Support

For issues and questions:
- Open an issue on [GitHub Issues](https://github.com/USERNAME/personal-event-summary/issues)
- Review [documentation](docs/)
- Check [existing issues](https://github.com/USERNAME/personal-event-summary/issues?q=is%3Aissue)

---

**Built with TDD** • **89.93% Test Coverage** • **139 Tests Passing** • **W3C Valid HTML5** • **24 Pages Generated** • **Fully Responsive**

Last Updated: 2025-11-07 • Version: 1.2.0 (Plan 007 Completed)
