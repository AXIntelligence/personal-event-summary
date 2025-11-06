# Data Models

This document describes the data models used in the Personal Event Summary system.

## Overview

The system uses JSON files to store mock event and attendee data. TypeScript interfaces provide compile-time type safety and runtime validation through type guards.

## Data Storage Structure

```
data/
├── events/
│   └── event-2025.json        # Event information
└── attendees/
    ├── 1001.json              # Individual attendee data
    ├── 1002.json
    └── ...                     # 10+ attendee files
```

## Core Data Models

### Event

Represents an event with metadata and statistics.

**TypeScript Interface:** `Event` (see `src/types/index.ts`)

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique event identifier (e.g., "event-2025") |
| `name` | string | Yes | Event name (e.g., "TechConf 2025") |
| `description` | string | Yes | Brief event description |
| `location` | string | Yes | Event location (city, venue) |
| `startDate` | string | Yes | ISO 8601 date string |
| `endDate` | string | Yes | ISO 8601 date string |
| `totalAttendees` | number | Yes | Total number of event attendees |
| `totalSessions` | number | Yes | Total number of sessions offered |
| `websiteUrl` | string | Yes | Event website URL |
| `logoUrl` | string | No | Relative path to event logo image |

**Example:**

```json
{
  "id": "event-2025",
  "name": "TechConf 2025",
  "description": "Annual technology conference",
  "location": "San Francisco, CA",
  "startDate": "2025-03-15T09:00:00Z",
  "endDate": "2025-03-17T18:00:00Z",
  "totalAttendees": 5000,
  "totalSessions": 120,
  "websiteUrl": "https://techconf2025.example.com",
  "logoUrl": "/static/images/event-logo.png"
}
```

### Attendee

Represents an event attendee with personalized data showcasing their event experience.

**TypeScript Interface:** `Attendee` (see `src/types/index.ts`)

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique attendee identifier (e.g., "1001") |
| `firstName` | string | Yes | Attendee first name |
| `lastName` | string | Yes | Attendee last name |
| `email` | string | Yes | Attendee email address |
| `company` | string | Yes | Company name |
| `title` | string | Yes | Job title |
| `eventId` | string | Yes | Reference to Event.id |
| `sessions` | Session[] | Yes | Array of sessions attended |
| `connections` | Connection[] | Yes | Array of connections made |
| `stats` | AttendeeStats | Yes | Personalized statistics |
| `callsToAction` | CallToAction[] | Yes | Re-engagement CTAs |
| `registeredAt` | string | Yes | ISO 8601 registration date |

**File Naming:** Each attendee is stored in a separate file named `{id}.json` (e.g., `1001.json`)

### Session

Represents a session at an event.

**TypeScript Interface:** `Session` (see `src/types/index.ts`)

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique session identifier |
| `title` | string | Yes | Session title |
| `description` | string | Yes | Session description |
| `speakers` | string[] | Yes | Array of speaker names |
| `dateTime` | string | Yes | ISO 8601 date/time string |
| `durationMinutes` | number | Yes | Session duration in minutes |
| `track` | string | No | Session track or category |

**Example:**

```json
{
  "id": "session-101",
  "title": "Future of AI",
  "description": "Exploring AI trends in 2025",
  "speakers": ["Dr. Jane Smith", "Prof. John Doe"],
  "dateTime": "2025-03-15T10:00:00Z",
  "durationMinutes": 60,
  "track": "Artificial Intelligence"
}
```

### Connection

Represents a professional connection made at an event.

**TypeScript Interface:** `Connection` (see `src/types/index.ts`)

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Connection's full name |
| `title` | string | Yes | Job title |
| `company` | string | Yes | Company name |
| `linkedIn` | string | No | LinkedIn profile URL |

**Example:**

```json
{
  "name": "Sarah Johnson",
  "title": "VP of Engineering",
  "company": "TechCorp Inc",
  "linkedIn": "https://linkedin.com/in/sarahjohnson"
}
```

### AttendeeStats

Represents personalized statistics and highlights for an attendee.

**TypeScript Interface:** `AttendeeStats` (see `src/types/index.ts`)

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sessionsAttended` | number | Yes | Total sessions attended |
| `connectionsMade` | number | Yes | Total connections made |
| `hoursAttended` | number | Yes | Total hours at event |
| `tracksExplored` | number | Yes | Number of different tracks |
| `topAchievement` | string | No | Key achievement or highlight |

**Example:**

```json
{
  "sessionsAttended": 12,
  "connectionsMade": 23,
  "hoursAttended": 18,
  "tracksExplored": 5,
  "topAchievement": "Most Active Networker"
}
```

### CallToAction

Represents a call-to-action for re-engagement.

**TypeScript Interface:** `CallToAction` (see `src/types/index.ts`)

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | CTA button/link text |
| `url` | string | Yes | Destination URL |
| `type` | 'primary' \| 'secondary' \| 'tertiary' | Yes | CTA visual priority |
| `trackingId` | string | No | Analytics tracking parameter |

**Example:**

```json
{
  "text": "Register for TechConf 2026",
  "url": "https://techconf2026.example.com/register?ref=summary",
  "type": "primary",
  "trackingId": "cta-register-2026"
}
```

## Data Relationships

```
Event (1) ←──── (N) Attendee
                  ├─→ (N) Session
                  ├─→ (N) Connection
                  ├─→ (1) AttendeeStats
                  └─→ (N) CallToAction
```

- One Event can have many Attendees
- Each Attendee references one Event via `eventId`
- Each Attendee can have multiple Sessions, Connections, and CTAs
- Each Attendee has one AttendeeStats object

## Type Safety

The system uses TypeScript interfaces for compile-time type checking and type guards for runtime validation:

- `isEvent(obj)` - Validates Event objects
- `isAttendee(obj)` - Validates Attendee objects
- `isSession(obj)` - Validates Session objects
- `isCallToAction(obj)` - Validates CallToAction objects

These type guards are used by the data loader to ensure data integrity.

## Validation Rules

### Email Format
Attendee emails should follow standard email format: `user@domain.com`

### Date Format
All dates use ISO 8601 format: `YYYY-MM-DDTHH:mm:ssZ`

### ID Format
- Event IDs: Alphanumeric with hyphens (e.g., `event-2025`)
- Attendee IDs: Numeric strings (e.g., `"1001"`)
- Session IDs: Alphanumeric with hyphens (e.g., `session-101`)

### URL Format
All URLs should be absolute URLs starting with `http://` or `https://`

## Mock Data Guidelines

When creating mock data:

1. **Diversity**: Create varied attendee profiles (different companies, titles, engagement levels)
2. **Realism**: Use realistic names, companies, and session topics
3. **Completeness**: Include all required fields
4. **Uniqueness**: Ensure each attendee has unique data to showcase personalization
5. **Relationships**: Ensure `eventId` in attendee data matches an actual event ID

## Future Considerations

- JSON Schema validation
- Data versioning
- Migration scripts for schema changes
- Database integration (replacing JSON files)
- Real-time data synchronization
