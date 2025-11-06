import { describe, it, expect } from 'vitest';
import { generateEventCSS } from '../../src/cssGenerator.js';
import type { EventStyleConfig } from '../../src/types/index.js';

describe('CSS Generator (Plan 003)', () => {
  const mockStyleConfig: EventStyleConfig = {
    eventId: 'test-event-2025',
    eventName: 'Test Conference 2025',
    sourceUrl: 'https://testconf.example.com',
    colors: {
      primary: '#667eea',
      secondary: '#764ba2',
      accent: '#f56565',
      background: '#ffffff',
      text: '#1a202c',
    },
    typography: {
      headingFont: 'Inter, sans-serif',
      bodyFont: 'system-ui, sans-serif',
      headingSize: '2.5rem',
      bodySize: '1rem',
      lineHeight: '1.6',
    },
    brandVoice: {
      tone: 'professional',
      keywords: ['innovation', 'technology', 'excellence'],
      style: 'formal',
      personality: 'authoritative',
    },
    layout: {
      gridSystem: 'flexbox',
      spacingUnit: '8px',
      borderRadius: '8px',
      containerWidth: '1200px',
    },
  };

  describe('generateEventCSS', () => {
    it('should generate valid CSS custom properties', () => {
      const css = generateEventCSS(mockStyleConfig);

      expect(css).toContain(':root');
      expect(css).toContain('{');
      expect(css).toContain('}');
    });

    it('should include all color properties', () => {
      const css = generateEventCSS(mockStyleConfig);

      expect(css).toContain('--color-primary: #667eea');
      expect(css).toContain('--color-secondary: #764ba2');
      expect(css).toContain('--color-accent: #f56565');
      expect(css).toContain('--color-background: #ffffff');
      expect(css).toContain('--color-text: #1a202c');
    });

    it('should include typography properties', () => {
      const css = generateEventCSS(mockStyleConfig);

      expect(css).toContain('--font-heading: Inter, sans-serif');
      expect(css).toContain('--font-body: system-ui, sans-serif');
      expect(css).toContain('--font-size-heading: 2.5rem');
      expect(css).toContain('--font-size-body: 1rem');
      expect(css).toContain('--line-height: 1.6');
    });

    it('should include layout properties', () => {
      const css = generateEventCSS(mockStyleConfig);

      expect(css).toContain('--spacing-unit: 8px');
      expect(css).toContain('--border-radius: 8px');
      expect(css).toContain('--container-width: 1200px');
    });

    it('should handle RGB color format', () => {
      const configWithRgb: EventStyleConfig = {
        ...mockStyleConfig,
        colors: {
          ...mockStyleConfig.colors,
          primary: 'rgb(102, 126, 234)',
        },
      };

      const css = generateEventCSS(configWithRgb);
      expect(css).toContain('--color-primary: rgb(102, 126, 234)');
    });

    it('should handle RGBA color format', () => {
      const configWithRgba: EventStyleConfig = {
        ...mockStyleConfig,
        colors: {
          ...mockStyleConfig.colors,
          accent: 'rgba(245, 101, 101, 0.9)',
        },
      };

      const css = generateEventCSS(configWithRgba);
      expect(css).toContain('--color-accent: rgba(245, 101, 101, 0.9)');
    });

    it('should handle HSL color format', () => {
      const configWithHsl: EventStyleConfig = {
        ...mockStyleConfig,
        colors: {
          ...mockStyleConfig.colors,
          secondary: 'hsl(280, 46%, 50%)',
        },
      };

      const css = generateEventCSS(configWithHsl);
      expect(css).toContain('--color-secondary: hsl(280, 46%, 50%)');
    });

    it('should create gradient CSS variable from primary and secondary colors', () => {
      const css = generateEventCSS(mockStyleConfig);

      // Should create a gradient variable combining primary and secondary
      expect(css).toMatch(/--gradient-primary:.*linear-gradient/);
      expect(css).toMatch(/--gradient-primary:.*#667eea/);
      expect(css).toMatch(/--gradient-primary:.*#764ba2/);
    });

    it('should handle different spacing units', () => {
      const configWithRem: EventStyleConfig = {
        ...mockStyleConfig,
        layout: {
          ...mockStyleConfig.layout,
          spacingUnit: '0.5rem',
        },
      };

      const css = generateEventCSS(configWithRem);
      expect(css).toContain('--spacing-unit: 0.5rem');
    });

    it('should handle different border radius values', () => {
      const configWithLargeRadius: EventStyleConfig = {
        ...mockStyleConfig,
        layout: {
          ...mockStyleConfig.layout,
          borderRadius: '16px',
        },
      };

      const css = generateEventCSS(configWithLargeRadius);
      expect(css).toContain('--border-radius: 16px');
    });

    it('should not include brand voice properties in CSS (comment only)', () => {
      const css = generateEventCSS(mockStyleConfig);

      // Brand voice should not be in CSS custom properties
      expect(css).not.toContain('--tone:');
      expect(css).not.toContain('--style:');
      expect(css).not.toContain('--keywords:');

      // But might include as a CSS comment for reference
      expect(css).toContain('Brand Voice:');
      expect(css).toContain('professional');
    });

    it('should include event metadata as CSS comments', () => {
      const css = generateEventCSS(mockStyleConfig);

      expect(css).toContain('Event: Test Conference 2025');
      expect(css).toContain('Event ID: test-event-2025');
      expect(css).toContain('Source: https://testconf.example.com');
    });

    it('should produce valid CSS that can be parsed', () => {
      const css = generateEventCSS(mockStyleConfig);

      // Basic CSS validation
      const rootBlocks = css.match(/:root\s*\{[^}]+\}/g);
      expect(rootBlocks).toBeTruthy();
      expect(rootBlocks!.length).toBeGreaterThan(0);

      // Should have balanced braces
      const openBraces = (css.match(/{/g) || []).length;
      const closeBraces = (css.match(/}/g) || []).length;
      expect(openBraces).toBe(closeBraces);
    });

    it('should handle font families with quotes', () => {
      const configWithQuotedFont: EventStyleConfig = {
        ...mockStyleConfig,
        typography: {
          ...mockStyleConfig.typography,
          headingFont: '"Helvetica Neue", Arial, sans-serif',
        },
      };

      const css = generateEventCSS(configWithQuotedFont);
      expect(css).toContain('--font-heading: "Helvetica Neue", Arial, sans-serif');
    });

    it('should generate CSS with consistent formatting', () => {
      const css = generateEventCSS(mockStyleConfig);

      // Should use consistent indentation (2 spaces)
      expect(css).toMatch(/\n  --color-/);
      expect(css).toMatch(/\n  --font-/);

      // Should end properties with semicolons
      const propertyLines = css.split('\n').filter(line => line.includes('--'));
      propertyLines.forEach(line => {
        if (line.trim().length > 0) {
          expect(line).toMatch(/;\s*$/);
        }
      });
    });

    it('should handle minimal configuration gracefully', () => {
      const minimalConfig: EventStyleConfig = {
        eventId: 'minimal',
        eventName: 'Minimal Event',
        sourceUrl: 'https://example.com',
        colors: {
          primary: '#000000',
          secondary: '#ffffff',
          accent: '#ff0000',
          background: '#ffffff',
          text: '#000000',
        },
        typography: {
          headingFont: 'sans-serif',
          bodyFont: 'sans-serif',
          headingSize: '2rem',
          bodySize: '1rem',
          lineHeight: '1.5',
        },
        brandVoice: {
          tone: 'neutral',
          keywords: [],
          style: 'standard',
        },
        layout: {
          gridSystem: 'flexbox',
          spacingUnit: '8px',
          borderRadius: '4px',
          containerWidth: '1200px',
        },
      };

      const css = generateEventCSS(minimalConfig);
      expect(css).toContain(':root');
      expect(css).toContain('--color-primary: #000000');
    });

    it('should create derived color variables for UI states', () => {
      const css = generateEventCSS(mockStyleConfig);

      // Should create hover, active, disabled states
      // These might be computed variations of the base colors
      expect(css).toMatch(/--color-primary-hover:|--color-hover:/);
    });

    it('should return CSS as a string', () => {
      const css = generateEventCSS(mockStyleConfig);
      expect(typeof css).toBe('string');
      expect(css.length).toBeGreaterThan(0);
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty keywords array', () => {
      const configWithEmptyKeywords: EventStyleConfig = {
        ...mockStyleConfig,
        brandVoice: {
          ...mockStyleConfig.brandVoice,
          keywords: [],
        },
      };

      const css = generateEventCSS(configWithEmptyKeywords);
      expect(css).toContain(':root');
    });

    it('should handle missing optional personality field', () => {
      const configWithoutPersonality: EventStyleConfig = {
        ...mockStyleConfig,
        brandVoice: {
          tone: 'casual',
          keywords: ['fun', 'friendly'],
          style: 'conversational',
        },
      };

      const css = generateEventCSS(configWithoutPersonality);
      expect(css).toContain(':root');
      expect(css).toContain('casual');
    });

    it('should handle very long font family names', () => {
      const configWithLongFont: EventStyleConfig = {
        ...mockStyleConfig,
        typography: {
          ...mockStyleConfig.typography,
          headingFont: '"SF Pro Display", "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif',
        },
      };

      const css = generateEventCSS(configWithLongFont);
      expect(css).toContain('SF Pro Display');
    });
  });
});
