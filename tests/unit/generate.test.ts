import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { readFile, access, readdir, rm } from 'fs/promises';
import { join } from 'path';
import {
  generateAttendeePage,
  generateAllAttendeePages,
  copyStaticAssets,
  setupHandlebars
} from '../../src/generate.js';

const TEST_DIST_DIR = join(process.cwd(), 'dist-test');

describe('generate', () => {
  beforeAll(async () => {
    // Clean up test directory if it exists
    try {
      await rm(TEST_DIST_DIR, { recursive: true, force: true });
    } catch {
      // Ignore if doesn't exist
    }
  });

  afterAll(async () => {
    // Clean up test directory after tests
    try {
      await rm(TEST_DIST_DIR, { recursive: true, force: true });
    } catch {
      // Ignore cleanup errors
    }
  });

  describe('setupHandlebars', () => {
    it('should setup Handlebars with templates and helpers', async () => {
      const hbs = await setupHandlebars();

      expect(hbs).toBeDefined();
      expect(typeof hbs.compile).toBe('function');
    });

    it('should register formatDate helper', async () => {
      const hbs = await setupHandlebars();

      // Test that helper exists by compiling a template using it
      const template = hbs.compile('{{formatDate date}}');
      const result = template({ date: '2025-03-15T09:00:00Z' });

      expect(result).toBeTruthy();
      expect(result.length).toBeGreaterThan(0);
    });

    it('should register substring helper', async () => {
      const hbs = await setupHandlebars();

      const template = hbs.compile('{{substring text 0 1}}');
      const result = template({ text: 'Hello' });

      expect(result).toBe('H');
    });

    it('should register currentYear helper', async () => {
      const hbs = await setupHandlebars();

      const template = hbs.compile('{{currentYear}}');
      const result = template({});

      const year = new Date().getFullYear();
      expect(result).toBe(year.toString());
    });

    it('should register CTA partial', async () => {
      const hbs = await setupHandlebars();

      // Test that partial is registered by using it
      const template = hbs.compile('{{> cta this}}');
      const result = template({
        text: 'Test CTA',
        url: 'https://example.com',
        type: 'primary'
      });

      expect(result).toContain('Test CTA');
      expect(result).toContain('https://example.com');
    });
  });

  describe('generateAttendeePage', () => {
    it('should generate HTML page for an attendee', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);

      expect(outputPath).toBeTruthy();
      expect(outputPath).toContain('1001');
      expect(outputPath).toContain('index.html');

      // Verify file was created
      await expect(access(outputPath)).resolves.not.toThrow();
    });

    it('should create nested directory structure', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);

      // Path should be dist/attendees/1001/index.html
      expect(outputPath).toMatch(/attendees\/1001\/index\.html$/);
    });

    it('should generate valid HTML content', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      // Check for basic HTML structure
      expect(content).toContain('<!DOCTYPE html>');
      expect(content).toContain('<html');
      expect(content).toContain('</html>');
      expect(content).toContain('<head>');
      expect(content).toContain('</head>');
      expect(content).toContain('<body>');
      expect(content).toContain('</body>');
    });

    it('should include attendee personalization', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      // Should contain attendee's first name and achievement (Sarah from mock data)
      expect(content).toContain('Sarah');
      expect(content).toContain('Early Bird Attendee');
    });

    it('should include event information', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      // Should contain event name
      expect(content).toContain('TechConf 2025');
      expect(content).toContain('San Francisco');
    });

    it('should include attendee stats', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      // Should show stats from mock data
      expect(content).toMatch(/Sessions Attended/i);
      expect(content).toMatch(/Connections Made/i);
      expect(content).toMatch(/Hours Invested/i);
    });

    it('should include sessions attended', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      // Should include session titles from mock data
      expect(content).toContain('Future of AI');
      expect(content).toContain('Building Scalable Microservices');
    });

    it('should include call-to-actions', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      // Should include CTAs
      expect(content).toMatch(/Register for TechConf 2026/i);
    });

    it('should link to CSS stylesheet', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      expect(content).toContain('/static/css/styles.css');
    });

    it('should throw error for non-existent attendee', async () => {
      await expect(
        generateAttendeePage('99999', TEST_DIST_DIR)
      ).rejects.toThrow();
    });

    it('should generate unique content for different attendees', async () => {
      const output1 = await generateAttendeePage('1001', TEST_DIST_DIR);
      const output2 = await generateAttendeePage('1002', TEST_DIST_DIR);

      const content1 = await readFile(output1, 'utf-8');
      const content2 = await readFile(output2, 'utf-8');

      // Content should be different
      expect(content1).not.toBe(content2);

      // Should contain different attendee names
      expect(content1).toContain('Sarah');
      expect(content2).toContain('Michael');
    });

    it('should handle attendees with different engagement levels', async () => {
      // Attendee 1002 has more sessions/connections
      const output = await generateAttendeePage('1002', TEST_DIST_DIR);
      const content = await readFile(output, 'utf-8');

      // Should show higher stats
      expect(content).toContain('5'); // 5 sessions attended
    });
  });

  describe('generateAllAttendeePages', () => {
    it('should generate pages for all attendees', async () => {
      const results = await generateAllAttendeePages(TEST_DIST_DIR);

      expect(Array.isArray(results)).toBe(true);
      expect(results.length).toBeGreaterThanOrEqual(10);
    });

    it('should return array of output paths', async () => {
      const results = await generateAllAttendeePages(TEST_DIST_DIR);

      results.forEach(path => {
        expect(path).toContain('attendees');
        expect(path).toContain('index.html');
      });
    });

    it('should create files for all attendees', async () => {
      await generateAllAttendeePages(TEST_DIST_DIR);

      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const dirs = await readdir(attendeesDir);

      expect(dirs.length).toBeGreaterThanOrEqual(10);
    });

    it('should create valid index.html in each attendee directory', async () => {
      await generateAllAttendeePages(TEST_DIST_DIR);

      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const dirs = await readdir(attendeesDir);

      for (const dir of dirs.slice(0, 3)) { // Check first 3
        const indexPath = join(attendeesDir, dir, 'index.html');
        await expect(access(indexPath)).resolves.not.toThrow();

        const content = await readFile(indexPath, 'utf-8');
        expect(content).toContain('<!DOCTYPE html>');
      }
    });

    it('should handle errors gracefully', async () => {
      // Should not throw even if some generation fails
      const results = await generateAllAttendeePages(TEST_DIST_DIR);
      expect(results).toBeDefined();
    });
  });

  describe('copyStaticAssets', () => {
    it('should copy CSS files to dist directory', async () => {
      await copyStaticAssets(TEST_DIST_DIR);

      const cssPath = join(TEST_DIST_DIR, 'static', 'css', 'styles.css');
      await expect(access(cssPath)).resolves.not.toThrow();
    });

    it('should preserve CSS content', async () => {
      await copyStaticAssets(TEST_DIST_DIR);

      const cssPath = join(TEST_DIST_DIR, 'static', 'css', 'styles.css');
      const content = await readFile(cssPath, 'utf-8');

      expect(content).toContain(':root');
      expect(content).toContain('--color-primary');
      expect(content.length).toBeGreaterThan(1000);
    });

    it('should create static directory structure', async () => {
      await copyStaticAssets(TEST_DIST_DIR);

      const staticDir = join(TEST_DIST_DIR, 'static');
      const cssDir = join(staticDir, 'css');

      await expect(access(staticDir)).resolves.not.toThrow();
      await expect(access(cssDir)).resolves.not.toThrow();
    });

    it('should copy images directory if it exists', async () => {
      await copyStaticAssets(TEST_DIST_DIR);

      const imagesDir = join(TEST_DIST_DIR, 'static', 'images');
      // Should create directory even if empty
      await expect(access(imagesDir)).resolves.not.toThrow();
    });

    it('should handle missing static directory gracefully', async () => {
      // Should not throw if static dir has issues
      await expect(copyStaticAssets(TEST_DIST_DIR)).resolves.not.toThrow();
    });
  });

  describe('Performance', () => {
    it('should generate single page in under 100ms', async () => {
      const start = Date.now();
      await generateAttendeePage('1001', TEST_DIST_DIR);
      const duration = Date.now() - start;

      expect(duration).toBeLessThan(100);
    });

    it('should generate all pages in under 2 seconds', async () => {
      const start = Date.now();
      await generateAllAttendeePages(TEST_DIST_DIR);
      const duration = Date.now() - start;

      // Should be fast even with 12+ attendees
      expect(duration).toBeLessThan(2000);
    });
  });

  describe('File Size', () => {
    it('should generate HTML files larger than 1KB', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      const sizeInBytes = Buffer.byteLength(content, 'utf-8');
      expect(sizeInBytes).toBeGreaterThan(1024); // > 1KB
    });

    it('should generate reasonable file sizes under 500KB', async () => {
      const outputPath = await generateAttendeePage('1001', TEST_DIST_DIR);
      const content = await readFile(outputPath, 'utf-8');

      const sizeInBytes = Buffer.byteLength(content, 'utf-8');
      expect(sizeInBytes).toBeLessThan(500 * 1024); // < 500KB
    });
  });
});
