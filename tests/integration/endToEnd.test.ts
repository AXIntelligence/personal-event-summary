import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { rm, access, readFile, readdir, stat } from 'fs/promises';
import { join } from 'path';
import { generateAll } from '../../src/generate.js';
import { loadAllAttendees } from '../../src/dataLoader.js';

const TEST_DIST_DIR = join(process.cwd(), 'dist-integration-test');

describe('End-to-End Integration Tests', () => {
  beforeAll(async () => {
    // Clean up test directory
    try {
      await rm(TEST_DIST_DIR, { recursive: true, force: true });
    } catch {
      // Ignore if doesn't exist
    }
  });

  afterAll(async () => {
    // Clean up after tests
    try {
      await rm(TEST_DIST_DIR, { recursive: true, force: true });
    } catch {
      // Ignore cleanup errors
    }
  });

  describe('Complete Generation Pipeline', () => {
    it('should generate complete static site with all pages and assets', async () => {
      // Run complete generation
      await generateAll(TEST_DIST_DIR);

      // Verify dist directory exists
      await expect(access(TEST_DIST_DIR)).resolves.not.toThrow();

      // Verify attendees directory exists
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      await expect(access(attendeesDir)).resolves.not.toThrow();

      // Verify static assets directory exists
      const staticDir = join(TEST_DIST_DIR, 'static');
      await expect(access(staticDir)).resolves.not.toThrow();
    });

    it('should generate pages for all attendees in data directory', async () => {
      const attendees = await loadAllAttendees();
      await generateAll(TEST_DIST_DIR);

      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const generatedDirs = await readdir(attendeesDir);

      // Should have same number of directories as attendees
      expect(generatedDirs.length).toBe(attendees.length);
      expect(generatedDirs.length).toBeGreaterThanOrEqual(10);
    });

    it('should create proper directory structure for clean URLs', async () => {
      await generateAll(TEST_DIST_DIR);

      // Check specific attendee structure
      const attendee1001Dir = join(TEST_DIST_DIR, 'attendees', '2001');
      const indexPath = join(attendee1001Dir, 'index.html');

      await expect(access(attendee1001Dir)).resolves.not.toThrow();
      await expect(access(indexPath)).resolves.not.toThrow();

      // Verify it's a file, not a directory
      const stats = await stat(indexPath);
      expect(stats.isFile()).toBe(true);
    });

    it('should copy all static assets correctly', async () => {
      await generateAll(TEST_DIST_DIR);

      // Check CSS
      const cssPath = join(TEST_DIST_DIR, 'static', 'css', 'styles.css');
      await expect(access(cssPath)).resolves.not.toThrow();

      // Check images directory exists
      const imagesDir = join(TEST_DIST_DIR, 'static', 'images');
      await expect(access(imagesDir)).resolves.not.toThrow();
    });
  });

  describe('Content Validation', () => {
    beforeAll(async () => {
      await generateAll(TEST_DIST_DIR);
    });

    it('should generate valid HTML for all attendees', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      for (const id of attendeeIds) {
        const htmlPath = join(attendeesDir, id, 'index.html');
        const content = await readFile(htmlPath, 'utf-8');

        // Basic HTML validation
        expect(content).toContain('<!DOCTYPE html>');
        expect(content).toContain('<html');
        expect(content).toContain('</html>');
        expect(content).toContain('<head>');
        expect(content).toContain('</head>');
        expect(content).toContain('<body>');
        expect(content).toContain('</body>');

        // Should have proper meta tags
        expect(content).toContain('<meta charset="UTF-8">');
        expect(content).toContain('viewport');
        expect(content).toContain('<title>');
      }
    });

    it('should include event information in all pages', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      for (const id of attendeeIds.slice(0, 3)) { // Check first 3
        const htmlPath = join(attendeesDir, id, 'index.html');
        const content = await readFile(htmlPath, 'utf-8');

        expect(content).toContain('Event Tech Live 2025');
        expect(content).toContain('London');
      }
    });

    it('should include personalized content for each attendee', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');

      // Check attendee 1001 (Aisha Patel)
      const sarah = await readFile(join(attendeesDir, '2001', 'index.html'), 'utf-8');
      expect(sarah).toContain('Aisha');
      expect(sarah).toContain('Aisha Patel - Event Tech Live 2025'); // Page title should be personalized
      expect(sarah).not.toMatch(/Marcus O[&#x27;']+Brien - Event Tech Live 2025/); // Shouldn't have other attendee's page title

      // Check attendee 2002 (Marcus Rodriguez)
      const marcus = await readFile(join(attendeesDir, '2002', 'index.html'), 'utf-8');
      expect(marcus).toContain('Marcus');
      expect(marcus).toContain('Marcus Rodriguez - Event Tech Live 2025'); // Page title should be personalized
      expect(marcus).not.toContain('Aisha Patel - Event Tech Live 2025'); // Shouldn't have other attendee's page title

      // Verify they're different
      expect(sarah).not.toBe(marcus);
    });

    it('should include CSS stylesheet link in all pages', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      for (const id of attendeeIds.slice(0, 5)) { // Check first 5
        const htmlPath = join(attendeesDir, id, 'index.html');
        const content = await readFile(htmlPath, 'utf-8');

        expect(content).toContain('/static/css/styles.css');
        expect(content).toContain('<link rel="stylesheet"');
      }
    });

    it('should include call-to-action links', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      for (const id of attendeeIds.slice(0, 3)) {
        const htmlPath = join(attendeesDir, id, 'index.html');
        const content = await readFile(htmlPath, 'utf-8');

        // Should have CTAs
        expect(content).toMatch(/Save the Date: Event Tech Live 2026/i);
        expect(content).toContain('cta-card');
      }
    });

    it('should include attendee stats in all pages', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const htmlPath = join(attendeesDir, '2001', 'index.html');
      const content = await readFile(htmlPath, 'utf-8');

      // Should show stats
      expect(content).toMatch(/Sessions Attended/i);
      expect(content).toMatch(/Connections Made/i);
      expect(content).toMatch(/Hours/i);
      expect(content).toContain('stat-card');
    });

    it('should include session information', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const htmlPath = join(attendeesDir, '2001', 'index.html');
      const content = await readFile(htmlPath, 'utf-8');

      // Should show sessions from mock data
      expect(content).toContain('AI-Powered Networking');
      expect(content).toContain('session-card');
    });
  });

  describe('Asset Integrity', () => {
    beforeAll(async () => {
      await generateAll(TEST_DIST_DIR);
    });

    it('should copy CSS file with complete content', async () => {
      const cssPath = join(TEST_DIST_DIR, 'static', 'css', 'styles.css');
      const content = await readFile(cssPath, 'utf-8');

      // Verify CSS has key content
      expect(content).toContain(':root');
      expect(content).toContain('--color-primary');
      expect(content).toContain('.hero');
      expect(content).toContain('.stat-card');
      expect(content).toContain('.session-card');
      expect(content).toContain('.cta-card');

      // Verify it's substantial
      expect(content.length).toBeGreaterThan(10000);
    });

    it('should have accessible file permissions', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const cssPath = join(TEST_DIST_DIR, 'static', 'css', 'styles.css');

      // Files should be readable
      await expect(access(htmlPath)).resolves.not.toThrow();
      await expect(access(cssPath)).resolves.not.toThrow();
    });
  });

  describe('Performance', () => {
    it('should generate complete site in under 3 seconds', async () => {
      const start = Date.now();
      await generateAll(TEST_DIST_DIR);
      const duration = Date.now() - start;

      expect(duration).toBeLessThan(3000);
    });

    it('should generate reasonably sized HTML files', async () => {
      await generateAll(TEST_DIST_DIR);

      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      for (const id of attendeeIds) {
        const htmlPath = join(attendeesDir, id, 'index.html');
        const stats = await stat(htmlPath);

        // Each file should be between 1KB and 500KB
        expect(stats.size).toBeGreaterThan(1024); // > 1KB
        expect(stats.size).toBeLessThan(500 * 1024); // < 500KB
      }
    });
  });

  describe('Error Handling', () => {
    it('should handle generation to same directory multiple times', async () => {
      // Generate once
      await generateAll(TEST_DIST_DIR);

      // Generate again (should overwrite)
      await expect(generateAll(TEST_DIST_DIR)).resolves.not.toThrow();

      // Files should still exist
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      await expect(access(htmlPath)).resolves.not.toThrow();
    });
  });

  describe('Data Integrity', () => {
    beforeAll(async () => {
      await generateAll(TEST_DIST_DIR);
    });

    it('should preserve data relationships between event and attendees', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      for (const id of attendeeIds.slice(0, 3)) {
        const htmlPath = join(attendeesDir, id, 'index.html');
        const content = await readFile(htmlPath, 'utf-8');

        // All attendees should reference the same event
        expect(content).toContain('Event Tech Live 2025');
        expect(content).toContain('1500'); // Total attendees
        expect(content).toContain('30'); // Total sessions
      }
    });

    it('should include correct number of sessions per attendee', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const content = await readFile(htmlPath, 'utf-8');

      // Count session cards (attendee 2001 has 10 sessions)
      const sessionMatches = content.match(/session-card/g);
      expect(sessionMatches?.length).toBe(10);
    });

    it('should include correct number of connections per attendee', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const content = await readFile(htmlPath, 'utf-8');

      // Count connection cards (attendee 2001 has 22 connections)
      const connectionMatches = content.match(/connection-card/g);
      expect(connectionMatches?.length).toBe(22);
    });
  });

  describe('Responsive Design Elements', () => {
    beforeAll(async () => {
      await generateAll(TEST_DIST_DIR);
    });

    it('should include viewport meta tag for responsive design', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const content = await readFile(htmlPath, 'utf-8');

      expect(content).toContain('width=device-width');
      expect(content).toContain('initial-scale=1.0');
    });

    it('should include responsive CSS classes', async () => {
      const cssPath = join(TEST_DIST_DIR, 'static', 'css', 'styles.css');
      const content = await readFile(cssPath, 'utf-8');

      // Check for media queries
      expect(content).toMatch(/@media.*min-width.*768px/);
      expect(content).toMatch(/@media.*min-width.*1024px/);
      expect(content).toMatch(/@media.*max-width.*767px/);
    });
  });
});
