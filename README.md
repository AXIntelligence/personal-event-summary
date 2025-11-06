# Personal Event Summary

[![Test Suite](https://github.com/USERNAME/personal-event-summary/actions/workflows/test.yml/badge.svg)](https://github.com/USERNAME/personal-event-summary/actions/workflows/test.yml)
[![Deploy to GitHub Pages](https://github.com/USERNAME/personal-event-summary/actions/workflows/deploy.yml/badge.svg)](https://github.com/USERNAME/personal-event-summary/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Note**: Replace `USERNAME` in the badge URLs with your GitHub username

A static site generator for creating personalized event summary pages for attendees. Built with Node.js, TypeScript, and Handlebars, designed to be deployed on GitHub Pages.

## ✨ Features

- 🎨 **Personalized Pages**: Generate unique, beautiful summary pages for each event attendee
- 📊 **Session Tracking**: Display sessions attended, speakers, duration, and tracks
- 🤝 **Connection Highlights**: Showcase networking connections made during the event
- 📈 **Engagement Stats**: Visual statistics showing attendance metrics
- 🎯 **Call-to-Actions**: Drive re-engagement with customizable CTAs
- 📱 **Responsive Design**: Mobile-first CSS with breakpoints for tablet and desktop
- ⚡ **Fast Generation**: Generates 12+ pages in under 500ms
- 🔒 **Type-Safe**: Full TypeScript implementation with runtime type guards
- ✅ **W3C Valid HTML5**: All pages pass HTML validation
- ♿ **Accessible**: Semantic HTML with proper ARIA attributes

## 🚀 Live Demo

View example attendee pages:
- [Attendee 1001 - Sarah Chen](https://USERNAME.github.io/personal-event-summary/attendees/1001/)
- [Attendee 1002 - Michael O'Brien](https://USERNAME.github.io/personal-event-summary/attendees/1002/)

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
│   │   └── event-2025.json   # Event configuration
│   └── attendees/
│       ├── 1001.json         # Individual attendee data
│       └── ...
├── src/                       # TypeScript source code
│   ├── types/
│   │   └── index.ts          # Type definitions
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
│   │   └── styles.css        # Responsive styles (14KB)
│   └── images/
├── tests/                     # Test suite (87 tests)
│   ├── unit/                 # Unit tests
│   ├── integration/          # End-to-end tests
│   └── validation/           # HTML validation tests
├── dist/                      # Generated static site
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

**Overall Coverage**: 85.42% (exceeds 80% target)

| File | Statements | Branches | Functions | Lines |
|------|------------|----------|-----------|-------|
| dataLoader.ts | 73.94% | 64.70% | 60% | 73.94% |
| generate.ts | 88.37% | 59.09% | 100% | 88.37% |
| types/index.ts | 89.84% | 50% | 50% | 89.84% |

**Test Suite**: 87 tests passing
- 21 unit tests (dataLoader)
- 31 unit tests (generate)
- 21 integration tests (end-to-end)
- 14 validation tests (HTML/accessibility)

## 🎨 Customization

### Adding Attendees

Create a JSON file in `data/attendees/` following this structure:

```json
{
  "id": "1001",
  "firstName": "Sarah",
  "lastName": "Chen",
  "email": "sarah.chen@example.com",
  "eventId": "event-2025",
  "sessions": [
    {
      "id": "session-01",
      "title": "Future of AI and Machine Learning",
      "description": "Exploring cutting-edge developments...",
      "speakers": ["Dr. Jane Smith", "Prof. Michael Zhang"],
      "durationMinutes": 60,
      "track": "Artificial Intelligence"
    }
  ],
  "connections": [
    {
      "name": "Marcus Rodriguez",
      "title": "CTO",
      "company": "StartupXYZ",
      "linkedinUrl": "https://linkedin.com/in/marcusrodriguez"
    }
  ],
  "stats": {
    "sessionsAttended": 3,
    "connectionsMade": 3,
    "hoursInvested": 3.75,
    "tracksExplored": 3
  },
  "callsToAction": [
    {
      "text": "Register for TechConf 2026",
      "url": "https://techconf2026.example.com",
      "type": "primary"
    }
  ]
}
```

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

Edit `data/events/event-2025.json` to configure:
- Event name and dates
- Venue information
- Total attendee count
- Total sessions
- Branding

### Template Helpers

Available Handlebars helpers:
- `{{formatDate date}}` - Format ISO dates
- `{{substring text start end}}` - Extract substring
- `{{currentYear}}` - Get current year

## 📖 Documentation

- [GitHub Pages Setup Guide](docs/github-pages-setup.md)
- [Data Models Reference](requirements/data-models.md)
- [Development Workflow](CLAUDE.md)
- [Implementation Plan](plans/001-github-pages-attendee-summary.md)

## 🧪 Quality Standards

This project follows strict quality standards:

- ✅ **Test-Driven Development**: All code written test-first
- ✅ **85%+ Test Coverage**: Exceeds 80% target
- ✅ **W3C Valid HTML5**: Zero validation errors
- ✅ **Type Safety**: Full TypeScript with strict mode
- ✅ **Accessibility**: WCAG 2.1 AA compliant
- ✅ **Performance**: < 2s generation for 12+ pages
- ✅ **Responsive Design**: Mobile-first approach

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

**Built with TDD** • **85% Test Coverage** • **W3C Valid HTML5** • **Fully Responsive**

Last Updated: 2025-11-06 • Version: 1.0.0
