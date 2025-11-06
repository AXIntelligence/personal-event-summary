# Examples

This document provides examples of data structures, generated output, and usage patterns.

## Example Data

The project includes comprehensive mock data for testing and demonstration purposes.

### Event Data Example

**Location**: `data/events/event-2025.json`

```json
{
  "id": "event-2025",
  "name": "TechConf 2025",
  "startDate": "2025-03-15T09:00:00Z",
  "endDate": "2025-03-17T18:00:00Z",
  "venue": {
    "name": "Moscone Center",
    "address": "747 Howard St",
    "city": "San Francisco",
    "state": "CA",
    "zipCode": "94103",
    "country": "USA"
  },
  "stats": {
    "totalAttendees": 5000,
    "totalSessions": 120
  }
}
```

### Attendee Data Examples

The project includes 12 mock attendees with varying engagement levels:

**High Engagement** (`data/attendees/1002.json`):
- 5 sessions attended
- 5 connections made
- 5.75 hours invested
- 4 tracks explored

**Medium Engagement** (`data/attendees/1001.json`):
- 3 sessions attended
- 3 connections made
- 3.75 hours invested
- 3 tracks explored

**Example Attendee Structure** (data/attendees/1001.json):

```json
{
  "id": "1001",
  "firstName": "Sarah",
  "lastName": "Chen",
  "email": "sarah.chen@example.com",
  "company": "TechCorp Inc",
  "title": "Senior Software Engineer",
  "eventId": "event-2025",
  "achievement": "Early Bird Attendee",
  "registeredAt": "2025-01-10T14:30:00Z",
  "sessions": [
    {
      "id": "session-01",
      "title": "Future of AI and Machine Learning",
      "description": "Exploring cutting-edge developments in artificial intelligence...",
      "speakers": ["Dr. Jane Smith", "Prof. Michael Zhang"],
      "durationMinutes": 60,
      "track": "Artificial Intelligence",
      "scheduledAt": "2025-03-15T10:00:00Z"
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
      "url": "https://techconf2026.example.com/register?ref=summary-1001",
      "type": "primary",
      "trackingId": "cta-register-2026"
    }
  ]
}
```

## Generated Output Examples

After running `npm run generate`, pages are created in the `dist/` directory.

### Directory Structure

```
dist/
├── attendees/
│   ├── 1001/
│   │   └── index.html    (Sarah Chen's page - 13KB)
│   ├── 1002/
│   │   └── index.html    (Michael O'Brien's page - 15KB)
│   ├── 1003/
│   │   └── index.html    (Emily Rodriguez's page - 14KB)
│   └── ...               (9 more attendee pages)
├── static/
│   ├── css/
│   │   └── styles.css    (14KB responsive CSS)
│   └── images/
│       ├── event-logo.png
│       └── favicon.png
├── .nojekyll
└── 404.html
```

### Example Generated Page

**URL**: `/attendees/1001/index.html` (dist/attendees/1001/index.html)

**Key Sections**:

1. **Hero Section**:
   - Welcome message with attendee's first name
   - Personalized subtitle
   - Achievement badge

2. **Stats Overview**:
   - Sessions Attended: 3
   - Connections Made: 3
   - Hours Invested: 3.75
   - Tracks Explored: 3

3. **Learning Journey**:
   - Future of AI and Machine Learning (60 min)
   - Building Scalable Microservices (90 min)
   - Cloud Native Security (75 min)

4. **Network Growth**:
   - Marcus Rodriguez (CTO, StartupXYZ)
   - Emily Watson (Lead Developer, DevHouse Studios)
   - Alex Thompson (Engineering Manager, CloudTech Solutions)

5. **Call-to-Actions**:
   - Register for TechConf 2026
   - Join Our Community
   - Download Session Materials

### Example Clean URLs

GitHub Pages serves these URLs:

- ✅ `https://username.github.io/repo/attendees/1001/`
- ✅ `https://username.github.io/repo/attendees/1001`
- ✅ `https://username.github.io/repo/attendees/1001/index.html`

All three URLs serve the same page.

## Usage Examples

### Basic Generation

```bash
# Generate all attendee pages
npm run generate

# Output:
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

### Adding a New Attendee

```bash
# 1. Create new attendee JSON file
cp data/attendees/1001.json data/attendees/2001.json

# 2. Edit the file with new attendee data
vim data/attendees/2001.json

# 3. Rebuild and regenerate
npm run build
npm run generate

# 4. New page created at: dist/attendees/2001/index.html
```

### Testing a Specific Attendee

```typescript
// tests/unit/dataLoader.test.ts
it('should load attendee 1001', async () => {
  const attendee = await loadAttendee('1001');

  expect(attendee.id).toBe('1001');
  expect(attendee.firstName).toBe('Sarah');
  expect(attendee.lastName).toBe('Chen');
  expect(attendee.sessions.length).toBe(3);
});
```

### Customizing Templates

```handlebars
<!-- templates/pages/attendee.hbs -->

<!-- Original -->
<h1 class="hero-title">
    Welcome back, <span class="highlight">{{attendee.firstName}}</span>! 🎉
</h1>

<!-- Customized -->
<h1 class="hero-title">
    Hey {{attendee.firstName}}, check out your {{event.name}} recap! 🚀
</h1>
```

## API Usage Examples

### Loading Data Programmatically

```typescript
import { loadEvent, loadAttendee, loadAllAttendees } from './src/dataLoader.js';

// Load specific event
const event = await loadEvent('event-2025');
console.log(event.name); // "TechConf 2025"

// Load specific attendee
const attendee = await loadAttendee('1001');
console.log(`${attendee.firstName} ${attendee.lastName}`); // "Sarah Chen"

// Load all attendees
const attendees = await loadAllAttendees();
console.log(`Total attendees: ${attendees.length}`); // 12
```

### Generating Pages Programmatically

```typescript
import { generateAttendeePage, generateAllAttendeePages } from './src/generate.js';

// Generate single attendee page
const outputPath = await generateAttendeePage('1001', './dist');
console.log(`Generated: ${outputPath}`);
// Generated: /path/to/dist/attendees/1001/index.html

// Generate all pages
const paths = await generateAllAttendeePages('./dist');
console.log(`Generated ${paths.length} pages`);
// Generated 12 pages
```

## Testing Examples

### Unit Test Example

```typescript
// tests/unit/dataLoader.test.ts
describe('loadAttendee', () => {
  it('should load valid attendee data', async () => {
    const attendee = await loadAttendee('1001');

    expect(attendee).toBeDefined();
    expect(attendee.id).toBe('1001');
    expect(attendee.eventId).toBe('event-2025');
    expect(Array.isArray(attendee.sessions)).toBe(true);
  });

  it('should throw error for non-existent attendee', async () => {
    await expect(loadAttendee('99999')).rejects.toThrow();
  });
});
```

### Integration Test Example

```typescript
// tests/integration/endToEnd.test.ts
it('should generate complete static site', async () => {
  await generateAll(TEST_DIST_DIR);

  // Verify directories exist
  await expect(access(TEST_DIST_DIR)).resolves.not.toThrow();
  await expect(access(join(TEST_DIST_DIR, 'attendees'))).resolves.not.toThrow();
  await expect(access(join(TEST_DIST_DIR, 'static'))).resolves.not.toThrow();

  // Verify attendee pages exist
  const attendees = await loadAllAttendees();
  const generatedDirs = await readdir(join(TEST_DIST_DIR, 'attendees'));
  expect(generatedDirs.length).toBe(attendees.length);
});
```

### HTML Validation Example

```typescript
// tests/validation/htmlValidation.test.ts
it('should validate all generated pages', async () => {
  const htmlvalidate = new HtmlValidate({
    extends: ['html-validate:recommended']
  });

  const attendeeIds = await readdir(join(TEST_DIST_DIR, 'attendees'));

  for (const id of attendeeIds) {
    const htmlPath = join(TEST_DIST_DIR, 'attendees', id, 'index.html');
    const html = await readFile(htmlPath, 'utf-8');
    const report = await htmlvalidate.validateString(html);

    expect(report.valid).toBe(true);
  }
});
```

## Performance Examples

### Generation Performance

```bash
# Time the generation process
time npm run generate

# Typical output:
# real    0m0.524s
# user    0m0.412s
# sys     0m0.089s
```

**Performance Metrics**:
- 12 pages generated in ~500ms
- Average: ~42ms per page
- Well under 2-second target

### File Sizes

**Attendee Pages**:
- Minimum: 12KB (attendee with 2 sessions)
- Average: 13KB (attendee with 3-4 sessions)
- Maximum: 15KB (attendee with 5+ sessions)

**Assets**:
- CSS: 14KB (unminified, 685 lines)
- Total static assets: ~14KB

## Customization Examples

### Custom Color Scheme

```css
/* static/css/styles.css */
:root {
    /* Original */
    --color-primary: #667eea;
    --color-secondary: #764ba2;

    /* Custom Brand Colors */
    --color-primary: #ff6b6b;
    --color-secondary: #4ecdc4;
}
```

### Custom Handlebars Helper

```typescript
// src/generate.ts
hbs.registerHelper('uppercase', (str: string) => {
  return str.toUpperCase();
});

// Then in template:
// {{uppercase attendee.firstName}} → SARAH
```

### Custom CTA

```json
{
  "callsToAction": [
    {
      "text": "Download Your Certificate",
      "url": "https://example.com/certificates/1001.pdf",
      "type": "primary",
      "trackingId": "cta-certificate"
    }
  ]
}
```

## Real-World Use Cases

### 1. Post-Event Engagement

**Scenario**: Send personalized summary pages to attendees after a conference.

**Implementation**:
1. Export attendee data from event platform
2. Convert to JSON format
3. Generate pages: `npm run generate`
4. Deploy to GitHub Pages
5. Email unique URLs to each attendee

### 2. Multi-Track Conference

**Scenario**: Large conference with multiple tracks and hundreds of attendees.

**Implementation**:
- One event JSON file
- Hundreds of attendee JSON files
- Parallel generation handles scale
- Clean URLs make sharing easy

### 3. Virtual Event Summary

**Scenario**: Online event tracking session views and chat connections.

**Implementation**:
- Track virtual "sessions attended" (videos watched)
- Track "connections" (chat interactions, meeting requests)
- Generate personalized recaps
- Include CTAs for next virtual event

## Additional Resources

- **Full Attendee Dataset**: `data/attendees/` (12 examples)
- **Event Configuration**: `data/events/event-2025.json`
- **Generated Output**: Run `npm run generate` to see results
- **Test Examples**: Review `tests/` directory for more examples

---

**Last Updated**: 2025-11-06
