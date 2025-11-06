import { describe, it, expect } from 'vitest';
import { isAttendee, isEvent, isSession, isCallToAction } from '../../src/types/index.js';
import type { Attendee, Product, BoothVisit } from '../../src/types/index.js';

describe('Type Guards', () => {
  describe('isAttendee', () => {
    const baseAttendee = {
      id: '1001',
      firstName: 'John',
      lastName: 'Doe',
      email: 'john@example.com',
      company: 'TechCorp',
      title: 'Engineer',
      eventId: 'event-2025',
      sessions: [],
      connections: [],
      stats: {
        sessionsAttended: 5,
        connectionsMade: 10,
        hoursAttended: 8,
        tracksExplored: 3,
      },
      callsToAction: [],
      registeredAt: '2024-01-01T00:00:00Z',
    };

    it('should accept valid attendee without B2B fields (backward compatibility)', () => {
      expect(isAttendee(baseAttendee)).toBe(true);
    });

    it('should accept valid attendee with productsExplored', () => {
      const attendeeWithProducts = {
        ...baseAttendee,
        productsExplored: [
          {
            name: 'Eventpack Registration Platform',
            company: 'Eventpack',
            category: 'Registration & Check-In Technology',
          },
          {
            name: 'Braindate Experience',
            company: 'Braindate',
            category: 'Networking Platforms',
          },
        ],
      };

      expect(isAttendee(attendeeWithProducts)).toBe(true);
    });

    it('should accept valid attendee with boothsVisited', () => {
      const attendeeWithBooths = {
        ...baseAttendee,
        boothsVisited: [
          {
            company: 'Choose 2 Rent',
            timeSpentMinutes: 15,
            productsViewed: ['Event Kiosk Pro', 'Zebra ZD621 Badge Printer'],
          },
          {
            company: 'Eventbase',
            timeSpentMinutes: 10,
            productsViewed: ['Event App Platform'],
          },
        ],
      };

      expect(isAttendee(attendeeWithBooths)).toBe(true);
    });

    it('should accept valid attendee with sponsorInteractions', () => {
      const attendeeWithSponsors = {
        ...baseAttendee,
        sponsorInteractions: [
          {
            sponsor: 'Choose 2 Rent',
            type: 'booth_visit',
            timestamp: '2025-11-12T10:30:00Z',
          },
          {
            sponsor: 'Choose 2 Rent',
            type: 'demo_request',
            timestamp: '2025-11-12T10:45:00Z',
          },
        ],
      };

      expect(isAttendee(attendeeWithSponsors)).toBe(true);
    });

    it('should accept valid attendee with all B2B fields', () => {
      const fullB2BAttendee = {
        ...baseAttendee,
        productsExplored: [
          { name: 'Product 1', company: 'Company A', category: 'Category 1' },
        ],
        boothsVisited: [
          { company: 'Company B', timeSpentMinutes: 20, productsViewed: ['Product 2'] },
        ],
        sponsorInteractions: [
          { sponsor: 'Sponsor A', type: 'booth_visit', timestamp: '2025-11-12T10:00:00Z' },
        ],
      };

      expect(isAttendee(fullB2BAttendee)).toBe(true);
    });

    it('should reject attendee with invalid productsExplored type', () => {
      const invalid = {
        ...baseAttendee,
        productsExplored: 'not an array',
      };

      expect(isAttendee(invalid)).toBe(false);
    });

    it('should reject attendee with invalid boothsVisited type', () => {
      const invalid = {
        ...baseAttendee,
        boothsVisited: 'not an array',
      };

      expect(isAttendee(invalid)).toBe(false);
    });

    it('should reject attendee with invalid sponsorInteractions type', () => {
      const invalid = {
        ...baseAttendee,
        sponsorInteractions: { invalid: 'object' },
      };

      expect(isAttendee(invalid)).toBe(false);
    });

    it('should reject attendee missing required fields', () => {
      const incomplete = {
        id: '1001',
        firstName: 'John',
        // Missing other required fields
      };

      expect(isAttendee(incomplete)).toBe(false);
    });

    it('should reject null or undefined', () => {
      expect(isAttendee(null)).toBe(false);
      expect(isAttendee(undefined)).toBe(false);
    });

    it('should reject non-object types', () => {
      expect(isAttendee('string')).toBe(false);
      expect(isAttendee(123)).toBe(false);
      expect(isAttendee([])).toBe(false);
    });
  });

  describe('isEvent', () => {
    it('should accept valid event', () => {
      const event = {
        id: 'event-2025',
        name: 'TechConf 2025',
        description: 'A tech conference',
        location: 'San Francisco',
        startDate: '2025-03-15T09:00:00Z',
        endDate: '2025-03-17T18:00:00Z',
        totalAttendees: 5000,
        totalSessions: 120,
        websiteUrl: 'https://example.com',
      };

      expect(isEvent(event)).toBe(true);
    });

    it('should reject event missing required fields', () => {
      const incomplete = {
        id: 'event-2025',
        name: 'TechConf 2025',
      };

      expect(isEvent(incomplete)).toBe(false);
    });
  });

  describe('isSession', () => {
    it('should accept valid session', () => {
      const session = {
        id: 'session-101',
        title: 'AI in Events',
        description: 'Learn about AI',
        speakers: ['Dr. Jane Smith'],
        dateTime: '2025-03-15T10:00:00Z',
        durationMinutes: 60,
      };

      expect(isSession(session)).toBe(true);
    });

    it('should reject session with invalid speakers type', () => {
      const invalid = {
        id: 'session-101',
        title: 'AI in Events',
        description: 'Learn about AI',
        speakers: 'Not an array',
        dateTime: '2025-03-15T10:00:00Z',
        durationMinutes: 60,
      };

      expect(isSession(invalid)).toBe(false);
    });
  });

  describe('isCallToAction', () => {
    it('should accept valid primary CTA', () => {
      const cta = {
        text: 'Register Now',
        url: 'https://example.com/register',
        type: 'primary' as const,
      };

      expect(isCallToAction(cta)).toBe(true);
    });

    it('should accept valid secondary CTA', () => {
      const cta = {
        text: 'Learn More',
        url: 'https://example.com/learn',
        type: 'secondary' as const,
      };

      expect(isCallToAction(cta)).toBe(true);
    });

    it('should reject CTA with invalid type', () => {
      const invalid = {
        text: 'Click Here',
        url: 'https://example.com',
        type: 'invalid',
      };

      expect(isCallToAction(invalid)).toBe(false);
    });
  });
});
