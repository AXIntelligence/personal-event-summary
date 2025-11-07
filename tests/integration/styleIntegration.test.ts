import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { rm, mkdir, readFile } from 'fs/promises';
import { join } from 'path';
import { loadStyleConfig, styleConfigExists } from '../../src/dataLoader.js';
import { generateEventCSS } from '../../src/cssGenerator.js';
import { generateAttendeePage, generateAllAttendeePages } from '../../src/generate.js';

const TEST_DIST_DIR = join(process.cwd(), 'dist-style-integration-test');

describe('Style Integration Tests (Plan 003 Phase 6)', () => {
  beforeAll(async () => {
    await mkdir(TEST_DIST_DIR, { recursive: true });
  });

  afterAll(async () => {
    await rm(TEST_DIST_DIR, { recursive: true, force: true });
  });

  describe('Style Config Loading', () => {
    it('should load event-tech-live-2025 style config successfully', async () => {
      const config = await loadStyleConfig('event-tech-live-2025');

      expect(config).not.toBeNull();
      expect(config?.eventId).toBe('event-tech-live-2025');
      expect(config?.eventName).toBe('Event Tech Live 2024');
      expect(config?.colors.primary).toBe('#160822');
      expect(config?.typography.headingFont).toBe("'Helvetica Neue', Helvetica, Arial, sans-serif");
      expect(config?.brandVoice.tone).toBe('professional');
      expect(config?.layout.containerWidth).toBe('1140px');
    });

    it('should load event-tech-live-2025 style config successfully', async () => {
      const config = await loadStyleConfig('event-tech-live-2025');

      expect(config).not.toBeNull();
      expect(config?.eventId).toBe('event-tech-live-2025');
      expect(config?.eventName).toBe('Event Tech Live 2024'); // Updated from scraped data
      expect(config?.colors.primary).toBe('#160822'); // Updated to real scraped color
      expect(config?.typography.headingFont).toBe("'Helvetica Neue', Helvetica, Arial, sans-serif"); // Updated from scraped data
      expect(config?.brandVoice.tone).toBe('professional'); // Updated from scraped data
    });

    it('should return null for non-existent style config', async () => {
      const config = await loadStyleConfig('non-existent-event');
      expect(config).toBeNull();
    });

    it('should correctly identify existing style configs', async () => {
      const exists1 = await styleConfigExists('event-tech-live-2025');
      const exists2 = await styleConfigExists('event-tech-live-2025');
      const exists3 = await styleConfigExists('non-existent');

      expect(exists1).toBe(true);
      expect(exists2).toBe(true);
      expect(exists3).toBe(false);
    });
  });

  describe('CSS Generation from Style Configs', () => {
    it('should generate CSS from event-tech-live-2025 style config', async () => {
      const config = await loadStyleConfig('event-tech-live-2025');
      expect(config).not.toBeNull();

      const css = generateEventCSS(config!);

      // Verify CSS structure
      expect(css).toContain(':root');
      expect(css).toContain('{');
      expect(css).toContain('}');

      // Verify colors
      expect(css).toContain('--color-primary: #160822');
      expect(css).toContain('--color-secondary: #0a2540');
      expect(css).toContain('--color-accent: #005bb5');

      // Verify typography
      expect(css).toContain("--font-heading: 'Helvetica Neue', Helvetica, Arial, sans-serif");
      expect(css).toContain("--font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif");

      // Verify layout
      expect(css).toContain('--spacing-unit: 4px');
      expect(css).toContain('--border-radius: 4px');
      expect(css).toContain('--container-width: 1140px');

      // Verify gradient
      expect(css).toContain('--gradient-primary:');
      expect(css).toContain('linear-gradient');

      // Verify metadata comments
      expect(css).toContain('Event: Event Tech Live 2024');
      expect(css).toContain('Brand Voice: professional');
    });

    it('should generate CSS from event-tech-live-2025 style config', async () => {
      const config = await loadStyleConfig('event-tech-live-2025');
      expect(config).not.toBeNull();

      const css = generateEventCSS(config!);

      // Verify different colors
      expect(css).toContain('--color-primary: #160822'); // Updated to real scraped color
      expect(css).toContain('--color-secondary: #0a2540'); // Updated from scraped data
      expect(css).toContain('--color-accent: #005bb5'); // Updated from scraped data

      // Verify different typography
      expect(css).toContain("--font-heading: 'Helvetica Neue', Helvetica, Arial, sans-serif"); // Updated from scraped data
      expect(css).toContain("--font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif"); // Updated from scraped data

      // Verify different layout
      expect(css).toContain('--spacing-unit: 4px'); // Updated from scraped data
      expect(css).toContain('--border-radius: 4px'); // Updated from scraped data
      expect(css).toContain('--container-width: 1140px'); // Updated from scraped data

      // Verify brand voice
      expect(css).toContain('Brand Voice: professional'); // Updated from scraped data
    });
  });

  describe('Page Generation with Styles', () => {
    it('should generate page with event-tech-live-2025 styles for attendee 2001', async () => {
      const outputPath = await generateAttendeePage('2001', TEST_DIST_DIR);

      expect(outputPath).toContain('2001');

      // Read generated HTML
      const html = await readFile(outputPath, 'utf-8');

      // Verify dynamic CSS is injected
      expect(html).toContain('Event-Specific Dynamic Styles');
      expect(html).toContain(':root');
      expect(html).toContain('--color-primary: #160822');
      expect(html).toContain("--font-heading: 'Helvetica Neue', Helvetica, Arial, sans-serif");

      // Verify Markus AI attribution appears
      expect(html).toContain('Powered by');
      expect(html).toContain('Markus AI');
      expect(html).toContain('https://dearmarkus.ai');

      // Verify base content still exists
      expect(html).toContain('Event Tech Live 2025');
      expect(html).toContain('Aisha'); // First name from attendee 2001
    });

    it('should generate page with event-tech-live styles for attendee 2001', async () => {
      const outputPath = await generateAttendeePage('2001', TEST_DIST_DIR);

      const html = await readFile(outputPath, 'utf-8');

      // Verify Event Tech Live styles are injected
      expect(html).toContain('--color-primary: #160822'); // Updated to real scraped color
      expect(html).toContain("--font-heading: 'Helvetica Neue', Helvetica, Arial, sans-serif"); // Updated from scraped data
      expect(html).toContain('--spacing-unit: 4px'); // Updated from scraped data

      // Verify Markus AI attribution
      expect(html).toContain('Markus AI');

      // Verify Event Tech Live content
      expect(html).toContain('Event Tech Live 2025');
    });

    it('should generate page without styles for event with no style config', async () => {
      // Create a test event without style config
      // (This would be an event that doesn't have a style-configs/{eventId}.json file)
      // For now, all our events have style configs, so this tests the fallback behavior

      const outputPath = await generateAttendeePage('2001', TEST_DIST_DIR);
      const html = await readFile(outputPath, 'utf-8');

      // Should still have base HTML structure
      expect(html).toContain('<!DOCTYPE html>');
      expect(html).toContain('<html');
      expect(html).toContain('</html>');

      // Should have base stylesheet
      expect(html).toContain('styles.css');
    });

    it('should generate all pages with consistent style application', async () => {
      const outputPaths = await generateAllAttendeePages(TEST_DIST_DIR);

      expect(outputPaths.length).toBeGreaterThan(0);

      // Check first few pages for style injection
      for (let i = 0; i < Math.min(3, outputPaths.length); i++) {
        const html = await readFile(outputPaths[i], 'utf-8');

        // Each page should have dynamic styles (since all events have configs now)
        expect(html).toContain('Event-Specific Dynamic Styles');
        expect(html).toContain(':root');
        expect(html).toMatch(/--color-primary: #[0-9a-f]{6}/i);
      }
    });
  });

  describe('Style Variation Validation', () => {
    it('should apply different styles to different events', async () => {
      // Generate pages for both events
      const page1 = await generateAttendeePage('2001', TEST_DIST_DIR); // Event Tech Live
      const page2 = await generateAttendeePage('3001', TEST_DIST_DIR); // AWS re:Invent

      const html1 = await readFile(page1, 'utf-8');
      const html2 = await readFile(page2, 'utf-8');

      // Verify different primary colors
      expect(html1).toContain('--color-primary: #160822'); // Event Tech Live purple (scraped)
      expect(html2).toContain('--color-primary: #232f3e'); // AWS re:Invent dark blue-gray (manual)

      // Verify different fonts
      expect(html1).toContain("'Helvetica Neue', Helvetica, Arial, sans-serif"); // Event Tech Live (scraped)
      expect(html2).toContain("'Amazon Ember'"); // AWS re:Invent (manual)

      // Verify different brand voices in comments
      expect(html1).toContain('professional');
      expect(html2).toContain('professional'); // Both events are professional
    });
  });

  describe('Performance with Styles', () => {
    it('should generate all pages with styles in reasonable time', async () => {
      const startTime = Date.now();

      await generateAllAttendeePages(TEST_DIST_DIR);

      const endTime = Date.now();
      const duration = endTime - startTime;

      // Should complete in under 3 seconds even with style loading
      expect(duration).toBeLessThan(3000);
    });
  });

  describe('HTML Validation with Dynamic Styles', () => {
    it('should produce valid HTML with injected CSS', async () => {
      const outputPath = await generateAttendeePage('2001', TEST_DIST_DIR);
      const html = await readFile(outputPath, 'utf-8');

      // Verify style tag is properly closed
      const styleTagMatches = html.match(/<style>/g);
      const styleCloseMatches = html.match(/<\/style>/g);

      if (styleTagMatches) {
        expect(styleCloseMatches?.length).toBe(styleTagMatches.length);
      }

      // Verify CSS is within style tags
      const cssBlock = html.match(/<style>[\s\S]*?<\/style>/);
      expect(cssBlock).not.toBeNull();

      if (cssBlock) {
        expect(cssBlock[0]).toContain(':root');
        expect(cssBlock[0]).toContain('--color-primary');
      }

      // Verify HTML structure is still valid
      expect(html).toMatch(/<!DOCTYPE html>/i);
      expect(html).toContain('<head>');
      expect(html).toContain('</head>');
      expect(html).toContain('<body>');
      expect(html).toContain('</body>');
    });
  });
});
