import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { HtmlValidate } from 'html-validate';
import { readFile, readdir, rm } from 'fs/promises';
import { join } from 'path';
import { generateAll } from '../../src/generate.js';

const TEST_DIST_DIR = join(process.cwd(), 'dist-validation-test');

describe('HTML Validation Tests', () => {
  let htmlvalidate: HtmlValidate;

  beforeAll(async () => {
    // Clean up test directory
    try {
      await rm(TEST_DIST_DIR, { recursive: true, force: true });
    } catch {
      // Ignore if doesn't exist
    }

    // Generate all pages for validation
    await generateAll(TEST_DIST_DIR);

    // Initialize HTML validator with configuration
    htmlvalidate = new HtmlValidate({
      extends: ['html-validate:recommended'],
      rules: {
        // Allow void elements (img, link, meta) without trailing slash
        'void-style': 'off',
        // Allow multiple h1 tags (sections may have their own)
        'no-multiple-h1': 'warn',
        // Allow inline styles for dynamic content
        'no-inline-style': 'warn',
        // Allow external links without rel=noopener (already added in templates)
        'require-sri': 'off'
      }
    });
  });

  afterAll(async () => {
    // Clean up after tests
    try {
      await rm(TEST_DIST_DIR, { recursive: true, force: true });
    } catch {
      // Ignore cleanup errors
    }
  });

  describe('W3C HTML5 Validation', () => {
    it('should validate 404.html page', async () => {
      const htmlPath = join(process.cwd(), '404.html');
      const html = await readFile(htmlPath, 'utf-8');

      const report = await htmlvalidate.validateString(html);

      expect(report.valid).toBe(true);
      if (!report.valid) {
        console.error('Validation errors in 404.html:', report.results);
      }
    });

    it('should validate all generated attendee pages', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      const validationPromises = attendeeIds.map(async (id) => {
        const htmlPath = join(attendeesDir, id, 'index.html');
        const html = await readFile(htmlPath, 'utf-8');

        const report = await htmlvalidate.validateString(html);

        if (!report.valid) {
          console.error(`Validation errors in attendee ${id}:`, report.results);
        }

        return { id, valid: report.valid, report };
      });

      const results = await Promise.all(validationPromises);

      // All pages should be valid
      const invalidPages = results.filter(r => !r.valid);
      expect(invalidPages.length).toBe(0);

      if (invalidPages.length > 0) {
        console.error('Invalid pages:', invalidPages.map(p => p.id));
      }
    });

    it('should have no critical HTML errors in any page', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      let totalErrors = 0;
      let totalWarnings = 0;

      for (const id of attendeeIds) {
        const htmlPath = join(attendeesDir, id, 'index.html');
        const html = await readFile(htmlPath, 'utf-8');

        const report = await htmlvalidate.validateString(html);

        totalErrors += report.errorCount;
        totalWarnings += report.warningCount;
      }

      // Should have no errors (warnings are acceptable)
      expect(totalErrors).toBe(0);

      console.log(`HTML Validation Summary: ${totalErrors} errors, ${totalWarnings} warnings across ${attendeeIds.length} pages`);
    });
  });

  describe('Semantic HTML Structure', () => {
    it('should have proper document structure', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      // Check for semantic HTML5 elements
      expect(html).toMatch(/<header[^>]*>/);
      expect(html).toMatch(/<main[^>]*>/);
      expect(html).toMatch(/<footer[^>]*>/);
      expect(html).toMatch(/<section[^>]*>/);

      // Check for proper heading hierarchy
      expect(html).toContain('<h1');
      expect(html).toContain('<h2');
      expect(html).toContain('<h3');
    });

    it('should use semantic HTML5 elements appropriately', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      // Should use semantic elements
      const semanticElements = [
        'header',
        'main',
        'footer',
        'section',
        'nav'
      ];

      // At least some semantic elements should be present
      const foundElements = semanticElements.filter(element =>
        html.includes(`<${element}`)
      );

      expect(foundElements.length).toBeGreaterThanOrEqual(4);
    });
  });

  describe('Accessibility Validation', () => {
    it('should have proper meta tags', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      // Check for essential meta tags
      expect(html).toContain('<meta charset="UTF-8">');
      expect(html).toContain('viewport');
      expect(html).toContain('<title>');
      expect(html).toContain('description');
    });

    it('should have proper alt attributes for images', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      // All img tags should have alt attributes
      const imgTags = html.match(/<img[^>]+>/g) || [];

      for (const imgTag of imgTags) {
        expect(imgTag).toMatch(/alt=["'][^"']*["']/);
      }
    });

    it('should have proper link attributes for external links', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      // External links should have target="_blank" and rel="noopener noreferrer"
      const externalLinks = html.match(/<a[^>]*href=["']https?:\/\/[^"']+["'][^>]*>/g) || [];

      for (const link of externalLinks) {
        if (link.includes('target="_blank"')) {
          expect(link).toMatch(/rel=["'][^"']*noopener[^"']*["']/);
        }
      }
    });

    it('should have proper lang attribute', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      expect(html).toMatch(/<html[^>]*lang=["'][^"']+["'][^>]*>/);
    });
  });

  describe('Performance Best Practices', () => {
    it('should have resource hints for external resources', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      // Should have preconnect for external fonts
      const hasPreconnect = html.includes('rel="preconnect"');
      expect(hasPreconnect).toBe(true);
    });

    it('should have CSS in head and minimal inline styles', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      // Should have external stylesheet link
      expect(html).toContain('<link rel="stylesheet"');

      // Count inline style tags (should be minimal or none)
      const inlineStyles = (html.match(/<style[^>]*>/g) || []).length;
      expect(inlineStyles).toBeLessThanOrEqual(1);
    });

    it('should defer or async non-critical JavaScript', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      // If there are external scripts, they should be deferred or async
      const scriptTags = html.match(/<script[^>]*src=["'][^"']+["'][^>]*>/g) || [];

      for (const script of scriptTags) {
        // External scripts should have defer or async, or be at end of body
        const hasDefer = script.includes('defer');
        const hasAsync = script.includes('async');
        const isAtEnd = html.indexOf(script) > html.lastIndexOf('</main>');

        expect(hasDefer || hasAsync || isAtEnd).toBe(true);
      }
    });
  });

  describe('Content Integrity', () => {
    it('should not have broken HTML comments or unclosed tags', async () => {
      const attendeesDir = join(TEST_DIST_DIR, 'attendees');
      const attendeeIds = await readdir(attendeesDir);

      for (const id of attendeeIds.slice(0, 5)) { // Check first 5
        const htmlPath = join(attendeesDir, id, 'index.html');
        const html = await readFile(htmlPath, 'utf-8');

        const report = await htmlvalidate.validateString(html);

        // Check for specific structural errors
        const structuralErrors = report.results[0]?.messages.filter(msg =>
          msg.ruleId === 'element-required-content' ||
          msg.ruleId === 'element-permitted-content' ||
          msg.ruleId === 'close-order'
        ) || [];

        expect(structuralErrors.length).toBe(0);
      }
    });

    it('should not have duplicate IDs', async () => {
      const htmlPath = join(TEST_DIST_DIR, 'attendees', '2001', 'index.html');
      const html = await readFile(htmlPath, 'utf-8');

      const report = await htmlvalidate.validateString(html);

      const duplicateIdErrors = report.results[0]?.messages.filter(msg =>
        msg.ruleId === 'no-dup-id'
      ) || [];

      expect(duplicateIdErrors.length).toBe(0);
    });
  });
});
