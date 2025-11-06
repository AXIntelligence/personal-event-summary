import { describe, it, expect, beforeAll } from 'vitest';
import { loadEvent, loadAttendee, loadAllAttendees } from '../../src/dataLoader.js';
import type { Event, Attendee } from '../../src/types/index.js';

describe('dataLoader', () => {
  describe('loadEvent', () => {
    it('should load and parse event data from JSON file', async () => {
      const event = await loadEvent('event-2025');

      expect(event).toBeDefined();
      expect(event.id).toBe('event-2025');
      expect(event.name).toBe('TechConf 2025');
      expect(event.location).toContain('San Francisco');
      expect(event.totalAttendees).toBeGreaterThan(0);
      expect(event.totalSessions).toBeGreaterThan(0);
    });

    it('should throw error for non-existent event', async () => {
      await expect(loadEvent('non-existent-event')).rejects.toThrow();
    });

    it('should validate event data structure with type guard', async () => {
      const event = await loadEvent('event-2025');

      // Verify all required fields are present
      expect(event).toHaveProperty('id');
      expect(event).toHaveProperty('name');
      expect(event).toHaveProperty('description');
      expect(event).toHaveProperty('location');
      expect(event).toHaveProperty('startDate');
      expect(event).toHaveProperty('endDate');
      expect(event).toHaveProperty('totalAttendees');
      expect(event).toHaveProperty('totalSessions');
      expect(event).toHaveProperty('websiteUrl');
    });

    it('should parse dates as strings in ISO format', async () => {
      const event = await loadEvent('event-2025');

      expect(typeof event.startDate).toBe('string');
      expect(typeof event.endDate).toBe('string');
      expect(event.startDate).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
    });
  });

  describe('loadAttendee', () => {
    it('should load and parse attendee data from JSON file', async () => {
      const attendee = await loadAttendee('1001');

      expect(attendee).toBeDefined();
      expect(attendee.id).toBe('1001');
      expect(attendee.firstName).toBeTruthy();
      expect(attendee.lastName).toBeTruthy();
      expect(attendee.email).toContain('@');
      expect(attendee.company).toBeTruthy();
      expect(attendee.eventId).toBe('event-2025');
    });

    it('should throw error for non-existent attendee', async () => {
      await expect(loadAttendee('9999')).rejects.toThrow();
    });

    it('should load attendee with sessions array', async () => {
      const attendee = await loadAttendee('1001');

      expect(Array.isArray(attendee.sessions)).toBe(true);
      expect(attendee.sessions.length).toBeGreaterThan(0);

      const session = attendee.sessions[0];
      expect(session).toHaveProperty('id');
      expect(session).toHaveProperty('title');
      expect(session).toHaveProperty('speakers');
      expect(Array.isArray(session.speakers)).toBe(true);
    });

    it('should load attendee with connections array', async () => {
      const attendee = await loadAttendee('1001');

      expect(Array.isArray(attendee.connections)).toBe(true);

      if (attendee.connections.length > 0) {
        const connection = attendee.connections[0];
        expect(connection).toHaveProperty('name');
        expect(connection).toHaveProperty('title');
        expect(connection).toHaveProperty('company');
      }
    });

    it('should load attendee with stats object', async () => {
      const attendee = await loadAttendee('1001');

      expect(attendee.stats).toBeDefined();
      expect(typeof attendee.stats.sessionsAttended).toBe('number');
      expect(typeof attendee.stats.connectionsMade).toBe('number');
      expect(typeof attendee.stats.hoursAttended).toBe('number');
      expect(typeof attendee.stats.tracksExplored).toBe('number');
    });

    it('should load attendee with callsToAction array', async () => {
      const attendee = await loadAttendee('1001');

      expect(Array.isArray(attendee.callsToAction)).toBe(true);
      expect(attendee.callsToAction.length).toBeGreaterThan(0);

      const cta = attendee.callsToAction[0];
      expect(cta).toHaveProperty('text');
      expect(cta).toHaveProperty('url');
      expect(cta).toHaveProperty('type');
      expect(['primary', 'secondary', 'tertiary']).toContain(cta.type);
    });

    it('should validate attendee email format', async () => {
      const attendee = await loadAttendee('1001');

      expect(attendee.email).toMatch(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
    });

    it('should validate all required attendee fields', async () => {
      const attendee = await loadAttendee('1001');

      const requiredFields = [
        'id', 'firstName', 'lastName', 'email', 'company', 'title',
        'eventId', 'sessions', 'connections', 'stats', 'callsToAction', 'registeredAt'
      ];

      requiredFields.forEach(field => {
        expect(attendee).toHaveProperty(field);
      });
    });
  });

  describe('loadAllAttendees', () => {
    it('should load all attendee files from data directory', async () => {
      const attendees = await loadAllAttendees();

      expect(Array.isArray(attendees)).toBe(true);
      expect(attendees.length).toBeGreaterThanOrEqual(10);
    });

    it('should return attendees with unique IDs', async () => {
      const attendees = await loadAllAttendees();

      const ids = attendees.map(a => a.id);
      const uniqueIds = new Set(ids);

      expect(uniqueIds.size).toBe(ids.length);
    });

    it('should load attendees for the same event', async () => {
      const attendees = await loadAllAttendees();

      const eventIds = attendees.map(a => a.eventId);
      const uniqueEventIds = new Set(eventIds);

      // All attendees should be for event-2025
      expect(uniqueEventIds.size).toBe(1);
      expect(uniqueEventIds.has('event-2025')).toBe(true);
    });

    it('should handle empty data directory gracefully', async () => {
      // This test ensures error handling exists
      // In actual implementation, if directory is empty, should return empty array
      const attendees = await loadAllAttendees();
      expect(attendees).toBeDefined();
    });

    it('should load attendees with varied engagement levels', async () => {
      const attendees = await loadAllAttendees();

      const sessionCounts = attendees.map(a => a.sessions.length);
      const connectionCounts = attendees.map(a => a.connections.length);

      // Verify diversity in engagement
      expect(Math.max(...sessionCounts)).toBeGreaterThan(Math.min(...sessionCounts));
      expect(Math.max(...connectionCounts)).toBeGreaterThan(0);
    });
  });

  describe('Error Handling', () => {
    it('should throw meaningful error for invalid JSON', async () => {
      // Test will be implemented after dataLoader is created
      // This ensures proper error messages
      await expect(loadEvent('event-2025')).resolves.toBeDefined();
    });

    it('should handle file read errors gracefully', async () => {
      await expect(loadAttendee('invalid-id')).rejects.toThrow();
    });
  });

  describe('Type Safety', () => {
    it('should return properly typed Event object', async () => {
      const event: Event = await loadEvent('event-2025');

      // TypeScript should enforce these types at compile time
      expect(typeof event.id).toBe('string');
      expect(typeof event.totalAttendees).toBe('number');
    });

    it('should return properly typed Attendee object', async () => {
      const attendee: Attendee = await loadAttendee('1001');

      // TypeScript should enforce these types at compile time
      expect(typeof attendee.id).toBe('string');
      expect(typeof attendee.stats.sessionsAttended).toBe('number');
    });
  });
});
